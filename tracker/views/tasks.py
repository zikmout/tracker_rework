from tracker.views.base import BaseView
from tracker.utils import flash_message, login_required, get_celery_task_state
from tracker.celery import app_socket
from tracker.workers.live_view_worker import live_view
from celery.task.control import discard_all

def revoke_chain(last_result): 
    print('[CALLER] Revoking: {}'.format(last_result.task_id))
    last_result.revoke()
    if last_result.parent is not None:
        revoke_chain(last_result.parent)

class PurgeAllTasks(BaseView):
    """ This function does not work the way it is expected to.
        Tasks stays in queue.
    """
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        res = 0
        if 'live_view' in self.session['tasks']:
            task_ids_to_stop = list()
            for worker in self.session['tasks']['live_view']:
                task_ids_to_stop.append(worker['id'])
                task = live_view.AsyncResult(worker['id'])
                print('Task id {} alive'.format(worker['id']))
                revoke_chain(task)


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