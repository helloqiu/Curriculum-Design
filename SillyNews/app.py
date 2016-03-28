# !/usr/bin/env python
# coding=utf-8

import tornado.ioloop
import tornado.web
from SillyNews.Handler.WebHandler import *
from SillyNews.Handler.APIHandler import *
import motor
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def make_app(db):
    return tornado.web.Application([
        (r'/api/news/',
         APINewsHandler, dict(db=db)),
        (r'/login/',
         LoginHandler, dict(db=db))
    ],
        default_host='',
        transforms=None,
        address="http://127.0.0.1:8888",
        cookie_secret=id_generator(64))


def run():
    '''Connect to the database and the username & password need change'''
    db = motor.motor_tornado.MotorClient().sillynews
    try:
        app = make_app(db)
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()
    finally:
        motor.motor_tornado.MotorClient().disconnect()


def stop():
    tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    run()
