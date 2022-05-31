import os
import random

from selenium.webdriver import Chrome
from matplotlib import pyplot as plt

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.vec_env.vec_frame_stack import VecFrameStack

from Tensium.TensiumEnv import TensiumEnv

from Tensium.TrainAndLoggingCallback import TrainAndLoggingCallback

from Tensium.commands.SeleniumSetTextCommand import SeleniumSetTextCommand
from Tensium.commands.SeleniumClickCommand import SeleniumClickCommand

from Tensium.goals.TensiumTextEqualsGoal import TensiumTextEqualsGoal


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

actions = [SeleniumSetTextCommand('#user-name', 'standard_user'), SeleniumSetTextCommand(
    '#password', 'secret_sauce'), SeleniumClickCommand('#login-button')]
    
for i in range(0,5):
    random.shuffle(actions)

logged_in_goal = TensiumTextEqualsGoal(
    element_selector=".title", value_selector='PRODUCTS', config={
        'lower': 'true'
    })

work_dir = os.getcwd()
env = TensiumEnv(driver_path='{}\\chromedriver.exe'.format(
    work_dir), actions=actions, discounts=[discount_error_login], goal=logged_in_goal)

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=LOG_DIR, learning_rate=0.000001,
            n_steps=512)
model.learn(total_timesteps=100, callback=callback)
model.save('thisisatestmodel')

# Test it out
model = PPO.load('./train/best_model_1000000')
state = env.reset()
while True: 
    
    action, _ = model.predict(state)
    state, reward, done, info = env.step(action)
    env.render()

# for idx in range(0, 100000):
#     state, reward, done, info = env.step(env.action_space.sample())

#     plt.figure(figsize=(20, 16))
#     for idx in range(state.shape[3]):
#         plt.subplot(1, 4, idx+1)
#         plt.imshow(state[0][:, :, idx])
#     plt.show()

#     if done == True:
#         env.reset()
