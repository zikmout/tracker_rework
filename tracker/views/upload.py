import os
import random
import string
import pandas as pd
import tornado
from tracker.views.base import BaseView
from tracker.utils import flash_message, login_required

class UploadHandler(BaseView):
    def post(self):
        #print('self.request.files = {}'.format(self.request.files))
        file1 = self.request.files['file1'][0]
        fname = file1['filename']
        extension = os.path.splitext(fname)[1]

        #fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        tmp_fname = 'tmp' + extension
        with open(tmp_fname, 'wb+') as fd:
            fd.write(file1['body'])
        df = pd.read_excel(tmp_fname)

        links = dict(zip(df['target'], df['target_label']))
        print('links = {}'.format(links))
        #print('DATAFRAME = {}'.format(df))
        os.remove(tmp_fname)
        flash_message(self, 'success', '\'{}\' successfully uploaded. Alert {} created.'.format(fname, fname.replace('.xlsx', '')))
        self.redirect('/')

        #links = 
        
        #user = self.request_db.query(User).filter_by(username=self.session['username']).first()
        #new_fastalert = FastAlert(fname.replace(extension, ''), self.application.data_path, links)

        #project = user.projects.filter_by(name=projectname).first()
        #content = project.contents.filter_by(name=content_name).first()
        #new_alert = Alert(args['inputName'], args['inputType'], args['inputStartTime'], notify=checked)
        #content.alerts.append(new_alert)
        #self.request_db.add(content)
        #self.request_db.commit()



        #self.finish("file" + final_filename + " is uploaded")
