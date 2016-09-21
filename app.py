import os

from flask import Flask, render_template, request

from lib import PersistLayerService, FlowService, TelegramBotService

app = Flask(__name__)

BASE_URL = os.environ.get('FLASK_BASE_URL', '')
WEBHOOK_URI = '/webhook'


def process_post_request(request):
    config = request.form
    persist = PersistLayerService()

    if persist.is_valid(config):
        persist.save(dict(api_key=config['api_key']))
        TelegramBotService.register(
            config['api_key'],
            ''.join([BASE_URL, WEBHOOK_URI]))
    else:
        return 'The configuration key is not valid', 400

    return 'Saved!'


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return process_post_request(request)

    return render_template('index.html')


@app.route(WEBHOOK_URI, methods=['POST'])
def webhook():
    persist = PersistLayerService()
    post_data = request.get_json()

    try:
        chat_id = post_data['message']['chat']['id']
        username = post_data['message']['from']['first_name']
        text = post_data['message']['text']
    except KeyError:
        return 'The POST data is not valid', 400

    flow_service = FlowService(
        chat_id=chat_id,
        extra_variables={'name': username})
    response = flow_service.process(text)
    TelegramBotService.send(persist.get()['api_key'], chat_id, response)

    return 'OK'


if __name__ == "__main__":
    app.run(debug=True)