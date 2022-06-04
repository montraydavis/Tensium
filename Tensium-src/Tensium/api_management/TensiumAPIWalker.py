import requests
import flatdict
import numpy as np


from Tensium.api_management.TensiumEndpoint import TensiumEndpoint

class TensiumAPIWalker():
    last_endpoint = None

    def build_input(self, endpoints, ept: TensiumEndpoint):
        endpoint_input = None

        if ept.method == 'POST' and endpoints.index(ept) != 0:
            '''
            Build input object
            '''
            endpoint_input_keys = list(ept.possible_inputs.keys())

            endpoint_input = {}

            for endpoint_n_key in endpoint_input_keys:
                endpoint_input_rand_value = np.random.randint(
                    0, len(endpoint_input_keys)-1)
                endpoint_input[endpoint_n_key] = ept.possible_inputs[endpoint_n_key]['allowed_values'][endpoint_input_rand_value]

        return endpoint_input

    def run_endpoint(self, endpoints: list, ept: TensiumEndpoint):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        ept_input = self.build_input(endpoints, ept)

        if ept.method == 'GET':
            return flatdict.FlatDict(
                requests.get(url=ept.url, params={}, headers=headers).json())
        else:
            return flatdict.FlatDict(
                requests.post(url=ept.url, json=ept_input, headers=headers).json())

    def do_regression(self, endpoints, endpoint_response, endpoint_regression, last_endpoint):
        if isinstance(endpoint_regression, dict):
            endpoint_regression_inputs = endpoint_regression['inputs']

            # endpoint_regression_input_key = endpoint_regression['input_key']
            '''
                TODO: Implement functionality to do regression on key matched object
                '''

            endpoint_previous_regression = dict(self.run_endpoint(endpoints,
                last_endpoint['endpoint']))

            endpoint_regression_input_matches = []
            for endpoint_regression_input in endpoint_regression_inputs:
                for regression_value in endpoint_previous_regression:
                    if str(regression_value).endswith(endpoint_regression_input) == True and dict(endpoint_response)[regression_value] == endpoint_previous_regression[regression_value]:
                        endpoint_regression_input_matches.append(
                            endpoint_regression_input)
                        break
          

            return endpoint_regression_input_matches == endpoint_regression_inputs
        return False

    def walk_chain(self, endpoints):
        walk_chain_pass = True

        try:
            for endpoint in endpoints:
                endpoint_index = endpoints.index(endpoint)
                endpoint_regression = endpoints[endpoint_index].regression

                endpoint_response = self.run_endpoint(endpoints, endpoint)

                if endpoint_regression is not None:
                    walk_chain_pass = self.do_regression(endpoints=endpoints,endpoint_response=endpoint_response,
                                    endpoint_regression=endpoint_regression, last_endpoint=last_endpoint)

                    if walk_chain_pass == False:
                        return False

                if endpoint_index < len(endpoints) - 1:
                    next_endpoint = endpoints[endpoint_index+1]

                    next_inputs = list(next_endpoint.possible_inputs.keys())

                    '''
                    Gather all field values which are applicable to next endpoint
                    '''
                    for n_input in next_inputs:
                        endpoint_n_input = next_endpoint.possible_inputs[n_input]
                        endpoint_n_input_allowed_values = endpoint_n_input['allowed_values']

                        '''
                        Forward feed applicable values 
                        '''
                        if isinstance(endpoint_n_input_allowed_values, str):
                            if endpoint_n_input_allowed_values == '$':
                                tmp_possible_values = []
                                tmp_possible_keys = endpoint_response.keys()

                                for possible_key in tmp_possible_keys:
                                    if str(possible_key).endswith(n_input):
                                        tmp_possible_values.append(
                                            endpoint_response[possible_key])

                                endpoints[endpoint_index+1].possible_inputs[n_input]['allowed_values'] = list(
                                    set(tmp_possible_values))

                last_endpoint = {
                    'endpoint': endpoint,
                    'response': endpoint_response
                }
        except:
            walk_chain_pass = False

        return walk_chain_pass