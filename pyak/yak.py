"""yak.py - Describes the yak model of the API"""


import base64
import hmac
import json
import os
import requests
import time
import urllib
from decimal import Decimal
from hashlib import sha1, md5
from random import randrange


def parse_time(timestr):
    format = "%Y-%m-%d %H:%M:%S"
    return time.mktime(time.strptime(timestr, format))


class Yak:

    def __init__(self, raw, client):
        self.client = client
        self.poster_id = raw["posterID"]
        self.hide_pin = bool(int(raw["hidePin"]))
        self.message_id = raw["messageID"]
        self.delivery_id = raw["deliveryID"]
        self.longitude = raw["longitude"]
        self.comments = int(raw["comments"])
        self.time = parse_time(raw["time"])
        self.latitude = raw["latitude"]
        self.likes = int(raw["numberOfLikes"])
        self.message = raw["message"]
        self.type = raw["type"]
        self.liked = int(raw["liked"])
        self.reyaked = raw["reyaked"]

        # Yaks don't always have a handle
        try:
            self.handle = raw["handle"]
        except KeyError:
            self.handle = None

        # For some reason this seems necessary
        self.message_id = self.message_id.replace('\\', '')

    def upvote(self):
        if self.liked == 0:
            self.liked += 1
            self.likes += 1
            return self.client.upvote_yak(self.message_id)

    def downvote(self):
        if self.liked == 0:
            self.liked -= 1
            self.likes -= 1
            return self.client.downvote_yak(self.message_id)

    def report(self):
        return self.client.report_yak(self.message_id)

    def delete(self):
        if self.poster_id == self.client.id:
            return self.client.delete_yak(self.message_id)

    def add_comment(self, comment):
        return self.client.post_comment(self.message_id, comment)

    def get_comments(self):
        return self.client.get_comments(self.message_id)

