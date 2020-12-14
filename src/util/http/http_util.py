# -*- coding:  utf-8 -*-
import requests
from requests import HTTPError
from functools import partial, partialmethod
from util.logger import Logger

logger = Logger(__name__)

TIMEOUT = 300


class HttpRequester:
    def __init__(self, base_url, timeout=TIMEOUT, headers={}):
        self.full_url_template = base_url + '/{}'
        self.headers = headers
        self.timeout = timeout
        self.cookies = requests.cookies.RequestsCookieJar()
        self.logger = logger

    def perform_request(self, api_path, method, params=None, json=None, **kwargs):
        full_url = self.full_url_template.format(api_path)
        self.logger.info('perform request.', {'method': method, 'url': full_url})
        response = perform_external_request(url=full_url,
                                            method=method,
                                            headers=self.headers,
                                            params=params,
                                            json=json,
                                            timeout=self.timeout,
                                            cookies=self.cookies,
                                            **kwargs)
        self.cookies.update(response.cookies)
        return response.json()

    perform_get = partialmethod(perform_request, method='GET')
    perform_post = partialmethod(perform_request, method='POST')
    perform_patch = partialmethod(perform_request, method='PATCH')
    perform_delete = partialmethod(perform_request, method='DELETE')


def perform_external_request(url,
                             method,
                             headers={},
                             params=None,
                             json=None,
                             timeout=TIMEOUT,
                             cookies=requests.cookies.RequestsCookieJar(), **kwargs):
    req = {'method': method, 'url': url, 'params': params, 'json': json}
    logger.log('Performing request.', req)
    try:
        resp = requests.request(headers=headers,
                                timeout=timeout,
                                cookies=cookies,
                                **req, **kwargs)
        if resp.status_code != requests.codes.ok:
            resp.raise_for_status()
        return resp
    except HTTPError as exception:
        logger.error('Failed to performing request.', {**req, 'error': exception, 'resp_content': resp.content})
        raise exception


perform_get_request = partial(perform_external_request, method='GET')
perform_post_request = partial(perform_external_request, method='POST')
