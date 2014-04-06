#! /usr/bin/env python

from __future__ import division
import sys, nltk, homophone_error_correction

def process_text(filename):
    with open(filename) as file:
        raw_text = file.read()
    
    # tokenize the text into sentences
    sentence_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    raw_sentences = sentence_tokenizer.tokenize(raw_text)
    
    words = []
    for sentence in raw_sentences:
        s = sentence.replace('\n', ' ').replace('\r', ' ')
        # tokenize the sentence into words
        s = s.strip()
        raw_words = s.split(' ')
        
        # clean up the text some more
        for w in raw_words:
            if w.isspace() or not w:
                continue
            
            w = w.lower()
            words.append(w)
    
    return words

def score():
    
    wrong_words = process_text("hw3/hw3.dev.err.txt")
    correct_words = process_text("hw3/hw3.dev.txt")
    output_words = process_text("output.txt")

    if len(wrong_words) != len(correct_words):
        print "1 - Uh oh, lengths are {0} and {1}...".format(len(wrong_words),len(correct_words))

    if len(wrong_words) != len(output_words):
        print "2 - Uh oh, lengths are {0} and {1}...".format(len(wrong_words),len(output_words))

    corrections = []
    for index,word in enumerate(wrong_words):
        if word != correct_words[index]:
            corrections.append(index)


    print "Num corrections: {0}".format(len(corrections))

    mods_needed = len(corrections) # A
    correct_mods = 0 # (A intersection B)
    total_mods = 0 # B

    for index,word in enumerate(output_words):
        if word != wrong_words[index]:
            total_mods += 1
        
            if word == correct_words[index]:
                correct_mods += 1

    precision = correct_mods/total_mods
    recall = correct_mods/mods_needed
    fscore = (2 * precision * recall)/(precision + recall)

    print "Precision: {0} Recall: {1}".format(precision, recall)
    print "F-score: {0}".format(fscore)

score()