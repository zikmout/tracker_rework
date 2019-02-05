from tracker.views.base import BaseView
from tracker.utils import flash_message, login_required, get_celery_task_state
from tracker.celery import app_socket
from tracker.workers.live_view_worker import live_view
from celery.task.control import discard_all

class PurgeAllTasks(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        if 'live_view' in self.session['tasks']:
            task_ids_to_stop = list()
            for worker in self.session['tasks']['live_view']:
                task_ids_to_stop.append(worker['id'])
                task = live_view.AsyncResult(worker['id'])
                print('Task id {} alive'.format(worker['id']))

            res = app_socket.control.revoke(task_ids_to_stop)
            print('Stopping all tasks id = {}'.format(res))
            print('Purging all live view tasks now ...')
            app_socket.control.purge()
            print('succesfully PURGED.')
            print('Try discard All now ...')
            discard_all()

            #print('Deleting live view tasks from session.')
            #del self.session['tasks']['live_view']
            #self.session.save()
            flash_message(self, 'success', 'Live view tasks succesfully purged ! Purged tasks = {}'.format(res))
            self.redirect('/')
        else:
            flash_message(self, 'danger', 'Failed purging live tasks')
            self.redirect('/')