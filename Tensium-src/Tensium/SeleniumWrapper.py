import string
from selenium.webdriver import Chrome

class ChromeDriverWrapper():
    executable_path: string = ""
    driver: Chrome = None
    home_page: string = "https://saucedemo.com/"

    def __init__(self, executable_path: string):
        self.executable_path = executable_path
        self.driver = Chrome(executable_path=self.executable_path)
        self.driver.get(self.home_page)
        pass
    
    def reset(self):
        try:
            if self.driver is not None:
                self.driver.close()
        except:
            pass

        if self.driver is not None:
            self.driver.quit()

        self.driver = Chrome(executable_path=self.executable_path)
        self.driver.get(self.home_page)
        