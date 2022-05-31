import string
from selenium.webdriver import Chrome

from Tensium.TensiumEnv import TensiumEnv
from Tensium.goals.TensiumBaseGoal import TensiumBaseGoal

class TensiumTextComparerBaseGoal(TensiumBaseGoal):
    
    def __init__(self, element_selector: string, value_selector: string, config: dict = {}) -> None:
        super(TensiumTextComparerBaseGoal, self).__init__(element_selector, value_selector, config)
        
        if self._can_lower():
            self.value_selector = str(self.value_selector).lower()

    def _can_lower(self):
        lower_config = str(self.config['lower']).lower()

        if lower_config is not None:
            if lower_config == 'true':
                return True
                
        return False

    def get_text(self, env:TensiumEnv) -> string:
        try:
            if self.element is not None and self._can_lower():
                return str(self.element.text).lower()

            return self.element.text
        except:
            return None
       
    def check_goal(self, env: TensiumEnv) -> bool:
        try:
            self.element = env.driver_wrapper.driver.find_element_by_css_selector(self.element_selector)
        except:
            return False

        if self.element is None:
            return False

        return env.get_discounts() <= 0