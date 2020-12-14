# -*- coding:utf-8 -*-

from aiohttp_session import get_session

from util.code_image import generate_verification_code
from util.logger import with_logger, Logger
from web.frame.wrapper import *

logger = Logger(__name__)


@with_logger(logger=logger)
@get("/")
async def index(request):
    return {
        '__template__': 'login.html',
        'users': [{"name": "11", "email": "22@163.com"}, {"name": "112", "email": "221@qq.com"}]
    }


@with_logger(logger=logger)
@get("/user/{ids}")
async def user():
    return "hello world"


@with_logger(logger=logger)
@get("/refreshCode")
async def refresh_code(request):
    session = await get_session(request=request)
    code_img, code_str = generate_verification_code()
    session['code_str'] = code_str
    return code_img


@get("/upload")
async def upload_page(request):
    return {
        '__template__': 'upload.html',
        'users': [{"name": "11", "email": "22@163.com"}, {"name": "112", "email": "221@qq.com"}]
    }


@post("/upload")
async def upload(**kw):
    multipart = kw['multipart']
    multipart_file = await multipart.next()

    filename = multipart_file.filename if multipart_file.filename else 'test'
    size = 0
    with open(filename, 'wb') as f:
        while True:
            chunk = await multipart_file.read_chunk()  # 默认是8192个字节。
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    text = {'res': '上传成功'}

    return "success"
