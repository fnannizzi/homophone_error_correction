#! /usr/bin/env python

from __future__ import division
import sys, os, nltk, re, pprint, homophone_error_correction

# move all the texts into one big file
def consolidate_text():
    
    with open("training_data.txt", 'w+') as outfile:
        
        for file in os.listdir("texts"):
            if file.endswith(".txt"):
                with open("texts/" + file) as infile:
                    for line in infile:
                        outfile.write(line)


# clean up the text for processing
def tokenize():
    hec = homophone_error_correction.HomophoneErrorCorrection()
    
    with open("training_data.txt") as textfile:
        raw_text = textfile.read().replace('\n', ' ').replace('\r', ' ')
        
    # tokenize the text into sentences
    sentence_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    sentences = sentence_tokenizer.tokenize(raw_text)

    for s in sentences:
        # tokenize the sentence into words
        raw_words = s.split(' ')
        words = []
        
        # clean up the text some more before we add POS tags
        for w in raw_words:
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
            words.append(w)
        
        # add POS tags to the words
        pos_tagged_words = nltk.pos_tag(words)
        print pos_tagged_words
        for w in words:
            # check to see if word is one of the homophones we're searching for
            h_type = hec.find_homophone_type(w)
            if  h_type != -1:
                # the current word is one of the types of homophones we're looking for
                # determine the class of the homophone (within its type)
                h_class = hec.find_homophone_class(w)
                print "Word: {0} h_type: {1} h_class: {2}".format(w, h_type, h_class)





# format into training samples
def format_for_training():
    training_samples = [] # contains training samples with features
    training_labels = [] # contains labels corresponding to training samples








#consolidate_text()
tokenize()