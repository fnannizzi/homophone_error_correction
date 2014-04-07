#! /usr/bin/env python

from __future__ import division
from sklearn import svm
import sys, nltk, homophone_error_correction, time

def learn():

    # record the starting time for entire execution
    t0 = time.time()
    
    if len(sys.argv) < 3:
        print "Not enough arguments, need a test filename and a output filename. Quitting..."
        return
    
    test_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    hec = homophone_error_correction.HomophoneErrorCorrection()
    classifiers = []

    print "Loading up the training data..."
    with open("training_data.txt") as f:
        # read the number of POS tags
        line = f.readline()
        tokens = line.split(' ')
        num_tags = int(tokens[1])
        # read in the POS tags and correspoding codes
        for tag_index in range(0, num_tags):
            line = f.readline()
            tokens = line.split(' ')
            hec.pos_tags[tokens[0]] = int(tokens[1])
        # read in each set of training examples (1 per homophone pair)
        for type_index in range(0,5):
            line = f.readline()
            tokens = line.split(' ')
            num_samples = int(tokens[3])
            # read in sample labels
            for sample_index in range(0, num_samples):
                line = f.readline()
                tokens = line.split(' ')
                hec.homophone_types[type_index].sample_labels.append(int(tokens[0]))
            # read in sample features
            for sample_index in range(0, num_samples):
                line = f.readline()
                tokens = line.split(' ')
                features = [int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])]
                hec.homophone_types[type_index].training_samples.append(features)

    print "Training the classifiers..."
    # create and train our svm classifiers
    for homophone_type in hec.homophone_types:
        # make an instance of a support vector classifier with a linear kernel function
        classifier = svm.SVC(kernel='linear')
        # fit the classifier to the training data
        classifier.fit(homophone_type.training_samples, homophone_type.sample_labels)
        # add the classifier to a list of classifiers
        classifiers.append(classifier)

    print "Reading test data..."
    # Get the raw input text
    with open(test_filename) as testfile:
        raw_text = testfile.read()
    # raw_text_index is used to match the processed text with the raw text
    raw_text_index = 0

    print "Tokenizing input text..."
    # tokenize the text into sentences
    sentence_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    raw_sentences = sentence_tokenizer.tokenize(raw_text)

    print "Beginning correction on input..."
    # record the starting time for correction
    t1 = time.time()
    
    with open(output_filename, 'w+') as outfile:
        for index,sentence in enumerate(raw_sentences):
            # clean and break the sentence into words for POS tagging
            s = sentence.replace('\n', ' ').replace('\r', ' ')
            s = s.strip()
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
            len_words = len(words)

            for index, w in enumerate(words):
                while(raw_text[raw_text_index].lower() != w[0]):
                    raw_text_index += 1
                
                # check to see if word is one of the homophones we're searching for
                h_type = hec.find_homophone_type(w)
                if  h_type != -1:
                    # the current word is one of the types of homophones we're looking for
                    # determine the class of the homophone (within its type)
                    h_class = hec.find_homophone_class(w)
                
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
                    if index < (len_words - 1):
                        post_tag = pos_tagged_words[index + 1][1]
                    else:
                        post_tag = "null_tag"
                    # find the 2-succeeding tag
                    if index < (len_words - 2):
                        post_post_tag = pos_tagged_words[index + 2][1]
                    else:
                        post_post_tag = "null_tag"
                
                    # create the feature vector
                    features = [hec.pos_tag_lookup(pre_pre_tag), hec.pos_tag_lookup(pre_tag), hec.pos_tag_lookup(post_tag), hec.pos_tag_lookup(post_post_tag)]

                    # predict the correct homophone word
                    classification = classifiers[h_type].predict(features)
                    # if the prediction doesn't match the word, we need to make a correction
                    if classification != h_class:
                        correction = hec.homophone_lookup(h_type, classification)
                        # need to split the text around the incorrect word and
                        # rebuild the text around the correct word
                        raw_text_half1 = raw_text[:raw_text_index]
                        raw_text_half2 = raw_text[(raw_text_index + len(w)):]
                        raw_text = raw_text_half1 + correction + raw_text_half2
                        # increment the raw_text_index past the word we just examined
                        raw_text_index += len(correction)
                    else:
                        # increment the raw_text_index past the word we just examined
                        raw_text_index += len(w)
                else:
                    # increment the raw_text_index past the word we just examined
                    raw_text_index += len(w)

        # record the time after correction has completed
        t2 = time.time()
        # write the corrected text to a file
        outfile.write(raw_text)

        total_time = t2-t0
        correction_time = t2-t1
        print " "
        print "Execution took {0} minutes".format(total_time/60)
        print "Correction took {0} minutes.".format(correction_time/60)


learn()