import shlex

import tornado.ioloop
import tornado.web

from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.process import Subprocess

class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET']
    @gen.coroutine
    def get(self):
        #cmd = shlex.split("rabbitmqadmin -f tsv -q list queues name > q2.txt; while read -r name; do rabbitmqadmin -q delete queue name='${name}'; done < q2.txt")
        cmd = "rabbitmqadmin -f tsv -q list queues name > q2.txt; while read -r name; do rabbitmqadmin -q delete queue name=\"${name}\"; done < q2.txt"
        #cmd = "ls -la; echo 'salut'; lss"
        yield self.run_subprocess(cmd)

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
            except StreamClosedError:
                break
            else:
                self.write(data)
                self.flush()


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8899)
    tornado.ioloop.IOLoop.current().start()