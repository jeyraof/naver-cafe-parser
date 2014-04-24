# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen


def param_to_dic(url='?'):
    tmp = dict()
    param_line = url.split('?', 1)[1]
    param_list = param_line.split('&')
    for param in param_list:
        par = param.split('=')
        tmp[par[0]] = par[1]
    return tmp


def get_html_from_url(url=None, headers=None):
    if url:
        r = Request(url=url)
        if headers:
            r.headers = headers
        resp = urlopen(r, timeout=30)
        return resp.read()

    else:
        return None