from NaiveBayesClassifier import naive_bayes_classifier
import msvcrt

def main():

    p = input("Enter CSV Path: ").replace('"', "").replace("'", "")
    predictor = naive_bayes_classifier()

    #Perform computations to get frequency data
    if not(predictor.train_from_csv(p)):
        print("Failed to train data! Please check your data!")
        return

    #ask user to input stuff
    data_fields_info = predictor.get_data_fields_info()

    u_input = []
    for d in data_fields_info:

        #sort options first
        options = d[1]
        options.sort()

        #display options
        print("Enter " + d[0] + " -> ")
        input_range = range(1, len(options) + 1)
        for o in input_range:
            print(str(o) + " - " + options[o - 1])
        print()

        curr_input = ""
        while(True):
            print("Option: ", end="")
            curr_input = msvcrt.getch()
            print(curr_input.decode("utf-8"))

            #simple input validation
            if curr_input.isdigit() and int(curr_input) in input_range:
                break
        u_input.append(options[int(curr_input) - 1])

    #do some little magic
    prediction_value = predictor.predict(u_input)
    print("\nPrediction: " + prediction_value)

main()
