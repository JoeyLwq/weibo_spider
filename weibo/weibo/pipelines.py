# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.err

class WeiboPipeline(object):
    def open_spider(self,spider):
        print('spider open')
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='test', charset='utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('drop table weibo;')
        sql_create = '''
                    create table if not exists weibo(num int auto_increment primary key,name varchar(20) unique,
                    sex varchar(10),location varchar(10),certification varchar(50),
                    id varchar(20) unique,follows int,articles int,fans int,
                    brief varchar(50),url varchar(50)
                    );
                    '''
        self.cursor.execute(sql_create)

    def process_item(self, item, spider):
        try:
            sql_insert = '''
            insert into weibo(name,sex,location,certification,id,follows,articles,fans,brief,url)
            values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'); '''\
            % (item['name'],item['sex'],item['location'],item['certification'],item['id'],
            item['follows'],item['articles'],item['fans'],item['brief'],item['url'])
            if item['name']:
                self.cursor.execute(sql_insert)
            self.conn.commit()
            # print('successful insert into ',item['name'])
        except Exception as e:
            print(item['name'],e)

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
        print('spider close')


