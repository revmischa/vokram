import os
import pickle
import random
import sys
from collections import defaultdict


NONWORD = '\v'


def markov(model, word_count):
    """Generates a Markov chain based on the given model with the given word
    count."""
    chain = []
    key = random.choice(model.keys())
    for _ in xrange(word_count):
        word = random.choice(model[key])
        chain.append(word)
        key = key[1:] + (word,)
    return ' '.join(chain)

def build_model(corpus, n=2):
    """Builds a model of the given corpus using n-grams of size n. The model
    is a dict mapping n-gram keys to lists of words appearing after those
    n-grams."""
    model = defaultdict(list)
    # Start with a dummy key for the first word. After n iterations, the key
    # will contain all valid words from the corpus.
    key = tuple(NONWORD for _ in xrange(n))
    for word in gen_words(corpus):
        model[key].append(word)
        key = key[1:] + (word,)
    # Make sure the last key has an entry
    model[key].append(NONWORD)
    # Return normal dict, instead of a defaultdict object
    return dict(model)

def load_model(infile):
    return pickle.load(infile)

def save_model(model, outfile):
    pickle.dump(model, outfile)

def gen_words(corpus):
    """Yields each word from the given corpus, which can be either a string or
    a file-like object containing the words."""
    if isinstance(corpus, basestring):
        corpus = (line for line in corpus.splitlines())
    for line in corpus:
        for word in line.strip().split():
            yield word
