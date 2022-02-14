import sys
from collections import deque
from flask import Flask, request, jsonify
from mindmeld.components.dialogue import Conversation
from email_bot.__init__ import app
import requests

LANGUAGE_CHAIN_LENGTH = 2  # TODO: Get this from settings file
LANGDETECT_URL = "http://localhost:5000/detect"

conversations = {}

api = Flask(__name__)


def is_user_confirm(message):
    return app.app_manager.nlp.domains['email'].intent_classifier.predict(message) == 'confirmation'


def detect_lang(txt, default='ru'):
    req = requests.post(LANGDETECT_URL, json={'text': txt})
    return req.json()[0][0] or default


@api.route('/send', methods=['POST'])
def send():
    request_body = request.get_json()
    session_id = request_body['session_id']
    api.logger.info(request_body.get('message'))


    if request_body.get('restart') is True or request_body.get('message') == '/restart' or request_body.get('end_session') is True:
        conversation = conversations[session_id]['conversation']
        del conversations[session_id]
        return jsonify({'session_id': session_id,
                        'response': "Session restarted",
                        'from_core': True})

    if not request_body['session_id'] in conversations:
        user_data = {'session_id': session_id,
                     'username': session_id,  # TODO: Need get real name
                     'language': 'ru',
                     'detected_languages': deque(maxlen=LANGUAGE_CHAIN_LENGTH),
                     'language_confirmed': False,
                     'message_without_response': None,
                     'suggest_change_language': False,
                     'aggressive_met': False,
                     'last_response': None}
        conversation = Conversation(app=app, context=user_data)
        conversations[session_id] = {'conversation': conversation,
                                     'data': user_data}

    conversation, data = conversations[session_id]['conversation'], conversations[session_id]['data']

    if request_body.get('time_out') is True:
        return jsonify({'session_id': session_id,
                        'response': f"Еще раз: {data['last_response'][0]}",
                        'from_core': True})

    message = request_body['message']

    detected_languages = data['detected_languages']
    lang = detect_lang(message, default=data['language'])
    detected_languages.append(lang)

    if data.get('suggest_change_language'):
        change_lang = is_user_confirm(message)
        if change_lang:
            data['language'] = detected_languages[0]
        data['language_confirmed'] = True
        message = data['message_without_response']
        data['message_without_response'] = None
        data['suggest_change_language'] = False
    elif not data['language_confirmed'] and \
            len(detected_languages) == LANGUAGE_CHAIN_LENGTH and detected_languages[0] != data['language'] and \
            all(e == detected_languages[0] for e in detected_languages):
        data['message_without_response'] = message
        data['suggest_change_language'] = True

        response = "Змінити мову з {} на {}?".format(data['language'], detected_languages[0])
        data['last_response'] = response
        conversations[session_id] = {'conversation': conversation,
                                     'data': data,
                                     'frame': conversation.frame}
        return jsonify({'session_id': session_id,
                        'response': response,
                        'from_core': True})

    conversation.context = data
    response = conversation.say(message)
    data = conversation.context

    intent = conversation.history[0]['request']['intent']
    entities = conversation.history[0]['request']['entities']

    # TODO: Exit on goodbye?
    # if intent == 'goodbye':
    #     del conversations[session_id]

    data['last_response'] = response[0],
    conversations[session_id] = {'conversation': conversation,
                                 'data': data,
                                 'frame': conversation.frame}
    return jsonify({
        'session_id': session_id,
        'response': response,
        'intent': intent,
        'entities': entities,
        'from_core': False,
        'lang': data['language']
    })

api.run(host='0.0.0.0', port=5001, debug=True)
