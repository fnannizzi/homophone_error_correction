#! /usr/bin/env python

from __future__ import division
from sklearn import svm
import sys, nltk, homophone_error_correction

def learn():
    
    hec = homophone_error_correction.HomophoneErrorCorrection()
    classifiers = []
    
    with open("training_data.txt") as f:
        line = f.readline()
        tokens = line.split(' ')
        num_tags = int(tokens[1])
        for tag_index in range(0, num_tags):
            line = f.readline()
            tokens = line.split(' ')
            hec.pos_tags[tokens[0]] = int(tokens[1])
        for type_index in range(0,5):
            line = f.readline()
            tokens = line.split(' ')
            num_samples = int(tokens[3])
            for sample_index in range(0, num_samples):
                line = f.readline()
                tokens = line.split(' ')
                hec.homophone_types[type_index].sample_labels.append(int(tokens[0]))
            for sample_index in range(0, num_samples):
                line = f.readline()
                tokens = line.split(' ')
                features = []
                features.append(tokens[0])
                features.append(tokens[1])
                features.append(tokens[2])
                features.append(tokens[3])
                hec.homophone_types[type_index].training_samples.append(features)

    print "Training the classifiers..."
    # create and train our svm classifiers
    for homophone_type in hec.homophone_types:
        # make an instance of a support vector classifier
        classifier = svm.SVC()
        # fit the classifier to the training data
        classifier.fit(homophone_type.training_samples, homophone_type.sample_labels)
        # add the classifier to a list of classifiers
        classifiers.append(classifier)

    print "Reading test data..."
    with open("test_data.txt") as testfile:
        raw_text = testfile.read()

    # tokenize the text into sentences
    sentence_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    raw_sentences = sentence_tokenizer.tokenize(raw_text)

    with open("output.txt", 'w+') as outfile:
        for sentence in raw_sentences:
            s = sentence.replace('\n', ' ').replace('\r', ' ')
            # tokenize the sentence into words
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
            print s
            print "Len raw text: {0} len clean text: {1}".format(len(raw_words), len(words))
            len_words = len(words)

            for index, w in enumerate(words):
                # check to see if word is one of the homophones we're searching for
                h_type = hec.find_homophone_type(w)
                if  h_type != -1:
                    # the current word is one of the types of homophones we're looking for
                    # determine the class of the homophone (within its type)
                    h_class = hec.find_homophone_class(w)
                    print "Word: {0} h_type: {1} h_class: {2}".format(w, h_type, h_class)
                
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

                    classification = classifiers[h_type].predict(features)
                    if classification != h_class:
                        print "Found correction!"
                        correction = hec.homophone_lookup(h_type, classification)
                        raw_words[index] = correction
                        print "Corrected text: ", raw_words


            for w in raw_words:
                outfile.write("{0} ".format(w))






learn()