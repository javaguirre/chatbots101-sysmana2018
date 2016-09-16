import pickle


class PersistLayerService(object):
    DB_FILE = 'db.pickle'

    def is_valid(self, data):
        return bool(data.get('api_key', None))

    def get(self):
        return pickle.load(open(self.DB_FILE, 'rb'))

    def save(self, data):
        pickle.dump(data, open(self.DB_FILE, 'wb'))

    def update_step(self, step):
        data = self.get()
        # TODO Per chat_id
        data['current_step'] = step
        self.save(data)

        return data

    def remove_current_step(self):
        data = self.get()
        del data['current_step']
        self.save(data)
