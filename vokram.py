#!/usr/bin/env python

"""
A simple, generic implementation of Markov chains in Python, with some helpers
for generating chains of words. A brief overview of how this works:

 1. Build a Markov model from a given corpus, which can be a sequence of
    basically anything (e.g., numbers, words). Special support is provided for
    building models based on words in strings or file-like objects.

    In this implementation, a model is a dictionary that maps tuples of
    n-grams to lists of the items that appear after those n-grams in the input
    corpus. The size of the n-grams is determined by the user, but currently
    defaults to 2.

    So, taking this simple corpus as an example (where ">>>" represents the
    interactive Python prompt):

      >>> corpus = [1, 2, 3, 2, 4, 5, 6, 2, 1, 3]

    The model, based on the default n-gram size of 2, would look like this:

      >>> build_model(corpus)
      {(1, 2): [3, 3, 4],
       (2, 1): [2],
       (2, 3): [1, 2],
       (2, 4): [3],
       (2, 5): [4],
       (3, 1): [2],
       (3, 2): [1, 5],
       (4, 3): [2, 1],
       (5, 4): [3]}

    For reference, the model of the same corpus with an n-gram size of 3 would
    look like this:

      >>> build_model(corpus, n=3)
      {(1, 2, 3): [1, 2],
       (1, 2, 4): [3],
       (2, 1, 2): [4],
       (2, 3, 1): [2],
       (2, 3, 2): [1],
       (2, 4, 3): [2],
       (2, 5, 4): [3],
       (3, 1, 2): [3],
       (3, 2, 1): [2],
       (3, 2, 5): [4],
       (4, 3, 2): [5],
       (5, 4, 3): [1]}

 2. Once the model is built, we can use it to construct a Markov chain of (I
    think, though there's a decent chance I'm butchering some or all of these
    concepts) statistically likely outputs.

    The process for building a chain works like this:

     a. Get a starting key in the model (chosen by the user or chosen
        randomly). For our purposes, let's choose the key (2, 3) from the
        first model above.

     b. Pick a random item from the list that our chosen key points to and add
        it to our chain. Let's say we choose 2 from the list [1, 2].

     c. Build a new key by dropping the first item in our current key and
        appending the item we chose in step b. This gives us a new key,
        (3, 2).

     d. Start over at step b, using our new key. In this example, we'd end up
        choosing a random value from the list [1, 5] to add to our chain. Do
        this until the chain has reached the desired length.

Note, there is a specialized markov_words version of the markov_chain function
that tries to slightly better at generating Markov chains that make
complete-ish sentences by trying to pick good starting keys and ensuring that
the chain ends in some kind of "sentence-ending" punctuation.

With inspiration from:
http://code.activestate.com/recipes/194364-the-markov-chain-algorithm/
"""

import os
import random
import sys
from collections import defaultdict


DEFAULT_NGRAM_SIZE = 2
MIN_SENTENCE_LENGTH = 5


##############################################################################
# Basic interface
##############################################################################

def markov_chain(model, length, start_key=None):
    """Generates a Markov chain with the given length based on the given
    model. The chain will be returned as a list. If a starting key (in the
    model) is not given, a random one will be chosen.
    """
    chain = []
    key = start_key or random.choice(model.keys())
    for _ in xrange(length):
        # Add a random selection from the value corresponding to the current
        # key to the chain.
        x = random.choice(model[key])
        chain.append(x)
        # Pick the next key by dropping the first item in the current key and
        # appending the current item (manually creating the n-gram that will
        # let us choose the next appropriate item for our chain)
        key = key[1:] + (x,)
    return chain

def build_model(xs, n=DEFAULT_NGRAM_SIZE):
    """Builds a model of the given sequence using n-grams of size n. The model
    is a dict mapping n-gram keys to lists of items appearing immediately
    after those n-grams.
    """
    model = defaultdict(list)
    for ngram in gen_ngrams(xs, n+1):
        key, item = ngram[:-1], ngram[-1]
        model[key].append(item)
    return dict(model)


##############################################################################
# Word-based interface
##############################################################################

def markov_words(model, length, start_key=None):
    """Generates a Markov chain of approximately the given length. Attempts to
    be intelligent about generating chains made up of what (hopefully) look
    like complete sentences, which means that the resulting sentence will
    often have fewer than the desired number of words.
    """

    # An overly-simplistic heuristic to use to try to generate complete
    # sentences
    sentence_end = ('.', '!', '?', '"', "'")

    # Find a start key that (hopefully) indicates the end of a sentence, which
    # will make it more likely that our chain will start with a word from the
    # beginning of a sentence.
    if start_key is None:
        keys = model.keys()
        key = random.choice(keys)
        # Making sure the key ends in a period (instead of anything in
        # sentence_end) seems to yield better results at the start of the
        # chain.
        while not key[-1][-1] == '.':
            key = random.choice(keys)
        start_key = key

    # Make sure our chain seems to end at the end of a sentence, by dropping
    # any dangling words after the end of the last sentence in the chain.
    chain = markov_chain(model, length, start_key)
    if chain[-1][-1] not in sentence_end:
        for i in xrange(length-1, -1, -1):
            if chain[i][-1] in sentence_end:
                break
        chain = chain[:i+1]

    # Make sure we've got a reasonable-sized chain.
    if len(chain) < MIN_SENTENCE_LENGTH:
        return markov_words(model, length)
    else:
        return ' '.join(chain)

def build_word_model(corpus, n=DEFAULT_NGRAM_SIZE):
    """A special-case of build_model that knows how to build a model based on
    words from a corpus given as a string or a file-like object.
    """
    return build_model(gen_words(corpus), n=n)


##############################################################################
# Utility functions
##############################################################################

def gen_ngrams(xs, n=DEFAULT_NGRAM_SIZE):
    """Yields n-grams from the given sequence. Assumes len(xs) >= n. N-grams
    are yielded as tuples of length n.
    """
    # Explicitly capture an iterator over xs, because we'll need it twice
    it = iter(xs)

    # Build and yield the first n-gram. This is where the assumption of
    # len(xs) >= n needs to be true.
    n_gram = tuple(it.next() for _ in xrange(n))
    yield n_gram

    # Each successive n-gram is built by dropping the first item of the
    # previous n-gram and appending the current element
    for x in it:
        n_gram = n_gram[1:] + (x,)
        yield n_gram

def gen_words(corpus):
    """Yields each word from the given corpus, which can be either a string or
    a file-like object containing the words.
    """
    # If we're given the corpus as a string, split it into lines so that we
    # can iterate over it the same as we would an open file.
    if isinstance(corpus, basestring):
        corpus = corpus.splitlines()
    for line in corpus:
        for word in line.strip().split():
            yield word


if __name__ == '__main__':
    usage = """%s corpus [length]""" % sys.argv[0]
    try:
        corpus = sys.argv[1]
    except IndexError:
        print usage
        sys.exit(1)
    else:
        try:
            length = int(sys.argv[2])
        except (IndexError, ValueError):
            length = 30
        model = build_word_model(open(corpus))
        try:
            print markov_words(model, length)
        except RuntimeError, e:
            print 'Could not generate a chain with length %s.' % length,
            print 'Please consider increasing the length.'
