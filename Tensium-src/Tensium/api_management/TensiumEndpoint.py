import string

class TensiumEndpoint():
    url: string
    possible_inputs: list
    method: string
    regression: dict

    def __init__(self, url: string, possible_inputs: list, method: string, regression: dict):
        self.url = url
        self.possible_inputs = possible_inputs
        self.method = method
        self.regression = regression