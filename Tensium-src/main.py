import random
import os


from Tensium.commands.SeleniumSetTextCommand import SeleniumSetTextCommand
from Tensium.commands.SeleniumClickCommand import SeleniumClickCommand

from Tensium.goals.TensiumTextEqualsGoal import TensiumTextEqualsGoal
from Tensium.TestCase import TestCase
from Tensium.observation.TensiumObservation import TensiumObservation


def _reset_env(env):
    env.driver_wrapper.driver.get('https://saucedemo.com/')


# def _create_set(action_history: list, labels: list):
#     df = pd.DataFrame([i for i in action_history], columns=labels)
#     labels_ds = df.pop(labels[-1])
#     df = tf.data.Dataset.from_tensor_slices((dict(df), labels_ds))
#     df = df.batch(1)

#     return df


# actions = [SeleniumSetTextCommand('#user-name', 'standard_user'),
#            SeleniumSetTextCommand('#password', 'secret_sauce'),
#            SeleniumClickCommand('#login-button')]

# goal_config = {
#     'lower': 'true'
# }
# logged_in_goal = TensiumTextEqualsGoal(
#     element_selector=".title", value_selector='PRODUCTS', config=goal_config)

# env = TensiumEnv(actions, logged_in_goal,
#                  'C:\\Users\\montr\\source\\repos\\Github\\Tensium\\Tensium-src\\', _reset_env)

# done = False

# for i in range(10):
#     sample = env.action_space.sample()
#     obs, reward, done, info = env.step(sample)

#     env.reset()

# labels = ["LABEL_" + str(i) for i in range(len(env.action_history[0]))]

# train_ds = _create_set([i for i in env.action_history], labels)

# feature_columns = [feature_column.numeric_column(i) for i in labels[:-1]]
# feature_layer = tf.keras.layers.DenseFeatures(feature_columns)
# model = keras.models.Sequential([
#     feature_layer,
#     keras.layers.Dense(128, activation='relu'),
#     keras.layers.Dense(1, activation='sigmoid')
# ])

# model.compile(optimizer='adam',
#               loss='mean_squared_error',
#               metrics=['accuracy'])

# model.fit(train_ds,
#           epochs=50)

actions = [SeleniumSetTextCommand('#user-name', 'standard_user'),
           SeleniumSetTextCommand('#password', 'secret_sauce'),
           SeleniumClickCommand('#login-button')]

goal_config = {
    'lower': 'true'
}

logged_in_goal = TensiumTextEqualsGoal(
    element_selector=".title", value_selector='PRODUCTS', config=goal_config)

login_test_case = TestCase('myfirst_testcase', actions,
                           logged_in_goal, os.getcwd()+'\\Tensium-src\\', _reset_env)

# TensiumObservation(login_test_case.env, ['#login-button'])

login_test_case.Learn(n_steps=100, force_end_success=10)
login_test_case.Run(n_steps=100)
login_test_case.Finish()


# ''' Tensium API Walker '''


# possible_inputs = {
#     'temperatureC': {
#         'allowed_values': '$'
#     },
#     'summary': {
#         'allowed_values': '$'
#     },
#     'id': {
#         'allowed_values': '$'
#     },
#     'date': {
#         'allowed_values': '$'
#     }
# }

# update_forecast_regression = {
#     'inputs': ['temperatureC', 'summary', 'date'],
#     'input_key': 'id'
# }

# forecasts = TensiumEndpoint(url='http://localhost:5120/weatherforecast',
#                             possible_inputs=None, method='GET', regression=None)

# update_forecast = TensiumEndpoint(url='http://localhost:5120/weatherforecast',
#                                   possible_inputs=possible_inputs, method='POST', regression=update_forecast_regression)

# endpoints = [forecasts, update_forecast]

# tensium_walker = TensiumAPIWalker().walk_chain(endpoints)
