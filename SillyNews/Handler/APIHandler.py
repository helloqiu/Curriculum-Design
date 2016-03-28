# !/usr/bin/env python
# coding=utf-8

from SillyNews.Handler.BaseHandler import BaseHandler
import tornado.web
import json


class APIHandler(BaseHandler):
    def initialize(self, db):
        self.db = db


class APINewsHandler(APIHandler):
    '''The RequestHandler for news apis'''

    async def get(self):
        news_title = self.get_query_argument("title", None)
        if news_title is None:
            raise tornado.web.HTTPError(404)
        news = await self.db.news.find({"title": news_title}).to_list(None)
        if news == [] or news is None:
            raise tornado.web.HTTPError(404)
        else:
            news = news[0]
            self.write(json.dumps({"title": news["title"],
                                   "author": news["author"],
                                   "date": news["date"],
                                   "body": news["body"],
                                   "column": news["column"]}))

    @tornado.web.authenticated
    async def put(self):
        body = self.get_body_argument("body", None)
        if body is None:
            raise tornado.web.HTTPError(404)
        body = json.loads(body)
        await self.db.news.insert({"title": body["title"],
                                   "body": body["body"],
                                   "author": body["author"],
                                   "date": body["date"],
                                   "column": body["column"]})

    @tornado.web.authenticated
    async def post(self):
        body = self.get_body_argument("body", None)
        if body is None:
            raise tornado.web.HTTPError(404)
        body = json.loads(body)
        news = await self.db.news.find({"title": body["title"]}).to_list(None)
        if news is None:
            raise tornado.web.HTTPError(404)
        else:
            news = news[0]
            self.db.news.update({"_id": news["_id"]},
                                body)

    @tornado.web.authenticated
    async def delete(self):
        news_title = self.get_query_argument("title", None)
        if news_title is None:
            raise tornado.web.HTTPError(404)
        await self.db.news.remove({"title": news_title})