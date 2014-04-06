#! /usr/bin/env python

class HomophoneType:
    def __init__(self, name):
        self.name = name
        self.training_samples = []
        self.sample_labels = []

class HomophoneErrorCorrection:
    def __init__(self):
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
