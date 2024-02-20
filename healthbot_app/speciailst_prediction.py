import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)



# Encoding the target value into numerical
# value using LabelEncoder
from sklearn.preprocessing import LabelEncoder
import json
import os
import random

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, 'static\\data\\specialists_symptoms_train.csv')

data = pd.read_csv(DATA_PATH).dropna(axis = 1)
encoder = LabelEncoder()
data["specialist"] = encoder.fit_transform(data["specialist"])

APP_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(APP_DIR, 'static\\data\\suggestion.json')

with open(JSON_PATH, 'r') as json_data:
    suggestions = json.load(json_data)

X = data.iloc[:,:-1]
import joblib
NB_model= os.path.join(APP_DIR, 'static\\data\\nb_model.joblib')
nb_model = joblib.load(NB_model)
RF_model= os.path.join(APP_DIR, 'static\\data\\rf_model.joblib')
rf_model = joblib.load(RF_model)
SVM_model= os.path.join(APP_DIR, 'static\\data\\svm_model.joblib')
svm_model = joblib.load(SVM_model)


 
# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptoms = X.columns.values

 
# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i for i in value.split("_")])
    symptom_index[symptom] = index
 
data_dict = {
    "symptom_index":symptom_index,
    "predictions_classes":encoder.classes_
}
 
def mode(x):
    values, counts = np.unique(x, return_counts=True)
    m = counts.argmax()
    return values[m], counts[m]
# Defining the Function
# Input: string containing symptoms separated by commmas
# Output: Generated predictions by models
def predictSpecialist(symptoms):
    # symptoms = symptoms.split(",")
     
    # creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1
         
    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1,-1)
     
    # generating individual outputs
    rf_prediction = data_dict["predictions_classes"][rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][svm_model.predict(input_data)[0]]
    
    print(rf_prediction)
    print(nb_prediction)
    print(svm_prediction)
    # making final prediction by taking mode of all predictions
    final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0]
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction":final_prediction
    }
    print(f"HealthBot: {final_prediction}")
    for suggestion in suggestions['specialists']:
                if final_prediction == suggestion["specialist"]:
                    return f"<strong style=\"color:#02c1cc\">{random.choice(suggestion['suggestions'])}, specialist:{final_prediction}</strong>"
   
 

