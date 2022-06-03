import random
import os

from selenium.webdriver import Chrome

from Tensium.TrainAndLoggingCallback import TrainAndLoggingCallback

from Tensium.commands.SeleniumSetTextCommand import SeleniumSetTextCommand
from Tensium.commands.SeleniumClickCommand import SeleniumClickCommand

from Tensium.goals.TensiumTextEqualsGoal import TensiumTextEqualsGoal
from Tensium.TestCase import TestCase


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
login_test_case.Learn(2)
login_test_case.Run()
login_test_case.Finish()