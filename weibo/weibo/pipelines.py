# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.err

class WeiboPipeline(object):
    def process_item(self, item, spider):
        try:
            conn = pymysql.connect(host='127.0.0.1',user='root',passwd='123456',db='test',charset='utf8')
            cursor = conn.cursor()
            sql_create = '''
            create table if not exists weibo(num int auto_increment primary key,name varchar(20) unique,
            sex varchar(10),location varchar(10),certification varchar(50),
            id varchar(15) unique,follows int,articles int,fans int,
            brief varchar(50),url varchar(50)
            );
            '''
            cursor.execute(sql_create)

            sql_insert = '''
            insert into weibo(name,sex,location,certification,id,follows,articles,fans,brief,url) 
            values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'); '''\
            % (item['name'],item['sex'],item['location'],item['certification'],item['id'],
            item['follows'],item['articles'],item['fans'],item['brief'],item['url'])


            if item['name']:
                cursor.execute(sql_insert)

            conn.commit()
            cursor.close()
            conn.close()
            print('successful insert into ',item['name'])
        except Exception as e:
            print(item['name'],e)


