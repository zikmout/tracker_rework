import os
import fastText

class SU_Model():
	def __init__(self, name):
		print('pwd = {}'.format(os.getcwd()))
		self.name = name 
		self.su_model = fastText.load_model(name)
		print('Successfuly loaded model named : {} (\'{}\').'.format(self.name, self.su_model))

#su_model = SU_Model()