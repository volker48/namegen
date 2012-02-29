#!/usr/bin/env python
import numpy
import os
import random
import cPickle as pickle
import argparse

class Namegen(object):
    PROB_PATH = 'prob.pickle'

    def __init__(self, corpus='male.txt'):
        if not os.path.exists(Namegen.PROB_PATH):
            self.prob, self.sums = self.read_corpus(corpus)
            self.save_arrays()
        else:
            self.prob, self.sums = self.load_arrays()

    def load_arrays(self):
        """
        Loads the numpy array from the pickled file on disk
        """
        with open(Namegen.PROB_PATH, 'rb') as prob_file:
            return pickle.load(prob_file)

    def save_arrays(self):
        """
        Pickles the numpy array to disk
        """
        with open(Namegen.PROB_PATH, 'wb') as prob_file:
            pickle.dump((self.prob, self.sums), prob_file, pickle.HIGHEST_PROTOCOL)

    def to_ordinal(self, c):
        """
        Converts the char c to its appropriate index in numpy array.
        """
        return 0 if c == ' ' else ord(c.lower()) - 96

    def bi_to_ordinal(self, bi):
        """
        Converts the string bi to the proper row index in the numpy array.
        """
        return 27 * self.to_ordinal(bi[0]) + self.to_ordinal(bi[1])

    def from_ordinal(self, i):
        return ' ' if i == 0 else chr(i + 96)

    def read_corpus(self, path):
        with open(path, 'r') as file:
            return self.create_prob(file)

    def create_prob(self, file):
        """
        Creates the numpy array that holds the number of occurrences of the
        bigrams.
        """
        prob = numpy.zeros((729, 27), dtype=numpy.int16)
        for line in file:
            line = line.rstrip()
            if not line.isalpha():
                continue
            #two in the front one in the back
            line = '  ' + line + ' '
            for i in xrange(2, len(line)):
                prev =self.bi_to_ordinal(line[i - 2:i])
                cur = self.to_ordinal(line[i])
                prob[prev, cur] += 1
        return prob, numpy.sum(prob, axis=1)

    def pick_char(self, previous):
        """
        Picks the next character given the previous bigram.
        """
        ordinal = self.bi_to_ordinal(previous)
        total = self.sums[ordinal]
        if not total:
            return ' '
        val = random.randint(0, total - 1)
        i = 0
        while val >= self.prob[ordinal, i]:
            val -= self.prob[ordinal, i]
            i += 1
        return self.from_ordinal(i)


    def generate(self):
        """
        Generates a random name.
        """
        name = '  '
        while True:
            name += self.pick_char(name[-2:])
            if name[-1] == ' ':
                return name.strip().capitalize()

    def generate_clean(self):
        """
        Generates a random name with length between 4 and 8.
        """
        while True:
            name = self.generate()
            if 4 <= len(name) <= 8:
                return name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Namegen: Random name generator.')
    parser.add_argument('-n', dest='count', type=int, default=1, help='The number of names to generate')
    args = parser.parse_args()
    generator = Namegen()
    for i in xrange(args.count):
        print(generator.generate_clean())
