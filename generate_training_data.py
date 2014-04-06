#! /usr/bin/env python

from __future__ import division
import sys, os, nltk, homophone_error_correction

# move all the texts into one big file
def consolidate_text():
    
    with open("raw_training_data.txt", 'w+') as outfile:
        
        for file in os.listdir("texts"):
            if file.endswith(".txt"):
                with open("texts/" + file) as infile:
                    for line in infile:
                        outfile.write(line)


# clean up the text for processing
# format into training samples
def format_for_training():
    hec = homophone_error_correction.HomophoneErrorCorrection()
    
    with open("raw_training_data.txt") as textfile:
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
        #print pos_tagged_words
        
        len_words = len(words)

        for index, w in enumerate(words):
            # check to see if word is one of the homophones we're searching for
            h_type = hec.find_homophone_type(w)
            if  h_type != -1:
                # the current word is one of the types of homophones we're looking for
                # determine the class of the homophone (within its type)
                h_class = hec.find_homophone_class(w)
                #print "Word: {0} h_type: {1} h_class: {2}".format(w, h_type, h_class)

                # find the features for this training example
                features = []
                # find the 2-preceding tag
                if index > 1:
                    pre_pre_tag = pos_tagged_words[index - 2][1]
                else:
                    pre_pre_tag = "null_tag"
                # find the preceding tag
                if index > 0:
                    pre_tag = pos_tagged_words[index - 1][1]
                else:
                    pre_tag = "null_tag"
                # find the succeeding tag
                if index < (len_words - 2):
                    post_post_tag = pos_tagged_words[index + 2][1]
                else:
                    post_post_tag = "null_tag"
                # find the 2-succeeding tag
                if index < (len_words - 1):
                    post_tag = pos_tagged_words[index + 1][1]
                else:
                    post_tag = "null_tag"
                
                features.append(hec.pos_tag_lookup(pre_pre_tag))
                features.append(hec.pos_tag_lookup(pre_tag))
                features.append(hec.pos_tag_lookup(post_tag))
                features.append(hec.pos_tag_lookup(post_post_tag))

                #print features

                # add the training example to the corresponding set of training examples
                hec.add_training_example(h_type, h_class, features)


    # write the training data to a file
    hec.write_data_to_file("training_data.txt")


consolidate_text()
format_for_training()