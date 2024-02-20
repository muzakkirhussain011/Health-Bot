import random
import json

import torch
from .model import NeuralNet

from .nltk_utils import bag_of_words, tokenize
# import speciailst_prediction
from .speciailst_prediction import predictSpecialist
extracted_symptoms = []
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import os
APP_DIR = os.path.dirname(os.path.abspath(__file__))
knowledgebase_file = os.path.join(APP_DIR, 'static\\data\\updated_knowldgebase.json')
with open(knowledgebase_file, 'r') as json_data:
    intents = json.load(json_data)

FILE = os.path.join(APP_DIR, 'static\\data\\data.pth')
data = torch.load(FILE)
# C:\Users\Sag10\OneDrive\Documents\GitHub\HealthyBot\healthbot_app\static\data\updated_knowldgebase.json
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
extracted_symptoms = []
def reset():
    global extracted_symptoms
    extracted_symptoms = []  # Reset the list to empty
def chatbot(sentence):   
     
    global extracted_symptoms

   

    bot_name = "HealthBot"
    print("Let's chat! (type 'quit' to exit)")
    sentence = sentence.lower()
    if sentence == "done":
        if len(extracted_symptoms) == 0:
            return "Please enter some symptoms."
        else:    
            extracted_symptoms = list(set(extracted_symptoms))

            suggestion = predictSpecialist(extracted_symptoms)
            extracted_symptoms = []
            return(str(suggestion))
        # print("NB prediction: ", nb_prediction)
        # print(prediction)
    reply = ""

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
   
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    # print("predicted item, ", predicted.item())
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    # print("prob: ", prob.item())
    if prob.item() > 0.90:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # print(f"{bot_name}: {random.choice(intent['responses'])}, tag:{intent['tag']}")
                reply += f"{random.choice(intent['responses'])}, tag:{intent['tag']}"
                if intent['tag'] not in ["greetings", "goodbye", "thanks"]:
                    extracted_symptoms.append(intent['tag'])
        return reply
    else:
        # print(f"{bot_name}: I do not understand, did you mean: {tag}")
        reply = reply + f"I do not understand, did you mean: {tag} <br>"

        # print("Try these:")
        reply += "Try these: <br>"

        for intent in intents['intents']:
            if tag == intent["tag"]:
                i =0
                for _ in intent['patterns']:
                    i += 1
                    # print(f"{i}. {pattern}")
                    reply += f"<br> {i}. {random.choice(intent['patterns'])}"

                    if i == 4:
                        break
                if i == 4:
                    break
        return reply

    

      