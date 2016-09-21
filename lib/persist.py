import pickle


class PersistLayerService(object):
    DB_FILE = 'db.pickle'

    def is_valid(self, data):
        return bool(data.get('api_key', None))

    def get(self):
        data = {}

        try:
            data = pickle.load(open(self.DB_FILE, 'rb'))
        except IOError:
            self.init()

        return data

    def save(self, data):
        pickle.dump(data, open(self.DB_FILE, 'wb'))

    def init(self):
        self.save({})

    def update_step(self, chat_id, step):
        data = self.get()
        data[chat_id] = step
        self.save(data)

        return data

    def remove_current_step(self, chat_id):
        data = self.get()
        del data[chat_id]
        self.save(data)
