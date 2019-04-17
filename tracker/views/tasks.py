from tracker.views.base import BaseView
from tracker.utils import flash_message, login_required, get_celery_task_state
from tracker.celery import app_socket
from tracker.workers.live_view_worker import live_view
from celery.task.control import discard_all

from tornado.process import Subprocess
from tornado.iostream import StreamClosedError

from tornado import gen

def revoke_chain(last_result): 
    print('[CALLER] Revoking: {}'.format(last_result.task_id))
    last_result.revoke()
    if last_result.parent is not None:
        revoke_chain(last_result.parent)

class DeleteTaskQueues(BaseView):
    SUPPORTED_METHODS = ['GET']

    @gen.coroutine
    def get(self, username, projectname):
        print('Launching delete task view command ...\n')
        #cmd = shlex.split("rabbitmqadmin -f tsv -q list queues name > q2.txt; while read -r name; do rabbitmqadmin -q delete queue name='${name}'; done < q2.txt")
        cmd = "rabbitmqadmin -f tsv -q list queues name > q2.txt; while read -r name; do rabbitmqadmin -q delete queue name=\"${name}\"; done < q2.txt"
        #cmd = "ls -la; echo 'salut'; lss"
        yield self.run_subprocess(cmd)
        print('ALL RABBITMQ queues PURGED NOW :)\n')
        print('Deleting tasks from user session now ...')
        del self.session['tasks']['live_view']
        self.session.save()
        print('Tasks succesfully deleted from session !\n')
        flash_message(self, 'success', 'All queues succesfully deleted.')
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

    # @login_required
    # def get(self, username, projectname):
    #     print('Launching delete task view command ...\n')
    #     #ret = execute_cmd_async("rabbitmqadmin -f tsv -q list queues name > q2.txt; while read -r name; do rabbitmqadmin -q delete queue name='${name}'; done < q2.txt")
    #     ret = execute_cmd_async('ls -l')
    #     async for out, err in ret:
    #         print('OUT: {}, ERR: {}'.format(out, err))
    #     print('ALL RABBITMQ queues PURGED NOW :)\n')
    #     print('Deleting tasks from user session now ...')
    #     self.session['tasks']['live_view'] = None
    #     self.session.save()
    #     print('Tasks succesfully deleted from session !\n')
    #     flash_message(self, 'success', 'All queues succesfully deleted.')
    #     self.redirect('/')

class PurgeAllTasks(BaseView):
    """ This function does not work the way it is expected to.
        Tasks stays in queue.
    """
    SUPPORTED_METHODS = ['GET']

    @login_required
    @gen.coroutine
    def get(self, username, projectname):
        res = 0
        if 'live_view' in self.session['tasks']:

            # for worker in self.session['tasks']['live_view']:
            #     task = live_view.AsyncResult(worker['id'])
            #     task.abort()
            
            # print('All task have been succesfully aborted, purging rabbitmq queues now...\n')




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