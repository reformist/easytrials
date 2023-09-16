from flask import Flask, render_template, request
import basic_chatbot

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html')

@app.route('/get_response', methods = ['POST'])

def get_bot_response():
    user_input = request.form['user_input']
    bot_response = basic_chatbot.get_response(user_input)
    return bot_response

if __name__ == '__main__':
    app.run(debug=True)