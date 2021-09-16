import ast
from defaultFile import DefaultFile

class CacheFile:
    def __init__(self):
        self.file = None
        self.load()
    
    def load(self):
        
        try:
            self.file = open('natasha_cache.txt', 'r')
            self.cache_in = self.file.readlines()
            self.file.close()
            
        except:
            print("Open ~DataFile~ not working! -> Create a file by default")
            
            #creare fisier daca acesta nu exista
            self.cache_in = self.create_file()
        
        self.add(self.cache_in)
    
    def add(self, cache_in):
        dictionary_cc_in = []
        
        for i in self.cache_in:
            dictionary_cc_in.append(ast.literal_eval(i))
        
        self.dictionary_cache = dictionary_cc_in[0]
        
        if self.dictionary_cache[3]['PET'] == 1:
            self.index_dict_cache = 0
            #!!meniu prima varianta PET
            #variable_plastic.set(options_plastic[0])
        elif self.dictionary_cache[3]['HDPE'] == 1:
            self.index_dict_cache = 1
            
        elif self.dictionary_cache[3]['PP'] == 1:
            self.index_dict_cache = 2
            #!!meniu prima varianta PP
            
    def export_file(self, dictionary_cache):
        self.file = open('natasha_cache.txt', 'w')
        self.file.write(str(dictionary_cache))
        self.file.close()
    
    def create_file(self):
        self.file = open('natasha_cache.txt', 'w')
        dictionary_cache = DefaultFile.add_data()
        self.file.write(str(dictionary_cache))
        
        cache = self.file.readlines()
        self.file.close()
        
        return cache
    
test = CacheFile()

