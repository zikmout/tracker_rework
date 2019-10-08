from tornado import gen
from tracker.views.base import BaseView
from tracker.utils import flash_message, login_required, get_celery_task_state, revoke_all_tasks
from tracker.celery import live_view_worker_app
from tracker.workers.live.live_view_worker import live_view

from tornado.process import Subprocess
from tornado.iostream import StreamClosedError
from tornado import gen

class DeleteTaskQueues(BaseView):
    # Code borrowed and adapted from : https://gist.github.com/eliangcs/0b253675759c97b5b842
    SUPPORTED_METHODS = ['GET']

    @gen.coroutine
    def get(self, username, projectname):
        cmd = "rabbitmqadmin -f tsv -q list queues name > queues.txt; while read -r name; do rabbitmqadmin -q delete queue name=\"${name}\"; done < queues.txt"
        print('\nDeleting all rabbitmq queues from computer ...\n(cmd = {})\n'.format(cmd))
        yield self.run_subprocess(cmd)
        print('[SUCCESS] All rabbitmq queues deleted.\n')
        print('-> Deleting tasks from user session now ...')
        try:
            del self.session['tasks']['live_view']
            self.session.save()
            print('Tasks succesfully deleted from session. New session saved.\n')
        except Exception as e:
            print('[WARNING] No tasks to delete from session.\n(Reason: {})\n'.format(e))
        flash_message(self, 'success', 'All rabbitmq queues succesfully deleted.')
        self.redirect('/')

    @gen.coroutine
    def run_subprocess(self, cmd):
        proc = Subprocess(cmd, stdout=Subprocess.STREAM,
                          stderr=Subprocess.STREAM, shell=True)
        yield self.redirect_stream(proc.stdout)
        yield self.redirect_stream(proc.stderr)

    @gen.coroutine
    def redirect_stream(self, stream):
        while True:
            try:
                data = yield stream.read_bytes(128, partial=True)
                return 
            except StreamClosedError:
                break
            else:
                self.write(data)
                self.flush()
                return

class RevokeLiveTasks(BaseView):
    SUPPORTED_METHODS = ['GET']
    
    @login_required
    @gen.coroutine
    def get(self, username, projectname):
        res = 0
        if 'live_view' in self.session['tasks']:
            res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker in self.session['tasks']['live_view']])
            print('Deleting live view tasks from session.')
            del self.session['tasks']['live_view']
            self.session.save()
            flash_message(self, 'success', 'Live view tasks succesfully revoked ! Tasks = {}'.format(res))
            self.redirect('/')
        else:
            flash_message(self, 'danger', 'Failed revoking live tasks')
            self.redirect('/')