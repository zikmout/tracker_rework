import os
import tornado
import json
import datetime
import time

from tornado import gen


from tracker.views.base import BaseView
from tracker.utils import json_response
import tracker.ml_toolbox as mltx

print('FILE predict == {} (cwd = {})'.format(__file__, os.getcwd()))
if '.egg' in __file__ and  'workers' not in os.getcwd():
    import tracker.ml_toolbox as mltx
    su_model = mltx.SU_Model('trained_800_wiki2.bin').su_model

def make_predictions(content, min_acc=0.75):
    global su_model
    #print('su_model : {}'.format(su_model))
    #gc.collect()
    #print('content : {} [...]'.format(content[:1000]))
    preds = su_model.predict(content, 2)
    print('predictions = {}'.format(preds))
    #print('predictions = {} (acc = {})'.format(preds[0][0], preds[1][0]))
    if '__label__1' in preds[0][0] and preds[1][0] > float(min_acc):
        prediction = '__label__1'
        #print('[FastText] Predicted {} with {} confidence.'.format(prediction, preds[1][0]))
        return True
    else:
        prediction = '__label__2'
        #print('[FastText] Predicted {} with {} confidence.'.format(prediction, preds[1][0]))
        return False

class SBBPredict(BaseView):
    SUPPORTED_METHODS = ['POST']
    @gen.coroutine
    def post(self):
    	args = { k: self.get_argument(k) for k in self.request.arguments }
    	#print('Ask to predict = {}'.format(args))
    	content = args['content']
    	min_acc = 0.75
    	if 'min_acc' in args:
    		min_acc = args['min_acc']

    	prediction = make_predictions(content, min_acc=min_acc)
    	self.send_response(data=prediction)











