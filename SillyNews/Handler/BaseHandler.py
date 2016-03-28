# !/usr/bin/env python
# coding=utf-8

from tornado.web import RequestHandler
import time


class BaseHandler(RequestHandler):
    def get_current_user(self):
        token = self.get_secure_cookie("user")
        if token is None:
            return None
        else:
            token = token.decode(encoding='UTF-8')
            split_token = token.split(":")
            if float(split_token[2]) - time.time() > 3600:
                self.redirect("/login/")
            self.set_secure_cookie("user",
                                   "%s:%s:%s" % (split_token[0], split_token[1], split_token[2]))
            return split_token[0]

    def get_login_url(self):
        return u'/login/'