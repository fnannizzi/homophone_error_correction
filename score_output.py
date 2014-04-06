#! /usr/bin/env python

from __future__ import division
import sys, nltk, homophone_error_correction

def score():
    with open("hw3/hw3.dev.err.txt") as wrong_file:
        wrong_raw_text = wrong_file.read()
        
    # tokenize the text into sentences
    sentence_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    wrong_raw_sentences = sentence_tokenizer.tokenize(wrong_raw_text)
    
    wrong_words = []
    for sentence in wrong_raw_sentences:
        s = sentence.replace('\n', ' ').replace('\r', ' ')
        # tokenize the sentence into words
        s = s.strip()
        wrong_raw_words = s.split(' ')
        
        
        # clean up the text some more before we add POS tags
        for w in wrong_raw_words:
            if w.isspace():
                continue
            
            w = w.lower()
            w = w.replace('.', '')
            w = w.replace('?', '')
            w = w.replace(',', '')
            w = w.replace(';', '')
            w = w.replace(':', '')
            w = w.replace('"', '')
            
            if not w:
                continue
            wrong_words.append(w)

    with open("hw3/hw3.dev.txt") as correct_file:
        correct_raw_text = correct_file.read()
        
    # tokenize the text into sentences
    sentence_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    correct_raw_sentences = sentence_tokenizer.tokenize(correct_raw_text)

    correct_words = []
    for sentence in correct_raw_sentences:
        s = sentence.replace('\n', ' ').replace('\r', ' ')
        # tokenize the sentence into words
        s = s.strip()
        correct_raw_words = s.split(' ')
        
                
        # clean up the text some more before we add POS tags
        for w in correct_raw_words:
            if w.isspace():
                continue
                    
            w = w.lower()
            w = w.replace('.', '')
            w = w.replace('?', '')
            w = w.replace(',', '')
            w = w.replace(';', '')
            w = w.replace(':', '')
            w = w.replace('"', '')
            
            if not w:
                continue
            correct_words.append(w)


    with open("output.txt") as output_file:
        output_raw_text = output_file.read()

    # tokenize the text into sentences
    sentence_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    output_raw_sentences = sentence_tokenizer.tokenize(output_raw_text)

    output_words = []
    for sentence in output_raw_sentences:
        s = sentence.replace('\n', ' ').replace('\r', ' ')
        # tokenize the sentence into words
        s = s.strip()
        output_raw_words = s.split(' ')
        
        
        # clean up the text some more before we add POS tags
        for w in output_raw_words:
            if w.isspace():
                continue
            
            w = w.lower()
            w = w.replace('.', '')
            w = w.replace('?', '')
            w = w.replace(',', '')
            w = w.replace(';', '')
            w = w.replace(':', '')
            w = w.replace('"', '')
            
            if not w:
                continue
            output_words.append(w)


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

    print "Precision: {0} Recall: {1}".format(precision, recall)


score()