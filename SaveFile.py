import ast
from defaultFile import DefaultFile

class ImportFile:
    def __init__(self):
        self.file = None
        self.cache_values = []
        self.load()
    
    def load(self):
        
        try:
            file = open('natasha_cache.txt', 'r')
        except:
            """Open ~DataFile~ not working! -> Create a file by default"""

            CreateFile().create_file()
            file = open('natasha_cache.txt', 'r')
        
        try:
            cache_in = file.readlines()
            file.close()
            
            for i in cache_in:
                self.cache_values.append(ast.literal_eval(i))
            self.cache_values = self.cache_values[0]
        except:
            pass
    
    def add(self, indice):
        if indice == None: 
            return self.cache_values[0]
        
        return self.cahe_values[indice]
            
    def select_values(self):
        pass
        
    def export_file(self, idd, value):
        self.cache_values[0][idd] = value
        file = open('natasha_cache.txt', 'w')
        file.write(str(self.cache_values))
        file.close()
    
class CreateFile:
    def create_file(self):
        file = open('natasha_cache.txt', 'w')
        dictionary_cache = DefaultFile.add_data()
        file.write(str(dictionary_cache))
        file.close()
