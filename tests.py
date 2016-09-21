import unittest
import datetime

from lib.variables import VariableResolutionService


class VariableResolutionServiceTest(unittest.TestCase):
    def test_hidrate_valid(self):
        # GIVEN
        text = 'Hola @var.name'
        variables = {
            'name': 'cosferico'
        }
        service = VariableResolutionService(variables)

        # WHEN
        text = service.hidrate(text)

        # THEN
        self.assertEqual(text, 'Hola cosferico')

    def test_hidrate_notneeded(self):
        # GIVEN
        text = 'Hola @var.name'
        variables = {
            'hour': 'mi time in string'
        }
        service = VariableResolutionService(variables)

        # WHEN
        text = service.hidrate(text)

        # THEN
        self.assertEqual(text, 'Hola @var.name')

    def test_replace_valid(self):
        # GIVEN
        text = 'Hola @var.name, son las @var.hour horas'
        variables = {
            'name': 'cosferico',
            'hour': datetime.datetime.now().strftime('%H')
        }
        variables_found = ['name', 'hour']
        service = VariableResolutionService(variables)

        # WHEN
        text = service.replace(text, variables_found)

        # THEN
        self.assertEqual(
            text,
            'Hola cosferico, son las {} horas'.format(variables['hour'])
        )

    def test_replace_notneeded(self):
        # GIVEN
        text = 'Hola @var.another'
        variables = {
            'name': 'cosferico',
            'hour': datetime.datetime.now().strftime('%H')
        }
        variables_found = ['another']
        service = VariableResolutionService(variables)

        # WHEN
        text = service.replace(text, variables_found)

        # THEN
        self.assertEqual(text, 'Hola @var.another')
