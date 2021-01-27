from flask import render_template, current_app as app, request, redirect, url_for
import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot('Calculator',
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
              logic_adapters=[
                  {
                      'import_path': 'chatterbot.logic.BestMatch',
                      'default_response': 'Désolé, je n\'ai pas compris',
                      'maximum_similarity_threshold': 0.99
                  }
              ],
              database_uri='sqlite:///database.sqlite3')

trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.french')


@app.route('/')
def index():
    now = datetime.datetime.now()

    return render_template('index.html', title=bot.name, time=f'{now.hour:02d}:{now.minute:02d}')


@app.route('/get_answer')
def get_answer():
    msg = request.args.get('msg')
    response = bot.get_response(msg)
    return response.text
