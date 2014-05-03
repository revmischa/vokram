from __future__ import print_function

import argparse
import sys

from .vokram import build_word_model, markov_words


DEFAULT_NGRAM_SIZE = 2
MIN_SENTENCE_LENGTH = 5


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='vokram',
        description='Generates plausible new sentences from a corpus provided '
                    'on STDIN.')
    arg_parser.add_argument(
        '-w', '--num-words', type=int, default=30,
        help='Maximum number of words in the resulting sentence.')
    arg_parser.add_argument(
        '-n', '--ngram-size', type=int, default=DEFAULT_NGRAM_SIZE)

    args = arg_parser.parse_args()

    # One way to check whether anything has been piped into STDIN, though I'm
    # not sure how reliable this is.
    if sys.stdin.isatty():
        print('Error: corpus must be provided on STDIN.', file=sys.stderr)
        sys.exit(1)

    model = build_word_model(sys.stdin, n=args.ngram_size)
    try:
        print(markov_words(model, args.num_words))
    except RuntimeError as e:
        msg = ('Error: Could not generate sentence with at least %d words.' %
               MIN_SENTENCE_LENGTH)
        print(msg, file=sys.stderr)
        sys.exit(1)
