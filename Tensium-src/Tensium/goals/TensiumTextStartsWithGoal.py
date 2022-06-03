import string
from Tensium.envs.TensiumEnv import TensiumEnv
from Tensium.goals.TensiumTextComparerBaseGoal import TensiumTextComparerBaseGoal

class TensiumTextStartsWithGoal(TensiumTextComparerBaseGoal):

    def __init__(self, element_selector: string, value_selector: string, config: dict) -> None:
        super(TensiumTextStartsWithGoal.py, self).__init__(element_selector, value_selector, config)
        pass

    def check_goal(self, env: TensiumEnv) -> bool:
        if super(TensiumTextStartsWithGoal.py, self).check_goal(env) == True:
            try:
                return str.startswith(self.get_text(env), self.value_selector) == True
            except:
                return False

        return False