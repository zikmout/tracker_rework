import os
try:
    import fasttext as fastText
except:
    import fastText


class SU_Model():
    def __init__(self, name):
        print('[LOADING ML MODEL] from folder: \'{}\''.format(os.getcwd()))
        self.name = name
        self.su_model = fastText.load_model(name)
        print('Successfuly loaded model named : {} (\'{}\').'.format(
            self.name, self.su_model))
