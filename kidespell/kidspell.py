import pandas as pd
import stringdist #pip install StringDist
import numpy as np
import re

class KidSpell(object):
  def __init__(self, dictionary_path):
    self.ks_vocab = {}
    with open(dictionary_path) as f:
      for line in f:
        (key, val) = line.split()
        self.ks_vocab[key] = val
    self.rules = [
      (r'[^A-zÀ-ú]', r''),  #remove non-letters
      #EXEPTIONS
      (r'^ce$', r'KE'), #CE -> KE
      #PRIMARY RULES
      (r'[á]', r'aa'), #á -> aa
      (r'[é]', r'ee'), #é -> ee
      (r'[í]', r'ii'), #í -> ii
      (r'[ó]', r'oo'), #ó -> oo
      (r'[ú]', r'uu'), #ú -> uu
      (r'x', r'KS'), #x -> KS
      (r'w', r'W'), #w -> GU
      (r't?ch',r'0'), #ch or tch to CH - CH sound represented as 0
      (r'ce', r'SE'), #ce -> SE
      (r'ci', r'SI'), #ci -> SI
      (r'[c]', r'K'), #other c's -> K
      (r'qu', r'K'), #qu -> k
      (r'ci', r'SI'), #ci -> SI
      (r'r+', r'R'), #remove extra r
      (r'z', r'S'), # z -> S
      (r'y', r'LL'), # y -> ll
      (r'v', r'B'), # v -> B
      (r'h', r''), # h -> silent
    ]
    self.phonetic_dict = {}
    for word in self.ks_vocab:
        word = str(word).lower()
        try:
            word_phone = self.pkey(word)
        except:
            continue
        if word_phone in self.phonetic_dict:
            self.phonetic_dict[word_phone].append(word)
        else:
            self.phonetic_dict[word_phone] = [word]

  #Returns phonetic key for a word
  def pkey(self,word):
    code = word.lower()
    for rule in self.rules:
        code = re.sub(rule[0], rule[1], code)
    return code.upper()

  #Generates phonetic key of edit distance 1
  def edit_distance_1(self,word):
    word = word.lower()
    letters = list('abdefgijklmnñopqrstuyz')
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(transposes + deletes + replaces + inserts)  

  #Returns spelling suggestions for the given word
  #The amount of spelling suggestions is up to the given count
  def suggestions(self, word, count=5):
    spelling_phone = self.pkey(word)
    suggestions = []
    #Primary Keys
    if spelling_phone in self.phonetic_dict:
        suggestions.extend(self.phonetic_dict[spelling_phone]) 

    #Supplementary Keys
    if len(suggestions) < count:
        additional_suggestions = []
        for eword in self.edit_distance_1(spelling_phone):
            if eword.upper() in self.phonetic_dict:
                additional_suggestions.extend(self.phonetic_dict[eword.upper()])
        additional_suggestions.sort(key=lambda x: stringdist.levenshtein_norm(x, word))
        suggestions.extend(additional_suggestions)

    suggestions = [sug[0].upper() + sug[1:] if word[0].upper() == word[0] else sug for sug in list(dict.fromkeys(suggestions)) if len(sug) > 1]
    return suggestions[:count]


  def isInVocab(self,word):
    return word.upper() in self.ks_vocab

  def getErrors(self,sentence):
    return [word for word in sentence.split() if word.upper() not in self.ks_vocab]

  def getSuggestionsForSentence(self,sentence, max=5):
    return {word:self.suggestions(word, max) for word in sentence.split() if word.upper() not in self.ks_vocab}