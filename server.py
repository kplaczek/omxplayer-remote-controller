#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import subprocess
import cgi
import thread
PORT_NUMBER = 8080
command = False


class ServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Define the default page
        if self.path == "/":
            self.path = "/server.html"

            status = subprocess.check_call(['./dbuscontroll.sh status'], shell=True)
            print status
        try:

            send_reply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                send_reply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                send_reply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                send_reply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                send_reply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                send_reply = True

            if send_reply:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404, '404: File Not Found: %s' % self.path)

    def do_POST(self):
        global command

        if self.path == "/controller":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })

            command = form['cmd'];

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return


def server_thread():
    try:
        server = HTTPServer(('', PORT_NUMBER), ServerHandler)

        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()


thread.start_new_thread(server_thread, ())

while True:
    if command:
        if command.value == 'pause':
            subprocess.Popen(['./dbuscontroll.sh pause'], shell=True)

        elif command.value == 'stop':
            subprocess.Popen(['./dbuscontroll.sh stop'], shell=True)

        elif command.value == '+5sec':
            subprocess.Popen(['./dbuscontroll.sh seek 5000000'], shell=True)
        elif command.value == '-5sec':
            subprocess.Popen(['./dbuscontroll.sh seek -5000000'], shell=True)
        elif command.value == '+30sec':
            subprocess.Popen(['./dbuscontroll.sh seek 30000000'], shell=True)
        elif command.value == '-30sec':
            subprocess.Popen(['./dbuscontroll.sh seek -30000000'], shell=True)
        elif command.value == '+1min':
            subprocess.Popen(['./dbuscontroll.sh seek 60000000'], shell=True)
        elif command.value == '-1min':
            subprocess.Popen(['./dbuscontroll.sh seek -60000000'], shell=True)
        elif command.value == '+10min':
            subprocess.Popen(['./dbuscontroll.sh seek 600000000'], shell=True)
        elif command.value == '-10min':
            subprocess.Popen(['./dbuscontroll.sh seek -600000000'], shell=True)
        elif command.value == 'dark':
            subprocess.Popen(['./dbuscontroll.sh setalpha 150'], shell=True)
        elif command.value == 'light':
            subprocess.Popen(['./dbuscontroll.sh setalpha 255'], shell=True)
        command = False
