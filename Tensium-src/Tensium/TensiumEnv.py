import string
import gym
import numpy as np
import base64
import io

from datetime import date
from datetime import datetime
from PIL import Image
from gym import Env
from gym.spaces import Discrete, Box

from Tensium.SeleniumWrapper import ChromeDriverWrapper
from Tensium.commands.SeleniumBaseCommand import SeleniumBaseCommand
from Tensium.commands.SeleniumSetTextCommand import SeleniumSetTextCommand
from Tensium.goals.TensiumBaseGoal import TensiumBaseGoal
from Tensium.utils.ImageUtils import compare_image

class TensiumEnv(Env):
    prev_image: list = None
    goal: TensiumBaseGoal = None
    driver_wrapper: ChromeDriverWrapper = None
    last_run_time: datetime = None
    reset_callback = None
    state: int = 0
    max_tries: int = 0
    tries_remaining: int = 0
    actions: list = []
    discounts: list = []
    steps_history: list = []
    steps_session: list = []
    step_frames: list = []

    def __init__(self, driver_path: string, actions: list, discounts: int, goal: TensiumBaseGoal, max_tries: int = -1, max_tries_factor: int = 3, reset_callback = None):
        self.driver_wrapper = ChromeDriverWrapper(driver_path)
        self.action_space = Discrete(3)
        self.observation_space = Box(low=np.array([0], dtype=int), high=np.array([100], dtype=int), shape=(1,), dtype=int)
        self.actions = actions
        self.discounts = discounts
        self.goal = goal
        self.state = 0
        self.reset_callback = reset_callback

        if max_tries_factor < 0:
            max_tries_factor = 1

        if max_tries < 0:
            max_tries = len(actions) * max_tries_factor

        self.max_tries = max_tries
        self.tries_remaining = max_tries
        pass

    def get_discounts(self):
        total_discount = 0

        for discount in self.discounts:
            if discount(self.driver_wrapper.driver) == True:
                total_discount += 1

        return total_discount

    def get_screenshot(self):
        img_b64 = self.driver_wrapper.driver.get_screenshot_as_base64()
        decoded = base64.b64decode(img_b64)
        img = list(Image.open(io.BytesIO(decoded)).getdata())

        return img

    def get_metrics(self, start_time: datetime, action: int, reward: int, total_discount: int, pixels) -> dict:
        last_run = 0

        if self.last_run_time is None:
            last_run = 0
        else:
            last_run = (datetime.now() - self.last_run_time).total_seconds()

        info = {
            'action': action,
            'reward': (reward + total_discount),
            'duration': (datetime.now() - start_time).total_seconds(),
            'since_last_run': last_run,
            'frame': pixels
        }

        return info

    def step(self, action: int):
        if self.tries_remaining <= 0:
            return self.state, 0, True, self.get_metrics(start_time=start_time, action=action, reward=0, total_discount=0)
        
        start_time = datetime.now()

        self.state = action
        reward = 1

        # Execute Selenium Command
        callable_action: SeleniumBaseCommand = self.actions[action]
        callable_action.execute(self.driver_wrapper.driver)

        # Discounts
        '''
            Get Discounts

            Discount when agent hits negatively impacting feature.
            IE:
                Error dialog on login attempt
        '''
        total_discount = self.get_discounts()

        done = self.goal.check_goal(self)

        # Get screenshot and compare with previous pixel data
        img = self.get_screenshot()
        img_compare_match = compare_image(img, self.prev_image)

        # Give a reward for noticing a difference
        if img_compare_match == False:
            reward += 1

        final_reward = (reward - total_discount)

        # Calculate step metrics
        info = self.get_metrics(start_time=start_time, action=action, reward=reward, total_discount=total_discount, pixels=pixels)

        self.tries_remaining -= 1
        self.last_run_time = datetime.now()

        # Append historical information
        self.steps_history.append(info)
        self.steps_session.append(info)
        self.step_frames.append(img)

        return self.state, final_reward, done, info

    def _reset(self):
        self.driver_wrapper.reset()
        self.tries_remaining = self.max_tries
        self.state = np.random.randint(0, len(self.actions))
        self.steps_session = []

    def reset(self): 
        if self.reset_callback is not None:
            if self.reset_callback(self) == True:
                self._reset()
        else:
            self._reset()
        
        return self.state