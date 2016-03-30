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
        news = await self.db.news.find({"title": news_title}, {"_id": 0}).to_list(None)
        if news == [] or news is None:
            raise tornado.web.HTTPError(404)
        else:
            news = news[0]
            self.write(json.dumps(news))

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


class APIColumnHandler(APIHandler):
    '''The RequestHandler for column api'''

    @tornado.web.authenticated
    async def put(self):
        column_name = self.get_body_argument("column", None)
        if column_name is None:
            raise tornado.web.HTTPError(404)
        column = await self.db.column.find({"name": column_name}).to_list(None)
        if column != []:
            raise tornado.web.HTTPError(404)
        else:
            await self.db.column.insert({"name": column_name})

    async def get(self):
        column_name = self.get_query_argument("column", None)
        if column_name is None:
            raise tornado.web.HTTPError(404)
        column = await self.db.column.find({"name": column_name}).to_list(None)
        if column == []:
            raise tornado.web.HTTPError(404)
        articles = await self.db.article.find({"column": column_name},
                                              {"title": 1, "date": 1, "_id": 0}).to_list(None)
        self.write(json.dumps(articles))


class APIGetAllColumnHandler(APIColumnHandler):
    '''The RequestHandler for getAllColumn api'''

    async def get(self):
        columns = await self.db.column.find({}, {"name": 1, "_id": 0}).to_list(None)
        return_values = []
        for column in columns:
            articles = await self.db.article.find({"column": column["name"]},
                                                  {"title": 1, "date": 1, "_id": 0}).to_list(None)
            return_values.append({"name": column["name"], "articles": articles})
        self.write(json.dumps(return_values))
