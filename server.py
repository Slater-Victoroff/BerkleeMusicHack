#!/usr/bin/python27
 
import tornado.platform.twisted
tornado.platform.twisted.install()

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
 
import time, os.path
import multiprocessing
import config
import numpy as np
#!/usr/bin/env python -B

import json

clients = []

class ViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('views/index.html')
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'New connection'
        clients.append(self)

    def on_message(self, message):
        print message
        
    def on_close(self):
        print 'Connection closed'
        clients.remove(self)
 
def main():
 
    result_queue = multiprocessing.Queue()

    # wait a second before sending first task
    time.sleep(1)
    app = tornado.web.Application(
        handlers=[
            (r"/", ViewHandler),
            (r"/ws", WebSocketHandler),
        ], static_path = config.static_path
    )

    server = tornado.httpserver.HTTPServer(app)
    server.listen(config.server_port)
    print "Listening on port:", config.server_port

    def tick():
        dx, dy, dr = np.random.randint(-50, 51), np.random.randint(-50, 51), np.random.randint(-10, 11)
        measurement = {'x': 300 + dx, 'y': 240 + dy, 'r': 20 + dr, 'note': np.random.randint(0, 5)}
        result_queue.put(measurement)

    def poll_monitor():
        try:
            if not result_queue.empty():
                result = result_queue.get()
                for c in clients:
                    c.write_message(json.dumps(result))
        except KeyboardInterrupt:
            tornado.ioloop.IOLoop.instance().stop()

    event_loop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(poll_monitor, 10, io_loop = event_loop)
    scheduler.start()

    datagen = tornado.ioloop.PeriodicCallback(tick, 500, io_loop = event_loop)
    datagen.start()

    event_loop.current().start()
 
if __name__ == "__main__":
    main()