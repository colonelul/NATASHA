import ast

class CacheFile:
    def __init__(self):
        print("~~~~~Cache file~~~~~")
    
    def import_file(self, val_plastic):
        dictionary_cc_in = []
        self.index_dict_cache = 0
        
        self.input_file = open('natasha_cache.txt', 'r')
        self.cache_in = self.input_file.readlines()
        
        for i in self.cache_in:
            dictionary_cc_in.append(ast.literal_eval(i))
        
        self.dictionary_cache = dictionary_cc_in[0]
        self.input_file.close()
        
        if self.dictionary_cache[3]['PET'] == 1:
            self.index_dict_cache = 0
            #!!meniu prima varianta PET
            #variable_plastic.set(options_plastic[0])
        elif self.dictionary_cache[3]['HDPE'] == 1:
            self.index_dict_cache = 1
            
        elif self.dictionary_cache[3]['PP'] == 1:
            self.index_dict_cache = 2
            #!!meniu prima varianta PP
            
        # =============================================================================
        #     temp_out_1.insert(tk.END, dictionary_cache[index_dict_cache]['1'])
        #     temp_out_2.insert(tk.END, dictionary_cache[index_dict_cache]['2'])
        #     temp_out_3.insert(tk.END, dictionary_cache[index_dict_cache]['3'])
        #     temp_out_4.insert(tk.END, dictionary_cache[index_dict_cache]['4'])
        #     temp_out_5.insert(tk.END, dictionary_cache[index_dict_cache]['5'])
        #     temp_out_6.insert(tk.END, dictionary_cache[index_dict_cache]['6'])
        #     temp_out_7.insert(tk.END, dictionary_cache[index_dict_cache]['7'])
        #     temp_out_8.insert(tk.END, dictionary_cache[index_dict_cache]['8'])
        #     temp_out_9.insert(tk.END, dictionary_cache[index_dict_cache]['9'])
        #     temp_out_11.insert(tk.END, dictionary_cache[index_dict_cache]['11'])
        #     temp_out_12.insert(tk.END, dictionary_cache[index_dict_cache]['12'])
        #     temp_out_13.insert(tk.END, dictionary_cache[index_dict_cache]['13'])
        # =============================================================================
            
    def export_file(self, dictionary_cache):
        file = open('natasha_cache.txt', 'w')
        file.write(str(self.dictionary_cache))
        file.close()
        
        