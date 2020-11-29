# Description: 
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2020 by Kireev Georgiy

import datetime as dt

BASE_URL_PREFIX_V1 = '/api/v1'

FILE_HEAD_SIZE = 1024

SESSION_LIFETIME = dt.timedelta(hours=8)
PERSIST_SESSION_LIFETIME = dt.timedelta(days=150)


class AppGlobals(object):
    version = "0.0.0"
    name = "aio_blog"
    config = {}
