# !/usr/bin/env python
# coding=utf-8

import requests
import pymongo
from nose.tools import with_setup
from SillyNews.app import *
import time
import json
import threading


def setup_func():
    connection = pymongo.Connection("localhost", 27017)
    db = connection.sillynews
    db.user.insert({"username": "testUsername",
                    "password": "testPassword"})
    connection.disconnect()


def teardown_func():
    connection = pymongo.Connection("localhost", 27017)
    connection.drop_database("sillynews")
    connection.disconnect()


@with_setup(setup_func, teardown_func)
def test_news_api():
    try:
        server_thread = threading.Thread(target=run)
        server_thread.setDaemon(False)
        server_thread.start()
        time.sleep(1)
        # get the user cookie
        r = requests.post("http://127.0.0.1:8888/login/",
                          data={"username": "testUsername",
                                "password": "testPassword"}, allow_redirects=False)
        user_cookie = r.cookies
        # test put
        r = requests.put("http://127.0.0.1:8888/api/news/")
        assert r.status_code == 403

        news = {"title": "test_title",
                "author": "test_author",
                "date": "test_date",
                "body": "test_body",
                "column": "test_column"}
        r = requests.put("http://127.0.0.1:8888/api/news/",
                         cookies=user_cookie,
                         data={"body": json.dumps(news)})
        assert r.status_code == 200

        # test get
        r = requests.get("http://127.0.0.1:8888/api/news/",
                         params={"title": "test_title"})
        news = r.json()
        assert news["title"] == "test_title"
        assert news["author"] == "test_author"
        assert news["body"] == "test_body"
        assert news["date"] == "test_date"
        assert news["column"] == "test_column"

        # test post
        change_news = {"title": "test_title",
                       "author": "change_author",
                       "date": "change_date",
                       "body": "change_body",
                       "column": "change_column"}

        r = requests.post("http://127.0.0.1:8888/api/news/",
                          cookies=user_cookie,
                          data={"body": json.dumps(change_news)})
        assert r.status_code == 200
        r = requests.get("http://127.0.0.1:8888/api/news/",
                         params={"title": "test_title"})
        assert r.status_code == 200
        assert r.json() == change_news

        # test delete
        r = requests.delete("http://127.0.0.1:8888/api/news/",
                            cookies=user_cookie,
                            params={"title": "test_title"})
        assert r.status_code == 200
        r = requests.get("http://127.0.0.1:8888/api/news/",
                         params={"title": "test_title"})
        assert r.status_code == 404
        # test 404
        r = requests.get("http://127.0.0.1:8888/api/news/")
        assert r.status_code == 404
        r = requests.post("http://127.0.0.1:8888/api/news/",
                          cookies=user_cookie)
        assert r.status_code == 404
        r = requests.delete("http://127.0.0.1:8888/api/news/",
                            cookies=user_cookie)
        assert r.status_code == 404
        r = requests.put("http://127.0.0.1:8888/api/news/",
                         cookies=user_cookie)
        assert r.status_code == 404

        # test column
        # test put column
        r = requests.put("http://127.0.0.1:8888/api/column/",
                         cookies=user_cookie)
        assert r.status_code == 404
        r = requests.put("http://127.0.0.1:8888/api/column/",
                         cookies=user_cookie,
                         data={"column": "test_column"})
        assert r.status_code == 200
        r = requests.put("http://127.0.0.1:8888/api/column/",
                         cookies=user_cookie,
                         data={"column": "test_column"})
        assert r.status_code == 404
        # test get column
        r = requests.get("http://127.0.0.1:8888/api/column/")
        assert r.status_code == 404
        r = requests.get("http://127.0.0.1:8888/api/column/",
                         params={"column": "test_column"})
        assert r.status_code == 200
        assert r.json() == []
        r = requests.get("http://127.0.0.1:8888/api/column/",
                         params={"column": "wrong_column"})
        assert r.status_code == 404
        # test get all column
        r = requests.get("http://127.0.0.1:8888/api/getallcolumn/")
        assert r.status_code == 200
        assert r.json() == [{"name": "test_column"}]
    finally:
        stop()
