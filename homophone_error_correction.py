#! /usr/bin/env python

class HomophoneType:
    def __init__(self, name):
        self.name = name
        self.training_samples = []
        self.sample_labels = []

class HomophoneErrorCorrection:
    def __init__(self):
        # initialize a dict of the various POS tags
        self.pos_tags = dict()
        self.pos_tag_counter = 0
        
        # initialize a set of homophone pairings
        self.homophone_types = []
        i = HomophoneType("it's vs its")
        self.homophone_types.append(i)
        y = HomophoneType("you're vs your")
        self.homophone_types.append(y)
        th = HomophoneType("they're vs their")
        self.homophone_types.append(th)
        l = HomophoneType("loose vs lose")
        self.homophone_types.append(l)
        to = HomophoneType("to vs too")
        self.homophone_types.append(to)
        
        # initialize a dict of the different homophones according
        # to their pairings
        self.homophones_by_type = dict()
        self.homophones_by_type["it's"] = 0
        self.homophones_by_type["its"] = 0
    
        self.homophones_by_type["you're"] = 1
        self.homophones_by_type["your"] = 1
    
        self.homophones_by_type["they're"] = 2
        self.homophones_by_type["their"] = 2
    
        self.homophones_by_type["loose"] = 3
        self.homophones_by_type["lose"] = 3

        self.homophones_by_type["to"] = 4
        self.homophones_by_type["too"] = 4
    
        # initialize a dict of the different homophones according
        # to their classification within a pairing
        self.homophones_by_class = dict()
        self.homophones_by_class["it's"] = 0
        self.homophones_by_class["its"] = 1
        
        self.homophones_by_class["you're"] = 0
        self.homophones_by_class["your"] = 1
        
        self.homophones_by_class["they're"] = 0
        self.homophones_by_class["their"] = 1
        
        self.homophones_by_class["loose"] = 0
        self.homophones_by_class["lose"] = 1
        
        self.homophones_by_class["to"] = 0
        self.homophones_by_class["too"] = 1

    # lookup the correct homophone
    def homophone_lookup(self, h_type, h_class):
        if h_type == 0:
            if h_class == 0:
                return "it's"
            else:
                return "its"
        elif h_type == 1:
            if h_class == 0:
                return "you're"
            else:
                return "your"
        elif h_type == 2:
            if h_class == 0:
                return "they're"
            else:
                return "their"
        elif h_type == 3:
            if h_class == 0:
                return "loose"
            else:
                return "lose"
        elif h_type == 4:
            if h_class == 0:
                return "to"
            else:
                return "too"

    # find the corresponding pair of homophones
    def find_homophone_type(self, word):
        if word in self.homophones_by_type:
            return self.homophones_by_type[word]
        else:
            return -1;

    # determine which homophone in the pair it is
    def find_homophone_class(self, word):
        if word in self.homophones_by_class:
            return self.homophones_by_class[word]
        else:
            return -1;
    
    # look up POS tags and return corresponding code
    def pos_tag_lookup(self, tag):
        if tag not in self.pos_tags:
            self.pos_tags[tag] = self.pos_tag_counter
            self.pos_tag_counter += 1

        return self.pos_tags[tag]


    # add a training example to the correct homophone type
    def add_training_example(self, h_type, h_class, features):
        self.homophone_types[h_type].training_samples.append(features)
        self.homophone_types[h_type].sample_labels.append(h_class)

    # write all the training data to a file
    def write_data_to_file(self, filename):
        with open(filename, 'w+') as outfile:
            outfile.write("pos_tags {}\n".format(len(self.pos_tags)))
            for tag in self.pos_tags:
                outfile.write("{0} {1}\n".format(tag, self.pos_tags[tag]))
            for homophone_type in self.homophone_types:
                outfile.write("{0} {1}\n".format(homophone_type.name, len(homophone_type.training_samples)))
                for sample in homophone_type.sample_labels:
                    outfile.write("{0}\n".format(sample))
                for sample in homophone_type.training_samples:
                    outfile.write("{0} {1} {2} {3}\n".format(sample[0], sample[1], sample[2], sample[3]))
