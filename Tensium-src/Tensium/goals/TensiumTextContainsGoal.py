import string
from Tensium.envs.TensiumEnv import TensiumEnv
from Tensium.goals.TensiumTextComparerBaseGoal import TensiumTextComparerBaseGoal
import TensiumBaseGoal

from selenium.webdriver import Chrome

class TensiumTextContainsGoal(TensiumTextComparerBaseGoal):

    def __init__(self, element_selector: string, value_selector: string, config: dict) -> None:
        super(TensiumTextContainsGoal, self).__init__(element_selector, value_selector, config)
        pass

    def check_goal(self, env: TensiumEnv) -> bool:
        if super(TensiumTextContainsGoal, self).check_goal(env) == True:
            try:
                return str(self.get_text(env)).index(self.value_selector) >= 0
            except:
                return False

        return False