"""
A simple, generic implementation of Markov chains in Python, with some
helpers for generating chains of words.

With inspiration from:
http://code.activestate.com/recipes/194364-the-markov-chain-algorithm/
"""

import os
import pickle
import random
import sys
from collections import defaultdict


def markov(model, length, start_key=None):
    """Generates a Markov chain based on the given model with the given word
    count."""
    chain = []
    key = start_key or random.choice(model.keys())
    for _ in xrange(length):
        x = random.choice(model[key])
        chain.append(x)
        key = key[1:] + (x,)
    return chain

def build_model(xs, n=2):
    """Builds a model of the given sequence using n-grams of size n. The model
    is a dict mapping n-gram keys to lists of items appearing immediately
    after those n-grams."""
    model = defaultdict(list)
    for ngram in gen_ngrams(xs, n+1):
        key, item = ngram[:-1], ngram[-1]
        model[key].append(item)
    return dict(model)

def build_word_model(corpus, n=2):
    """A special-case of build_model that knows how to build a model based on
    words from a corpus given as a string or a file-like object."""
    return build_model(gen_words(corpus), n=n)

def gen_ngrams(xs, n=2):
    """Yields n-grams from the given sequence. Assumes len(xs) >= n."""
    it = iter(xs)
    gram = tuple(it.next() for _ in xrange(n))
    yield gram
    for x in xs:
        gram = gram[1:] + (x,)
        yield gram

def gen_words(corpus):
    """Yields each word from the given corpus, which can be either a string or
    a file-like object containing the words."""
    if isinstance(corpus, basestring):
        corpus = (line for line in corpus.splitlines())
    for line in corpus:
        for word in line.strip().split():
            yield word

if __name__ == '__main__':
    try:
        length = int(sys.argv[-1])
    except ValueError:
        length = 30
    model = build_word_model(sys.stdin)
    chain = markov(model, length)
    for item in chain:
        print item,
