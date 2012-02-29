import numpy
import os
import random
import cPickle as pickle

PROB_PATH = 'prob.pickle'

class Namegen(object):
    def __init__(self):
        if not os.path.exists(PROB_PATH):
            self.prob, self.sums = self.read_corpus('male.txt')
            self.save_arrays()
        else:
            self.prob, self.sums = self.load_arrays()

    def load_arrays(self):
        with open(PROB_PATH, 'r') as prob_file:
            return pickle.load(prob_file)

    def save_arrays(self):
        with open(PROB_PATH, 'wb') as prob_file:
            pickle.dump((self.prob, self.sums), prob_file, pickle.HIGHEST_PROTOCOL)

    def to_ordinal(self, c):
        return 0 if c == ' ' else ord(c.lower()) - 96

    def bi_to_ordinal(self, bi):
        return 27 * self.to_ordinal(bi[0]) + self.to_ordinal(bi[1])

    def from_ordinal(self, i):
        return ' ' if i == 0 else chr(i + 96)

    def read_corpus(self, path):
        with open(path, 'r') as file:
            return self.create_prob(file)

    def create_prob(self, file):
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
        name = '  '
        name += self.pick_char(name[-2:])
        while name[-1] != ' ':
            name += self.pick_char(name[-2:])
        return name.strip().capitalize()





if __name__ == '__main__':
    generator = Namegen()
    print(generator.generate())