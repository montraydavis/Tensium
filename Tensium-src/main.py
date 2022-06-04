import random
import os

from selenium.webdriver import Chrome


from Tensium.commands.SeleniumSetTextCommand import SeleniumSetTextCommand
from Tensium.commands.SeleniumClickCommand import SeleniumClickCommand

from Tensium.goals.TensiumTextEqualsGoal import TensiumTextEqualsGoal
from Tensium.TestCase import TestCase
from Tensium.api_management.TensiumEndpoint import TensiumEndpoint
from Tensium.api_management.TensiumAPIWalker import TensiumAPIWalker


def discount_error_login(driver: Chrome) -> bool:
    try:
        error_dialog = driver.find_element_by_css_selector(
            ".error-message-container")

        if error_dialog.text != '':
            return True
    except:
        return False

    return False


CHECKPOINT_DIR = './train/'
LOG_DIR = './logs/'

callback = TrainAndLoggingCallback(check_freq=10000, save_path=CHECKPOINT_DIR)

actions = [SeleniumSetTextCommand('#user-name', 'standard_user'),
           SeleniumSetTextCommand('#password', 'secret_sauce'),
           SeleniumClickCommand('#login-button')]

for i in range(0, 5):
    random.shuffle(actions)

config = {
    'lower': 'true'
}
logged_in_goal = TensiumTextEqualsGoal(
    element_selector=".title", value_selector='PRODUCTS', config=config)

login_test_case = TestCase('myfirst_testcase', actions,
                           [discount_error_login], logged_in_goal, os.getcwd()+'\\Tensium-src\\')
login_test_case.Learn()
login_test_case.Run()
login_test_case.Finish()


''' Tensium API Walker '''


possible_inputs = {
    'temperatureC': {
        'allowed_values': '$'
    },
    'summary': {
        'allowed_values': '$'
    },
    'id': {
        'allowed_values': '$'
    },
    'date': {
        'allowed_values': '$'
    }
}

update_forecast_regression = {
    'inputs': ['temperatureC', 'summary', 'date'],
    'input_key': 'id'
}

forecasts = TensiumEndpoint(url='http://localhost:5120/weatherforecast',
                            possible_inputs=None, method='GET', regression=None)

update_forecast = TensiumEndpoint(url='http://localhost:5120/weatherforecast',
                                  possible_inputs=possible_inputs, method='POST', regression=update_forecast_regression)

endpoints = [forecasts, update_forecast]

tensium_walker = TensiumAPIWalker().walk_chain(endpoints)
