import numpy
import os
import random
import cPickle as pickle

PROB_PATH = 'prob.pickle'

class Generator(object):
    def __init__(self):
        home = os.path.expanduser("~")
        file_path = os.path.join(home, "nltk_data", "corpora", "names", "male.txt")
        if not os.path.exists(PROB_PATH):
            self.prob, self.sums = self.read_corpus(file_path)
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

    def from_ordinal(self, i):
        return ' ' if i == 0 else chr(i + 96)

    def read_corpus(self, path):
        with open(path, 'r') as file:
            return self.create_prob(file)

    def create_prob(self, file):
        prob = numpy.zeros((27,27), dtype=numpy.int16)
        for line in file:
            line = line.rstrip()
            if not line.isalpha():
                continue
            for i in xrange(len(line)):
                prev = self.to_ordinal(line[i - 1]) if i > 0 else 0
                cur = self.to_ordinal(line[i])
                prob[prev, cur] += 1
                if i == len(line) - 1:
                    prob[cur, 0] += 1
        return prob, numpy.sum(prob, axis=0)

    def pick_char(self, previous):
        ordinal = self.to_ordinal(previous)
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
        name = ''
        current = ' '
        current = self.pick_char(current)
        name += current
        while current != ' ':
            current = self.pick_char(current)
            name += current
        return name.capitalize()





if __name__ == '__main__':
    generator = Generator()
    print(generator.generate())