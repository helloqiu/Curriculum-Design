# !/usr/bin/env python
# coding=utf-8
from tornado.web import RequestHandler
import time


class LoginHandler(RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        self.write("Login")

    async def post(self):
        username = self.get_arguments("username")
        password = self.get_arguments("password")
        user = self.db.user.find({
            "username": username[0], "password": password[0]
        })
        user = await user.to_list(None)
        if user is [] or user is None:
            self.redirect("/login/?login=false")
        else:
            user = user[0]
            self.set_secure_cookie(
                "user", "%s:%s:%s" % (user["username"], user["password"], time.time()))
            self.redirect("/manage/")

    def put(self):
        self.get()
