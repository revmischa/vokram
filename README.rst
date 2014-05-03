======
Vokram
======

Vokram is a toy `Markov chain`_ library that is most likely implemented
incorrectly and extremely inefficiently.


Installation
============

Use `pip`_ to install::

    pip install vokram


Usage
=====

Command Line Usage
------------------

Pipe a body of text into ``vokram`` and it will generate some (hopefully)
plausible sentences synthesized from that body of text::

    $ cat the_art_of_war.txt | vokram
    Spies cannot be obtained inductively from experience, nor by any danger.

You can control the maximum number of words in the output and the n-gram size
used when building the Markov model. All command line options are given below::

    $ vokram --help

Outputs::

    usage: vokram [-h] [-w NUM_WORDS] [-n NGRAM_SIZE]

    Generates plausible new sentences from a corpus provided on STDIN.

    optional arguments:
      -h, --help            show this help message and exit
      -w NUM_WORDS, --num-words NUM_WORDS
                            Maximum number of words in the resulting sentence.
      -n NGRAM_SIZE, --ngram-size NGRAM_SIZE

Library Usage
-------------

Vokram can also be used as a plain old Python library::

    >>> import vokram
    >>> corpus = open('the_art_of_war.txt')
    >>> model = vokram.build_word_model(corpus, 2)
    >>> vokram.markov_words(model, 25))
    'Hence it is not supreme excellence; supreme excellence consists in breaking the enemy's few.'


Credits
=======

Vokram was made with inspiration from this simple and approachable
`Python implementation and explanation`_.

.. _Markov chain: http://en.wikipedia.org/wiki/Markov_chain
.. _Python implementation and explanation: http://code.activestate.com/recipes/194364-the-markov-chain-algorithm/
.. _pip: http://www.pip-installer.org/
