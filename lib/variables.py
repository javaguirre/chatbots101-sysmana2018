import re


class VariableResolutionService(object):
    VARIABLES_PREFIX = '@var.'
    VARIABLES_REGEX = '{}(\w+)'.format(VARIABLES_PREFIX)

    def __init__(self, variables):
        self.variables = variables

    def hidrate(self, text):
        variables_to_be_hidrated = re.findall(self.VARIABLES_REGEX, text)

        if not variables_to_be_hidrated:
            return text

        return self.replace(variables_to_be_hidrated)

    def replace(self, text, variables):
        response_text = text

        for variable in variables:
            response_text = text.replace(
                '{}{}'.format(self.VARIABLES_PREFIX, variable),
                self.variables[variable]
            )

        return response_text
