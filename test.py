"""
This class is for testing and verifying the code I have written
"""

from DataClassifier import age_classifier, age_started_classifier, num_sticks_per_day_classifier, value_classifier
from NaiveBayesClassifier import naive_bayes_classifier
from CSVReader import csv_reader

def test_normal():

    #csv input path
    p = "SmokingDataSet (1).csv"
    csvReader = csv_reader(p)
    if csvReader.read():
        #test input data
        list_input = []
        for i in range(csvReader.get_row_length("age")):
            data_list = []
            for c in csvReader.get_col_names():
                data_list.append(csvReader.get_cell(c, i))
            list_input.append(data_list)
        
        #predictor = naive_bayes_classifier("yes")
        predictor = naive_bayes_classifier()
        predictor.train_from_csv(p)

        inacc = 0
        for i in list_input:
            ret = predictor.predict(i)
            if ret != i[-1]:
                inacc += 1
            print(str(list_input.index(i)) + ": " + ret + ' - ' + i[-1])
            
        print("Mistakes count: " + str(inacc))
        print("Prediction Accuracy: " + f"{(((len(list_input) - inacc)/ len(list_input)) * 100):.2f}" + "%")

def test_bing_chilling():
    p = "SmokingDataSet (1).csv"
    
    csvReader = csv_reader(p)
    if csvReader.read():
        #test input data
        list_input = []
        for i in range(csvReader.get_row_length("age")):
            data_list = []
            for c in csvReader.get_col_names():
                data_list.append(csvReader.get_cell(c, i))
            list_input.append(data_list)

        #ordered classifier (improve by labeling data??)
        classifier_list = [age_classifier(), value_classifier("gender"), value_classifier("civilstatus"), value_classifier("hasinfoaboutcessation"),
                        value_classifier("employmentstatus"), value_classifier("type"), age_started_classifier(), value_classifier("influence"), 
                        value_classifier("urge"), num_sticks_per_day_classifier(), value_classifier("mainaccess")]
        
        predictor = naive_bayes_classifier()
        predictor.train_from_csv(p, classifier_list)

        inacc = 0
        for i in list_input:
            predictor.transform_input(i, classifier_list)
            ret = predictor.predict(i)
            if ret != i[-1]:
                inacc += 1
            print(str(list_input.index(i)) + ": " + ret + ' - ' + i[-1])
        
        print("Mistakes count: " + str(inacc))
        print("Prediction Accuracy: " + f"{(((len(list_input) - inacc)/ len(list_input)) * 100):.2f}" + "%")


test_bing_chilling()
test_normal()