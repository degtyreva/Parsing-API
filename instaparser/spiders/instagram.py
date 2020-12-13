
import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy



class InstagramSpider(scrapy.Spider):
    #атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = ' '
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['bigdata_and_ai', 'bigdata.msu']     #Пользователь, у которого собираем подписчиков и подписки. Можно указать список

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    # posts_hash = ''     #hash для получения данных по постах с главной страницы
    followers_hash = 'c76146de99bb02f6415203be841dd25a'     #hash для получения данных подписчиков
    following_hash = 'd04b0a864b4b54837c0d870b0e77e076'     #hash для получения данных подписок


    def parse(self, response:HtmlResponse):             #Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(                   #заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:  #Проверяем ответ после авторизации
            for el in self.parse_user:

                yield response.follow(
                    f'/{el}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': el}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)       #Получаем id пользователя
        variables = {'id': user_id,
                     'first': 12}                                      #12 постов. Можно больше (макс. 50)
        url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'    #Формируем ссылку для получения данных о подписчиках:
        url_following = f'{self.graphql_url}query_hash={self.following_hash}&{urlencode(variables)}'    # Формируем ссылку для получения данных о подписках:

        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}         #variables ч/з deepcopy во избежание гонок
        )

        yield response.follow(
            url_following,
            callback=self.user_following_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}  # variables ч/з deepcopy во избежание гонок
        )



    def user_following_parse(self, response: HtmlResponse, username, user_id, variables):  # подписки
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            url_following = f'{self.graphql_url}query_hash={self.following_hash}&{urlencode(variables)}'
            yield response.follow(
                url_following,
                callback=self.user_following_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        following = j_data.get('data').get('user').get('edge_follow').get('edges')

        for elem in following:
            item = InstaparserItem(
                account=username,
                username=elem['node']['username'],
                user_id=elem['node']['id'],
                photo=elem['node']['profile_pic_url'],
                type='following'
            )
        yield item

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):  # подписчики
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')

        for elem in followers:
            item = InstaparserItem(
                account=username,
                username=elem['node']['username'],
                user_id=elem['node']['id'],
                photo=elem['node']['profile_pic_url'],
                type='followers'
            )
        yield item

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')


