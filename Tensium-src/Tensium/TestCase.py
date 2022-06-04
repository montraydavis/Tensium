from cgitb import reset
import string

from stable_baselines3 import PPO
from Tensium.goals.TensiumBaseGoal import TensiumBaseGoal

from Tensium.TrainAndLoggingCallback import TrainAndLoggingCallback
from Tensium.envs.TensiumEnv import TensiumEnv

from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv


class TestCase():
    LOG_DIR: string = ""

    def __init__(self, id: string, possible_actions: list, discounts: list,
                 goal: TensiumBaseGoal, working_dir: string, max_tries: int = -1,
                 max_tries_factor: int = 3, reset_callback=None) -> None:

        self.id = id
        self.possible_actions = possible_actions
        self.discounts = discounts
        self.goal = goal
        self.working_dir = working_dir
        self.max_tries = max_tries,
        self.max_tries_factor = max_tries_factor
        self.reset_callback = reset_callback
        self.LOG_DIR = './' + id + '/logs'
        self.CHECKPOINT_DIR = './' + id + '/train'

        self.env = TensiumEnv(possible_actions, discounts, goal, working_dir,
                              max_tries, max_tries_factor, reset_callback)

        self.oenv = self.env

        self.env = DummyVecEnv([lambda: self.env])

    def Learn(self, n_steps=10000):

        callback = TrainAndLoggingCallback(
            check_freq=2, save_path=self.working_dir+'\\train\\'+self.id+'\\')

        model = PPO('MlpPolicy', self.env, verbose=0, tensorboard_log=self.LOG_DIR, learning_rate=0.000001,
                    n_steps=n_steps)
        model.learn(total_timesteps=1, callback=callback)
        pass

    def Run(self):
        model = PPO.load(
            self.working_dir+'\\train\\'+self.id+'\\model.zip')
        state = self.env.reset()

        done = False
        while done == False:
            action, _ = model.predict(state)
            state, reward, done, info = self.env.step(action)

    def Finish(self):
        self.oenv.driver_wrapper.driver.quit()


