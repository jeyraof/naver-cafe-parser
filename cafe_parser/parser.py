# -*- coding: utf-8 -*-


from lxml import html

from helper import param_to_dic, get_html_from_url


class Cafe(object):
    """
    cafe object
    """

    def __init__(self, cafe_id):
        self.cafe_id = cafe_id.split('/')[-1] if '/' in cafe_id else cafe_id
        self.club_id = self.get_club_id()

    def get_club_id(self):
        url = self.build_url()
        html_string = get_html_from_url(url)
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


class Article(object):
    """
    article object
    """

    def __init__(self, club_id, article_id, url=None):
        if url:
            param = param_to_dic(url)
            self.club_id = param.get('club_id', None)
            self.article_id = param.get('article_id', None)

        else:
            self.club_id = club_id
            self.article_id = article_id

        self.fetched = False
        self._author = None
        self._title = None
        self._created_at = None
        self._content = None

    def fetch(self):
        url = 'http://m.cafe.naver.com/ArticleRead.nhn?clubid=%s&articleid=%s' % (self.club_id, self.article_id)
        html_string = get_html_from_url(url=url, headers={'Referer': 'http://search.naver.com'})

        dom = html.fromstring(html_string)

        post_tit = dom.cssselect('div.post_tit h2')
        if len(post_tit) > 0:
            post_tit = post_tit[0]
        self._title = post_tit.text.strip()

        # im = dom.cssselect('span.im')
        # if len(im) > 0:
        #     im = im[0]
        # print im

    @property
    def author(self):
        if not self.fetched:
            self.fetch()
        return self._author

    @property
    def title(self):
        if not self.fetched:
            self.fetch()
        return self._title

    @property
    def created_at(self):
        if not self.fetched:
            self.fetch()
        return self._created_at

    @property
    def content(self):
        if not self.fetched:
            self.fetch()
        return self._content