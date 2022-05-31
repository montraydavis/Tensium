import string
from typing import overload
from selenium.webdriver import Chrome
from Tensium.commands.SeleniumBaseCommand import SeleniumBaseCommand

class SeleniumSetTextCommand(SeleniumBaseCommand):
    element_selector: string = None
    value: string = None

    def __init__(self, element_selector: string, value: string) -> None:
        super().__init__()

        self.element_selector = element_selector
        self.value = value
        
    def execute(self, driver: Chrome):
        try:
            element = driver.find_element_by_css_selector(self.element_selector)
    
            element.clear()
            element.send_keys(self.value)

        except: 
            pass
        pass