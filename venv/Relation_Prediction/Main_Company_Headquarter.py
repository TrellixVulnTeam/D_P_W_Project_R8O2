import warnings

warnings.filterwarnings(action="ignore", category=UserWarning, module='gensim')
import random
import gensim, re
import numpy as np
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('Happy_Das', 'gqFHrnV4u2yQkUdckBtD')

f2 = open("../Results/Company_Headquarter/Company_headquarter.txt", "w+", encoding="utf-8")
f3 = open("../Results/Company_Headquarter/Company_headquarter_Final.txt", "w+", encoding="utf-8")
f4 = open("../Results/Company_Headquarter/Company_headquarter_Accuracy.txt", "w+", encoding="utf-8")
f5 = open("../Results/Company_Headquarter/Company_headquarter_Average_Accuracy.txt", "w+", encoding="utf-8")
vec = gensim.models.KeyedVectors.load_word2vec_format(
    'D:/dl4j-files/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin', binary=True)
train  = open("../Data/Company_Headquarter/Company_headquarter_Train.txt", 'r', encoding="utf-8")
test = open("../Data/Company_Headquarter/Company_headquarter_Test.txt", 'r', encoding="utf-8")

train_lines = train.readlines()
test_lines = test.readlines()


def createSuperVector(number):
    counter = 0
    company_arr, headquarter_arr = [], []
    while counter < number:
        counter += 1
        line = random.choice(train_lines).split()
        headquarter_arr.append(vec[line[1]])
        company_arr.append(vec[line[0]])
    company = np.average(company_arr, axis=0)
    headquarter = np.average(headquarter_arr, axis=0)
    return company, headquarter

def visualize(arg1, arg2):
    vect, avgr = [], []
    for a, b in zip(arg1, arg2):
        vect.append(a)
        avgr.append(b)

    data1 = {
        "x": vect,
        "y": avgr,

        "name": "Average accuracy for Company_Headquarter",
        "type": "scatter"
    }

    data = Data([data1])
    layout = {
        "title": "Average accuracy against testing data set",
        "xaxis": {"title": "Number of Vectors"},
        "yaxis": {"title": "Average accuracy"}
    }
    return data, layout


i = 0
line_number = sum(1 for line in open('../Data/Company_Headquarter/Company_headquarter_Test.txt'))

vector = []
avg = []

while i < 20:
    i += 1
    counter = 0
    accuracy = 0


    while counter < 10:
        counter += 1
        correct_result = 0

        company_super, headquarter_super = createSuperVector(i)
        for line in test_lines:
                Data_Test = line.split()
                if len(Data_Test) > 1:
                    Super_Vector = vec[Data_Test[0]] + headquarter_super
                    Result = vec.similar_by_vector((Super_Vector - company_super), topn=3)
                    # print(Result[0][0])
                    if Result[1][0] == Data_Test[1]:
                         Final_Result = Result[1][0]
                    elif Result[2][0] == Data_Test[1]:
                         Final_Result = Result[2][0]
                    else:
                        Final_Result = Result[0][0]
                    if Final_Result == Data_Test[1]:
                         correct_result += 1
                    f2.write(str(Result) + " " + Data_Test[1] + "\n")
                    f3.write(str(Final_Result) + " " + Data_Test[1] + "\n")
        print(correct_result)
        accuracy += correct_result / line_number
        print(accuracy)
        f4.write(str(correct_result) + "  " + (str(accuracy)) + "\n")
    Avg_Accuracy = (accuracy/10)
    print("Average Accuracy for Average ", i, ": ", Avg_Accuracy)
    f5.write(str(i) + " " + (str(Avg_Accuracy)) + "\n")
    vector.append(i)
    avg.append(Avg_Accuracy)
    visualize(vector, avg)
data, layout = visualize(vector, avg);
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)
