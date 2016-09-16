import telegram


class TelegramBotService(object):
    @staticmethod
    def register(auth_token, url):
        bot = telegram.Bot(auth_token)
        bot.setWebhook(url)

    @staticmethod
    def send(auth_token, chat_id, text):
        bot = telegram.Bot(auth_token)
        bot.sendMessage(
            chat_id=chat_id,
            text=text
        )
