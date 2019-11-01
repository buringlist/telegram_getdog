from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import re
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

# https_proxy = {'https': "198.199.85.139:3128", }

# token = '1049364873:AAGVY0jkqHC7tIAKGlneY-fhqecoIxBC60k'
# setWebHook https://221787f1.ngrok.io
URL = 'https://api.telegram.org/bot1049364873:AAGVY0jkqHC7tIAKGlneY-fhqecoIxBC60k/'


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text):
    # Отправка ответа пользователю
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    # Поиск породы в полученной фразе
    pattern = r'\w+'
    name = re.search(pattern, text).group()
    return name


def get_dog(breed):
    # Получение изображения по api
    url = 'https://dog.ceo/api/breed/{}/images/random'.format(breed)
    r = requests.get(url).json()
    image = r['message']
    return image


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'\w+'

        if re.search(pattern, message):
            image = get_dog(parse_text(message))
            send_message(chat_id, image)
        return jsonify(r)
    return '<h1> Welcome </h1>'


if __name__ == '__main__':
    app.run()
