import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os
from tornado import ioloop, iostream
import tornadio

LISTENERS = []

class SIOHandler(tornadio.SocketConnection):
    def on_open(self, *args, **kwargs):
        print "Client Connected"
        LISTENERS.append(self)

    def on_close(self):
        LISTENERS.remove(self)

    def on_message(self, message):
        for listener in LISTENERS:
            listener.send(message)

class Announcer(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        data = self.get_argument('data')
        for socket in LISTENERS:
            socket.send(data)
        self.write('Posted')

application = tornado.web.Application([
     tornadio.get_router(SIOHandler,
                                resource=r'socket',
                                extra_re="(?P<path>.*)",
                                extra_sep='/' ).route(),
    (r"/push", Announcer),
])

if __name__ == "__main__":
    application.listen(8888)
    ioloop.IOLoop.instance().start()
