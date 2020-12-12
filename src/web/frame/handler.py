# -*- coding:utf-8 -*-

import json
import inspect

from urllib import parse
from aiohttp import web

from src.project.errors import APIError
from src.util.logger import Logger

logger = Logger(__name__)


def _get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)


def _get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


def _has_named_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True


def _has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True


def _has_arg(fn):
    params = inspect.signature(fn).parameters
    return params.__len__() > 0


def _has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (
                param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError(
                'request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found


class RequestHandler(object):
    def __init__(self, app, func):
        self._app = app
        self._func = func
        self._has_arg = _has_arg(func)
        self._has_request_arg = _has_request_arg(func)
        self._has_var_kw_arg = _has_var_kw_arg(func)
        self._has_named_kw_args = _has_named_kw_args(func)
        self._named_kw_args = _get_named_kw_args(func)
        self._required_kw_args = _get_required_kw_args(func)

    async def __call__(self, request):
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest(reason='Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest(reason="JSON body must be object.")
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded'):
                    params = await request.post()
                    kw = dict(**params)
                elif ct.startswith('multipart/form-data'):
                    params = await request.multipart()
                    kw = dict()
                    kw['multipart'] = params
                else:
                    return web.HTTPBadRequest(reason='Unsupported Content-Type: %s' % request.content_type)
            elif request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not self._has_var_kw_arg and self._named_kw_args:
                # remove all unamed kw:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logger.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
        # check required kw:
        if self._required_kw_args:
            for name in self._required_kw_args:
                if name not in kw:
                    return web.HTTPBadRequest(reason='Missing argument: %s' % name)
        try:
            logger.debug('call with args: %s' % str(kw))
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)


class ResponseHandler(object):
    def __init__(self, app, handler):
        self._app = app
        self._handler = handler

    async def __call__(self, request):
        r = await self._handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            cookies = r.get('__cookies__')
            template = r.get('__template__')
            if template is None:
                resp = web.Response(
                    body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
            else:
                # r['__user__'] = request.__user__
                resp = web.Response(body=self._app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
            self._set_cookies(resp=resp, cookies=cookies)
            return resp
        if isinstance(r, int) and 600 > r >= 100:
            return web.Response(status=r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and 600 > t >= 100:
                return web.Response(status=t, body=str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp

    @staticmethod
    def _set_cookies(resp, cookies):
        if not cookies:
            return
        if isinstance(cookies, dict):
            resp.set_cookie(**cookies)
        if isinstance(cookies, list):
            for cookie in cookies:
                resp.set_cookie(**cookie)
