# python3
'''word similarity (sameness) from https://github.com/sujitpal/nltk-examples'''

from __future__ import division
from nltk.corpus import wordnet as wn
import sys

def similarity(w1, w2, sim=wn.path_similarity):
  synsets1 = wn.synsets(w1)
  synsets2 = wn.synsets(w2)
  sim_scores = []
  for synset1 in synsets1:
    for synset2 in synsets2:
      score = sim(synset1, synset2)
      if score:
        sim_scores.append(score)
  if len(sim_scores) == 0:
    return 0
  else:
    # print(sim_scores)
    return max(sim_scores)

def main():
  f = open(sys.argv[1], 'r')
  for line in f:
    word1, word2 = line.strip().split("\t")
    score = similarity(word1, word2)
    label = "same"
    if score < 1.0:
        label = "DIFF"
    print("%s:  %.3f  %s %s %s" % (label, score, word1, ' '*(14 - len(word1)), word2))
  f.close()

if __name__ == "__main__":
  main()
