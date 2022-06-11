import string
import base64
import io

from PIL import Image
from gym import Env
from gym.spaces import MultiDiscrete, Box, Dict
from gym.utils import seeding

from Tensium.envs.SeleniumWrapper import ChromeDriverWrapper
from Tensium.goals.TensiumBaseGoal import TensiumBaseGoal
from Tensium.utils.EventSample import Eventsample

class TensiumEnv(Env):
    numeric_obs_space: list = []
    action_history: list = []
    image_obs_space = None
    goal: TensiumBaseGoal = None
    reset_callback = None

    event_handlers = {
        'on_stepping': Eventsample(),
        'on_stepped': Eventsample(),
        'on_resetting': Eventsample(),
        'on_reset': Eventsample(),
    }

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _get_screenshot(self, element_selector):
        img_b64 = self.driver_wrapper.driver.find_element_by_tag_name(element_selector).screenshot_as_base64
        decoded = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(decoded))

        return img, img.getdata()

    def _get_obs(self):
        img_b64 = self.driver_wrapper.driver.find_element_by_tag_name("html").screenshot_as_base64
        decoded = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(decoded)).convert('RGB').getdata()

        return img

    def get_discounts(self):
        return 0

    def __init__(self, actions: list, goal: TensiumBaseGoal, working_dir: string, reset_callback):
        self.actions = actions
        self.goal = goal
        self.working_dir = working_dir
        self.driver_wrapper = ChromeDriverWrapper(
            working_dir + '\\chromedriver.exe')
        self.reset_callback = reset_callback

        img, pixels = self._get_screenshot("body")

        self.obs_info = {
            'width': img.width,
            'height': img.height
        }

        self.action_space = MultiDiscrete([len(actions)] * len(actions))
        self.observation_space = Dict({
            'screenshot': Box(low=0, high=255, shape=(img.height, img.width, 3))
        })
        
        self.seed()

    def _execute_actions(self, actions):
        for act in actions: self.actions[act].execute(self.driver_wrapper.driver)

    def step(self, actions):
        self.event_handlers['on_stepping']({'action':actions})
        reward = 0
        done = False

        self._execute_actions(actions)

        if self.goal.check_goal(self):
            reward = 1
            done = True

        self.action_history.append([i for i in actions] + [reward])

        info = {
            'action':actions,
            'history': self.action_history
        }

        self.event_handlers['on_stepped'](info)
        return dict(screenshot=self._get_obs()), reward, done, info

    def reset(self):
        if self.reset_callback is not None:
            self.reset_callback(self)

    def render(self):
        pass
