import string
from Tensium.envs.TensiumEnv import TensiumEnv
from Tensium.goals.TensiumTextComparerBaseGoal import TensiumTextComparerBaseGoal

class TensiumTextEndsWithGoal(TensiumTextComparerBaseGoal):

    def __init__(self, element_selector: string, value_selector: string, config: dict) -> None:
        super(TensiumTextEndsWithGoal, self).__init__(element_selector, value_selector, config)
        pass

    def check_goal(self, env: TensiumEnv) -> bool:
        if super(TensiumTextEndsWithGoal, self).check_goal(env) == True:
            try:
                return str.endswith(self.get_text(env), self.value_selector) == True
            except:
                return False

        return False