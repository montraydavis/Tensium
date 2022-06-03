import string
from Tensium.envs.TensiumEnv import TensiumEnv
from Tensium.goals.TensiumTextComparerBaseGoal import TensiumTextComparerBaseGoal

class TensiumTextEqualsGoal(TensiumTextComparerBaseGoal):

    def __init__(self, element_selector: string, value_selector: string, config: dict) -> None:
        super(TensiumTextEqualsGoal, self).__init__(element_selector, value_selector, config)
        pass

    def check_goal(self, env: TensiumEnv) -> bool:
        if super(TensiumTextEqualsGoal, self).check_goal(env) == True:
            return self.get_text(env) == self.value_selector

        return False