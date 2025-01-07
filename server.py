import os
import http.server
import socketserver
from peewee import SqliteDatabase
from peewee import Model, CharField, IntegerField

from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        msg = "Hello! you requested %s" % (self.path)
        self.wfile.write(msg.encode())


db = SqliteDatabase("database.sqlite")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)


db.connect()
db.create_tables([User])
db.close()

port = int(os.getenv("PORT", 80))
print("Listening on port %s" % (port))
httpd = socketserver.TCPServer(("", port), Handler)
httpd.serve_forever()
