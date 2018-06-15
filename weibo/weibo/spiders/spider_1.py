# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import re
from weibo.items import WeiboItem

class Spider1Spider(scrapy.Spider):
    name = 'spider_1'
    start_urls = ['https://passport.weibo.cn/signin/login']

    def parse(self, response):
        print(response.request.headers.get('Cookie'))
        #输入用户名、密码
        form_data = {
            'username' : '******',
            'password' : '******'
        }
        yield scrapy.FormRequest(url='https://passport.weibo.cn/sso/login',
                        formdata=form_data,callback=self.next)

    #关注列表
    def next(self,response):
        print(response.request.headers.get('Cookie'))
        data = json.loads(response.text)
        #关注者界面
        url = 'https://weibo.cn/%s/follow' % data['data']['uid']
        for i in range(1,2):
            page_url = url + '?page=' + str(i)
            try:
                yield Request(page_url,callback=self.parse2,)
            except:
                continue

    pattern_url = re.compile(r'<td valign="top"><a href="(.*?)"',re.S)
    pattern_link_uid = re.compile('uid=([0-9]{10})')
    def parse2(self,response):
        print(response.request.headers.get('Cookie'))
        data = str(response.body,'utf-8')
        urls = re.findall(self.pattern_url,data)
        for i in urls:
            yield Request(url=i,callback=self.parse3)


    pattern_name = re.compile('<title>(.*?)的微博</title>',re.S)
    pattern_id =re.compile('href="/im/chat\?uid=(.*?)&amp;rl=0">私信',re.S)
    pattern_cert = re.compile('"ctt">认证：(.*?)</span>',re.S)
    pattern_sex = re.compile(r'alt="头像".*?>&nbsp;(.*?)&nbsp',re.S)
    pattern_sex2 = re.compile(r'alt="头像".*?&nbsp;(.*?)&nbsp',re.S)
    pattern_info = re.compile('送Ta会员.*?微博\[(.*?)\].*?关注\[(.*?)\].*?粉丝\[(.*?)\]',re.S)
    pattern_brief = re.compile('已关注.*?width:50px;">(.*?)</span>.*?私信')
    pattern_brief2 = re.compile('加关注.*?width:50px;">(.*?)</span>.*?私信')
    #保存数据
    def parse3(self,response):
        # print(response.request.headers.get('User-Agent'))
        item = WeiboItem()
        data = str(response.body,'utf-8')

        item['name'] = re.findall(self.pattern_name,data)[0]
        item['url'] = response.url
        item['id'] = re.findall(self.pattern_id,data)[0]
        try:
            brief = re.findall(self.pattern_brief,data)[0]
        except:
            try:
                brief = re.findall(self.pattern_brief2,data)[0]
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
            except:
                sl = re.findall(self.pattern_sex2, data)[0].split('/')
            item['sex'] = sl[0]
            item['location'] = sl[1].strip()
            item['articles'] = info[0]
            item['follows'] = info[1]
            item['fans'] = info[2]
        except Exception as e:
            print(item['name'],e)
        yield item
   


