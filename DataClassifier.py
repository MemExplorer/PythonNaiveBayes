class classifier_base:
    def __init__(self, id):
        self.__str_id = id

    def get_str_id(self):
        return self.__str_id
    
    def classify_data(self, unique_col_names, data_list, result_data_list):
        raise "Unreachable"
    
    def get_classifier(self, input_data):
        raise "Unreachable"

#classifier for labeled data
class value_classifier(classifier_base):
    def __init__(self, id):
        super().__init__(id)

        #returns dictionary table with counted data
    def classify_data(self, unique_col_names, data_list, result_data_list):
        #initialze empty data table
        tmp_dict = {}
        for i in range(len(data_list)):
            if data_list[i] not in tmp_dict:
                tmp_dict[data_list[i]] = [0] * len(unique_col_names)
            current_col_index = unique_col_names.index(result_data_list[i])
            tmp_dict[data_list[i]][current_col_index] += 1

        return tmp_dict
    
    def get_classifier(self, input_data):
        return input_data

#classifier for unlabeled data
class unsupervised_data_classifier_base(classifier_base):

    def __init__(self, id):
        super().__init__(id)

    #returns dictionary table with counted data
    def classify_data(self, unique_col_names, data_list, result_data_list):
        type_list = self.get_classifier_type_list()

        #initialze empty data table
        tmp_dict = {}
        for t in type_list:
            tmp_dict[t] = [0] * len(unique_col_names)

        for i in range(len(data_list)):
            current_data_type = self.get_classifier(data_list[i])
            current_col_index = unique_col_names.index(result_data_list[i])
            tmp_dict[current_data_type][current_col_index] += 1

        return tmp_dict
    
    def get_classifier(self, input_data):
        raise "unreachable"

    def get_classifier_type_list(self):
        raise "unreachable"
    
class age_classifier(unsupervised_data_classifier_base):
    TEEN_YEARS = "ty"
    YOUNG_ADULT = "ya"
    MIDDLE_AGE = "ma"

    def __init__(self):
        super().__init__("age")
    
    def get_classifier(self, input_data):
        current_data = int(input_data)

        if current_data >= 12 and current_data <= 18:
            return age_classifier.TEEN_YEARS
        elif current_data >= 19 and current_data <= 40:
            return age_classifier.YOUNG_ADULT
        elif current_data >= 41 and current_data <= 65:
            return age_classifier.MIDDLE_AGE
        else:
            raise "Unreachable"

    def get_classifier_type_list(self):
        return [age_classifier.TEEN_YEARS, age_classifier.YOUNG_ADULT, age_classifier.MIDDLE_AGE]

class age_started_classifier(unsupervised_data_classifier_base):
    AT_YOUNG = "aty"
    AT_ADULT = "ata"

    def __init__(self):
        super().__init__("agestarted")

    def get_classifier(self, input_data):
        current_data = int(input_data)

        if current_data >= 12 and current_data <= 18:
            return age_started_classifier.AT_YOUNG
        elif current_data >= 19:
            return age_started_classifier.AT_ADULT
        else:
            raise "Unreachable"

    def get_classifier_type_list(self):
        return [age_started_classifier.AT_YOUNG, age_started_classifier.AT_ADULT]
        
class num_sticks_per_day_classifier(unsupervised_data_classifier_base):
    LIGHT_SMOKER = "l"
    MODERATE_SMOKER = "m"
    HEAVY_SMOKER = "h"

    def __init__(self):
        super().__init__("numberofsticksperday")

    def get_classifier(self, input_data):
        current_data = int(input_data)

        if current_data >= 1 and current_data <= 10:
            return num_sticks_per_day_classifier.LIGHT_SMOKER
        elif current_data >= 11 and current_data <= 19:
            return num_sticks_per_day_classifier.MODERATE_SMOKER
        elif current_data >= 20:
            return num_sticks_per_day_classifier.HEAVY_SMOKER
        else: 
            raise "Unreachable"

    def get_classifier_type_list(self):
        return [num_sticks_per_day_classifier.LIGHT_SMOKER, num_sticks_per_day_classifier.MODERATE_SMOKER,num_sticks_per_day_classifier.HEAVY_SMOKER]