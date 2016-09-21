import logging
from datetime import datetime, timedelta

from persist import PersistLayerService
from variables import VariableResolutionService


class FlowService(object):
    FLOW = [
        {
            'text': 'Hola! Quieres encargar una empanada?',
            'next': {'si': 1, 'no': 2, 'error': 5}
        },
        {
            'text': 'Genial! Cual quieres? Si no conoces el (menu) te lo puedo mostrar',
            'next': {'menu': 3, 'other': 4}
        },
        {
            'text': 'Una pena, otra vez sera! :-)',
            'next': None
        },
        {
            'text': 'El menu es: 1. atun, cebolla, 2. vieira, 3. jamon y queso',
            'next': {'menu': 3, 'other': 4}
        },
        {
            'text': 'Genial @var.name! a las @var.hour tus empanadas estaran listas!',
            'next': None
        },
        {
            'text': 'Perdona, no he entendido lo que has dicho, alguien se va a poner en contacto contigo',
            'next': None
        }
    ]

    # STEPS
    NOT_STARTED_STEP = -1
    START_STEP = 0

    def __init__(self, chat_id, extra_variables):
        self.persist = PersistLayerService()
        current_data = self.persist.get()
        self.chat_id = chat_id
        self.current_step = current_data.get(chat_id, self.START_STEP)

        if self.current_step is None:
            self.current_step = self.START_STEP

        self.variables = VariableResolutionService({
            'hour': datetime.now() + timedelta(hours=1),
            'name': extra_variables['name']
        })

    def process(self, text):
        step = self.get_next_step(text)
        message = self.variables.hidrate(self.FLOW[step]['text'])

        return message

    def get_next_step(self, text):
        step = self.decide_next_step(text)
        logging.info('Step {}'.format(step))
        self.persist.update_step(self.chat_id, step)

        return step

    def decide_next_step(self, text):
        if self.current_step is self.NOT_STARTED_STEP:
            return self.START_STEP

        next_step = self.FLOW[self.current_step]['next']

        if not next_step:
            # END
            self.persist.remove_current_step(self.chat_id)

            return self.NOT_STARTED_STEP

        return self.process_next_step_logic(next_step, text)

    def process_next_step_logic(self, step, text):
        try:
            return step[text]
        except KeyError:
            if 'other' in step:
                return step['other']
            else:
                return step['error']
