# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import re
from weibo.items import WeiboItem

class Spider1Spider(scrapy.Spider):
    name = 'spider_1'
    # allowed_domains = ['weibo.com']

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def start_requests(self):  # 模拟成浏览器访问
        yield Request('https://passport.weibo.cn/signin/login',callback=self.parse,headers=self.header,dont_filter=True)

    def parse(self, response):
        #输入用户名、密码
        form_data = {
            'username' : '*******',
            'password' : '*******'
        }
        yield scrapy.FormRequest(
                        url='https://passport.weibo.cn/sso/login',
                        headers=self.header,formdata=form_data,callback=self.next,dont_filter=True)

    #关注列表
    following = {}
    def next(self,response):
        data = json.loads(response.text)
        # Cookie = response.request.headers.getlist('Cookie')

        #获取登录后服务器返回的cookie
        cookie = response.headers.getlist('Set-Cookie')

        #将其转换成scrapy支持的cookie格式
        itemdict = {}
        try:
            for i in cookie:
                items = str(i,'utf-8').split(';')
                for item in items:
                    try:
                        key = item.split('=')[0].replace(' ','')
                        value = item.split('=')[1]
                        itemdict[key] = value
                    except:
                        continue
        except Exception as e:
            print(e)

        #关注者界面
        url = 'https://weibo.cn/%s/follow' % data['data']['uid']
        for i in range(1,4):
            page_url = url + '?page=' + str(i)
            try:
                yield Request(page_url,callback=self.parse2,headers=self.header,
                              meta={'cookie':itemdict},cookies=itemdict)
            except:
                continue

    pattern = re.compile(r'<td valign="top"><a href="(.*?)">(.*?)</a>',re.S)

    searched = []
    def parse2(self,response):
        item = WeiboItem()
        try:
            data = str(response.body,'utf-8')
        except:
            data = str(response.body,'gbk')


        for i in re.findall(self.pattern,data):
            key = i[1]
            value = i[0]
            self.following[key] = value


        for i in self.following:
            if i not in self.searched:
                self.searched.append(i)
                yield Request(url=self.following[i],headers=self.header,
                              cookies=response.meta['cookie'],
                              callback=self.parse3)

    pattern_name = re.compile('<title>(.*?)的微博</title>',re.S)
    pattern_cert = re.compile('"ctt">认证：(.*?)</span>',re.S)
    pattern_sex = re.compile(r'alt="头像".*?>&nbsp;(.*?)<span class="cmt">已关注',re.S)
    pattern_info = re.compile('送Ta会员.*?微博\[(.*?)\].*?关注\[(.*?)\].*?粉丝\[(.*?)\]',re.S)
    pattern_brief = re.compile('已关注.*?width:50px;">(.*?)</span>.*?私信')

    def parse3(self,response):
        item = WeiboItem()
        try:
            data = str(response.body,'utf-8')
        except:
            data = str(response.body,'gbk')

        item['name'] = re.findall(self.pattern_name,data)[0]
        item['url'] = response.url
        item['id'] = response.url.split('/')[-1]
        try:
            brief = re.findall(self.pattern_brief,data)[0]
        except:
            brief = ''
        if brief:
            item['brief'] = brief
        else:
            item['brief'] = 'none'
        try:
            cert = re.findall(self.pattern_cert,data)[0]
        except:
            cert = ''
        if cert:
            item['certification'] = cert
        else:
            item['certification'] = 'none'
        try:
            info = re.findall(self.pattern_info,data)[0]
            try:
                sl = re.findall(self.pattern_sex, data)[0].split('/')
                item['sex'] = sl[0]
                item['location'] = sl[1].split('&')[0].strip()
            except:
                item['sex'] = 'none'
                item['location'] = 'none'
            try:
                item['articles'] = info[0]
                item['follows'] = info[1]
                item['fans'] = info[2]
            except:
                item['articles'] = 'none'
                item['follows'] = 'none'
                item['fans'] = 'none'
        except Exception as e:
            print(item['name'],e)

        yield item




