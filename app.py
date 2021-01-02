from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot(
    'Bobot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

 # Training with Personal Ques & Ans 
arabic_data_sample = open('arabic.txt').read().splitlines()
french_data_sample = open('french.txt').read().splitlines()
english_data_sample = open('english.txt').read().splitlines()

training_data = arabic_data_sample+english_data_sample+french_data_sample

trainer = ListTrainer(chatbot)
trainer.train(training_data)

from flask import Flask, render_template, request

app = Flask(__name__, template_folder= 'template')
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

if __name__ == "__main__":
    app.run()
