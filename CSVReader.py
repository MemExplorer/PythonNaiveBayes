class csv_reader:
    
    def __init__(self, fpath):
        self.file_path = fpath
        self.__columnList = []
        self.__raw_data = {}

    def read(self):
        try:
            with open(self.file_path) as f:
                lines_content = f.readlines()

                #column names are always at first index
                for i in range(len(lines_content)):
                    split_data = lines_content[i].split(",")
                    for colIndex in range(len(split_data)):
                        current_row_data = split_data[colIndex].strip().lower()
                        if(i == 0):
                            self.__columnList.append(current_row_data)
                        else:
                            dict_key = self.__columnList[colIndex]

                            #initialize array if key doesn't exist in data list
                            if dict_key not in self.__raw_data:
                                self.__raw_data[dict_key] = []

                            self.__raw_data[dict_key].append(current_row_data)
        except:
            return False
        
        return True
    
    def get_col_names(self):
        return self.__columnList
                    
    def get_cell(self, col_name, index):
        return self.__raw_data[col_name][index]
    
    def get_row_data(self, col_name):
        return self.__raw_data[col_name]
    
    def get_row_length(self, col_name):
        return len(self.__raw_data[col_name])