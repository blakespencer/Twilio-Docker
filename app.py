import os
from flask import Flask, send_from_directory, jsonify, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from sentiment import get_sentiment
from db import login, get_sentences, put_sentences, create_customer, get_response, update_customer_response, get_customer
import json

from secrets import account_sid, client_id


client = Client(account_sid, client_id)

path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='react_app/build')


@app.route('/api/send_sms')
def send_sms():
    number = request.args.get('number')
    message = request.args.get('message')
    positive = request.args.get('positive')
    negative = request.args.get('negative')
    number = '+1' + number.replace('-', '')
    print(number)
    create_customer(number, positive, negative)
    message = client.messages.create(
        body=message,
        from_='+13109847247',
        to=number)
    return jsonify({'message': 'success'}), 200


@app.route('/api/reply_sms', methods=['get', 'post'])
def reply_sms():
    reply = request.form['Body']
    number = request.form['From']
    # Check if they have replied
    if(get_customer(number)[4] != None):
        resp = MessagingResponse()
        response = 'Thank you for your response'
        resp.message(response)
        return str(resp)
    # Save response and then send back positive or negative
    update_customer_response(number, reply)
    sentiment_data = get_sentiment(reply)
    score = float(sentiment_data['documents'][0]['score'])
    print(score)
    if(score < 0.5):
        response = get_response(number, 2)
    if(score >= 0.5):
        response = get_response(number, 1)
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)


@app.route('/api/login', methods=['GET'])
def login_or_create():
    name = request.args.get('name')
    user_id = login(name)
    return jsonify({'name': name, 'id': user_id})


@app.route('/api/sentences', methods=['GET'])
def sentences_get():
    user_id = request.args.get('user_id')
    sentences = get_sentences(user_id)
    return jsonify(sentences), 200


@app.route('/api/sentences', methods=['PUT'])
def sentences_put():
    data = request.data
    data = data.decode(encoding='utf-8', errors='strict')
    print('data', data)
    dataDict = json.loads(data)
    user_id = dataDict['userId']
    type_num = dataDict['type']
    sentence = dataDict['sentence']
    put_sentences(sentence, user_id, type_num)
    return jsonify([]), 200


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("build/" + path):
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
