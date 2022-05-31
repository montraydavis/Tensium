class TensiumAction():
    action = None

    def __init__(self, action):
        self.action = action

    def run(self, driver):
        if self.action is not None:
            self.action(driver)