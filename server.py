#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import subprocess
import cgi
import thread

PORT_NUMBER = 8080
command = False

# dictionary outside of the function so it doesn't rebuild dictionary on every function call
commands_dictionary = {
    'pause': 'pause',
    'stop': 'stop',
    '+5sec': 'seek 5000000',
    '-5sec': 'seek -5000000',
    '+30sec': 'seek 30000000',
    '-30sec': 'seek -30000000',
    '+1min': 'seek 60000000',
    '-1min': 'seek -60000000',
    '+10min': 'seek 600000000',
    '-10min': 'seek -600000000',
    'dark': 'setalpha 150',
    'light': 'setalpha 255',
}


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


def get_command(post_parameter):
    return commands_dictionary.get(post_parameter, False)


def server_thread():
    try:
        server = HTTPServer(('', PORT_NUMBER), ServerHandler)

        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()


thread.start_new_thread(server_thread, ())


while True:
    if command:
        parameter = get_command(command.value)

        if parameter:
            subprocess.Popen(['./dbuscontroll.sh %s' % parameter], shell=True)
        command = False
