from abc import abstractclassmethod


class SeleniumBaseCommand():
    @abstractclassmethod
    def execute():
        '''
            Execute commands
        '''
        pass
    pass