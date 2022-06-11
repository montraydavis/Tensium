class Eventsample(object): 
	def __init__(self): 
		self.__eventhandlersample = [] 
	def __iadd__(self, Ehandler): 
		self.__eventhandlersample.append(Ehandler) 
		return self
	def __isub__(self, Ehandler): 
		self.__eventhandlersample.remove(Ehandler) 
		return self

	def __call__(self, *args, **keywargs): 
		for eventhandlersample in self.__eventhandlersample: 
			eventhandlersample(*args, **keywargs) 