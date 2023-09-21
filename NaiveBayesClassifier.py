from CSVReader import csv_reader
from DataClassifier import value_classifier

class naive_bayes_classifier:

    def __init__(self):
        self.__data_frequency = {}
        self.__result_row = []
        self.__unique_values = () #unique value names
        self.__has_frequency = False
    
    def get_data_fields_info(self):
        #check if there's frequency data
        self.__check_frequency_data()

        return [(i, list(self.__data_frequency[i])) for i in self.__data_frequency]

    def transform_input(self, input, classifier_list):
        #check if there's frequency data
        self.__check_frequency_data()

        for i in range(len(classifier_list)):
            input[i] = classifier_list[i].get_classifier(input[i])
    
    def train_from_csv(self, data_path, classifier_list = None):
        csv_data = csv_reader(data_path)
        if csv_data.read():
            #initialize classifiers
            col_list = csv_data.get_col_names()
            self.bool_name = col_list[-1]
            self.__result_row = csv_data.get_row_data(self.bool_name)
            self.__unique_values = tuple(set(self.__result_row))

            #check if we have our own data transformer
            if classifier_list == None:
                classifier_list = []

                #exclude last element because last column and its data are the values we depend on
                for c_name in col_list[:-1]:
                    classifier_list.append(value_classifier(c_name))

            #identify and process each data
            for classifier in classifier_list:
                sid = classifier.get_str_id()
                processed_data = self.__process_row(csv_data, classifier)
                self.__data_frequency[sid] = processed_data
            
            #print data to verify if the data frequenct is correct
            #print("Frequency: \n" + str(self.__data_frequency) + "\n")

            #set this to true to allow prediction
            self.__has_frequency = True

            return True

        return False
    
    def predict(self, input_arr):
        
        #check if there's frequency data
        self.__check_frequency_data()

        #check if smoothing is needed
        need_smoothing = self.__do_we_need_smoothing(input_arr)

        #initialize array for storing computations
        posterior_probability_result = [0] * len(self.__unique_values)
        proportional_probability_result = [0] * len(self.__unique_values)

        #compute the posterior probability first cuz we will need the sum of these values later
        for n in range(len(self.__unique_values)):
            posterior_probability_result[n] = self.__compute(input_arr, n, need_smoothing)

        #do the epic proportional probability computation to find out who has the highest percentage
        for n in range(len(posterior_probability_result)):
            proportional_probability_result[n] = posterior_probability_result[n] / sum(posterior_probability_result)

        #get item with highest percentage
        highest_percentage = max(proportional_probability_result)
        h_index = proportional_probability_result.index(highest_percentage)

        #return prediction
        return self.__unique_values[h_index]

    def __check_frequency_data(self):
        #check if we have frequency data
        if(not(self.__has_frequency)):
            raise "Failed to do prediction! Please check your data!"

    def __process_row(self, csv_data, classifier):
        #classify data
        curr_row = csv_data.get_row_data(classifier.get_str_id())
        classified_data = classifier.classify_data(self.__unique_values, curr_row, self.__result_row)
        return classified_data

    def __perform_laplace_smoothing(self, num, den, alpha, k_value):
        return (num + alpha) / (den + alpha * k_value)
    
    def __perform_normal_computation(self, num, den, alpha, k_value):
        return num / den

    def __perform_jelinek_mercer_smoothing(self, num, den, alpha, k_value):
        background_prob = self.__perform_normal_computation(num, den, 0, 0)
        return (1 - alpha) * num + alpha * background_prob
    
    def __perform_dirichlet_smoothing(self, num, den, alpha, k_value):
        background_prob = self.__perform_normal_computation(num, den, 0, 0)
        likelihood = (num + alpha * background_prob) / (den + alpha)
        return likelihood


    def __compute(self, input_arr, item_index, need_smoothing):
        entry_count = len(self.__result_row)
        occurence_count = self.__result_row.count(self.__unique_values[item_index])
        compute_op = self.__perform_laplace_smoothing if need_smoothing else self.__perform_normal_computation

        #denominator computation
        denominator = 1
        col_list = list(self.__data_frequency)
        alpha = 0.1 #constant value???
        k_value = len(col_list)
        for cd_index in range(len(self.__data_frequency)):
            input_key = input_arr[cd_index]
            col_name = col_list[cd_index]
            current_iter_data = self.__data_frequency[col_name][input_key]
            denominator *= compute_op(sum(current_iter_data), entry_count, alpha, k_value)

        #numerator computation
        numerator = 1
        for cd_index in range(len(self.__data_frequency)):
            input_key = input_arr[cd_index]
            col_name = col_list[cd_index]
            current_iter_data = self.__data_frequency[col_name][input_key]
            numerator *= compute_op(current_iter_data[item_index], occurence_count, alpha, k_value) 

        numerator *= compute_op(occurence_count, entry_count, alpha, k_value)
        return numerator / denominator
        

    #check whether smoothing is necessary
    def __do_we_need_smoothing(self, input_arr):
        col_list = list(self.__data_frequency)
        for cd_index in range(len(self.__data_frequency)):
            input_key = input_arr[cd_index]
            col_name = col_list[cd_index]
            current_iter_data = self.__data_frequency[col_name][input_key]
            has_zero = any(i == 0 for i in current_iter_data) # check if any of the values are 0
            if(has_zero):
                return True
            
        return False