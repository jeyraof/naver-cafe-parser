# -*- coding: utf-8 -*-


from lxml import html

from .helper import param_to_dic, get_html_from_url


class Cafe(object):
    """
    cafe object
    """

    def __init__(self, cafe_id):
        self.cafe_id = cafe_id.split('/')[-1] if '/' in cafe_id else cafe_id
        self.club_id = self.get_club_id()

    def get_club_id(self):
        url = 'http://m.cafe.naver.com/' + str(self.cafe_id)
        html_string = get_html_from_url(url, headers={'Referer': 'http://search.naver.com'})
        dom = html.fromstring(html_string)

        ic_info = dom.cssselect('a#ic_info')
        ic_info = ic_info.pop() if len(ic_info) == 1 else None

        club_id = ic_info.get('href', None)
        club_id = club_id.split('=')[-1] if '=' in club_id else None

        return club_id

    def get_board_list(self):
        board_list = []
        page = 0
        while 1:
            page += 1
            url = 'http://m.cafe.naver.com/MenuList.nhn?firstViewingFavoriteCafe=false&' \
                  'search.clubid=%s&' \
                  'search.page=%s' % (self.club_id, page)
            html_string = get_html_from_url(url, headers={'Referer': 'http://search.naver.com'})
            dom = html.fromstring(html_string)

            menu_list = dom.cssselect('ul.lst3 a.tit')
            if len(menu_list) == 0:
                break

            for menu in menu_list:
                href = menu.get('href', '')

                if not 'menuid' in href:
                    continue

                param = param_to_dic(href)
                menu_id = param.get('search.menuid', None)
                board_name = menu.text_content().strip()
                board_type = param.get('search.boardtype', None)

                board_list.append((menu_id, board_name, board_type))

        return board_list


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
        self._title = None
        self._author = None
        self._content = None
        self.error = False

    def fetch(self):
        url = 'http://m.cafe.naver.com/ArticleRead.nhn?clubid=%s&articleid=%s' % (self.club_id, self.article_id)
        html_string = get_html_from_url(url=url, headers={'Referer': 'http://search.naver.com'})

        dom = html.fromstring(html_string)

        try:
            post_tit = dom.cssselect('div.post_tit h2')
            if len(post_tit) > 0:
                post_tit = post_tit[0]
            self._title = post_tit.text_content().strip()

            nick = dom.cssselect('a.nick')
            if len(nick) > 0:
                nick = nick[0]
            self._author = nick.text_content().strip()

            post_content = dom.cssselect('div#postContent')
            if len(post_content) > 0:
                post_content = post_content[0]
            self._content = html.tostring(post_content).strip()

            self.fetched = True

        except Exception as inst:
            self.error = True

    @property
    def title(self):
        if not self.fetched:
            self.fetch()
        return self._title

    @property
    def author(self):
        if not self.fetched:
            self.fetch()
        return self._author

    @property
    def content(self):
        if not self.fetched:
            self.fetch()
        return self._content
