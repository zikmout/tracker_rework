import os
import fastText
import tracker.ml_toolbox as mltbx

class SU_Model():
	def __init__(self):
		print('pwd = {}'.format(os.getcwd()))
		self.name = 'modelx.bin' 
		self.su_model = fastText.load_model(self.name)
		print('Successfuly loaded model named : {} (\'{}\').'.format(self.name, self.su_model))

su_model = SU_Model()