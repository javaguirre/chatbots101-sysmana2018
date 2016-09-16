from datetime import datetime, timedelta

from persist import PersistLayerService
from variables import VariableResolutionService


class FlowService(object):
    FLOW = [
        {
            'text': 'Hola! Quieres encargar una empanada?',
            'next': {'si': 1, 'no': 2}
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
        }
    ]

    # STEPS
    NOT_STARTED_STEP = -1
    START_STEP = 0

    def __init__(self, extra_variables):
        self.persist = PersistLayerService()
        current_data = self.persist.get()
        self.current_step = current_data.get('current_step', 0)
        self.variables = VariableResolutionService({
            'hour': datetime.now() + timedelta(hours=1),
            'name': extra_variables['name']
        })

    def process(self, text):
        step = self.get_next_step(text)
        message = self.variables.hidrate(self.get_step_text(step))

        return message

    def get_next_step(self, text):
        step = self.decide_next_step(text)
        print('Step {}'.format(step))
        self.persist.update_step(step)

        return step

    def get_step_text(self, step):
        return self.FLOW[step]['text']

    def decide_next_step(self, text):
        if self.current_step is self.NOT_STARTED_STEP:
            return self.START_STEP

        next_step = self.FLOW[self.current_step]['next']

        if not next_step:
            # END
            self.persist.remove_current_step()

        elif type(next_step) is int:
            return next_step

        elif type(next_step) is dict:
            print(next_step)
            return next_step[text]
