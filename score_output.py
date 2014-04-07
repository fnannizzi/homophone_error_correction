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
    
    if len(sys.argv) < 4:
        print "Not enough arguments, need a filename for text before correction, a filename for text after correction, and an output filename. Quitting..."
        return
        
    wrong_filename = sys.argv[1]
    correct_filename = sys.argv[2]
    output_filename = sys.argv[3]
    
    # process all the text
    wrong_words = process_text(wrong_filename)
    correct_words = process_text(correct_filename)
    output_words = process_text(output_filename)

    # check to make sure that the lengths of the texts line up
    # if they don't it means I messed up
    if len(wrong_words) != len(correct_words):
        print "Uh oh, lengths of text are mismatched. len_incorrect:{0} len_correct:{1}...".format(len(wrong_words),len(correct_words))

    if len(wrong_words) != len(output_words):
        print "Uh oh, lengths of text are mismatched. len_incorrect:{0} len_output:{1}...".format(len(wrong_words),len(output_words))

    # count the number of corrections that needed to be made
    corrections = []
    for index,word in enumerate(wrong_words):
        if word != correct_words[index]:
            corrections.append(index)

    print "Num corrections: {0}".format(len(corrections))

    mods_needed = len(corrections) # A
    correct_mods = 0 # (A intersection B)
    total_mods = 0 # B

    # count the number of modifications made
    for index,word in enumerate(output_words):
        if word != wrong_words[index]:
            total_mods += 1
        
            if word == correct_words[index]:
                correct_mods += 1

    # calculate the scores
    precision = correct_mods/total_mods
    recall = correct_mods/mods_needed
    fscore = (2 * precision * recall)/(precision + recall)

    print "Precision: {0} Recall: {1}".format(precision, recall)
    print "F-score: {0}".format(fscore)

score()