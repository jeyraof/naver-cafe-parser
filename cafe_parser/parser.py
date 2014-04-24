# -*- coding: utf-8 -*-


from urllib2 import Request, urlopen
from lxml import html


class Cafe(object):
    """
    cafe object
    """

    def __init__(self, cafe_id=None):
        self.cafe_id = cafe_id.split('/')[-1] if '/' in cafe_id else cafe_id
        self.club_id = self.get_club_id()

    def get_club_id(self):
        url = self.build_url()
        html_string = self.get_html_from_url(url)
        dom = html.fromstring(html_string)

        ic_info = dom.cssselect('a#ic_info')
        ic_info = ic_info.pop() if len(ic_info) == 1 else None

        club_id = ic_info.get('href', None)
        club_id = club_id.split('=')[-1] if '=' in club_id else None

        return club_id

    def build_url(self):
        if self.cafe_id:
            return 'http://m.cafe.naver.com/' + str(self.cafe_id)
        else:
            return None

    @staticmethod
    def get_html_from_url(url=None):
        if url:
            r = Request(url=url)
            resp = urlopen(r, timeout=30)
            return resp.read()

        else:
            return None