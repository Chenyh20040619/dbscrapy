# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline

from dbscrapy import settings
import os
import csv

class CsvPipeline(object):
    def process_item(self, item, spider):
        base_dir = '结果文件' + os.sep + item['keyword']
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + item['keyword'] + '.csv'
        if not os.path.isfile(file_path):
            is_first_write = 1
        else:
            is_first_write = 0
        if item:
            with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if is_first_write:
                    header = [
                        'id', 'bid', 'user_id', '用户昵称', '微博正文', '头条文章url',
                        '发布位置', '艾特用户', '话题', '转发数', '评论数', '点赞数', '发布时间',
                        '发布工具', '微博图片url', '微博视频url', 'retweet_id'
                    ]
                    writer.writerow(header)
                # {'weibo': weibo, 'keyword': keyword}
                writer.writerow([item['weibo'][key] for key in item['weibo'].keys()])
        return item
class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if len(item['weibo']['pics']) == 1:
            yield scrapy.Request(item['weibo']['pics'][0],
                                 meta={
                                     'item': item,
                                     'sign': ''
                                 })
        else:
            sign = 0
            for image_url in item['weibo']['pics']:
                yield scrapy.Request(image_url,
                                     meta={
                                         'item': item,
                                         'sign': '-' + str(sign)
                                     })
                sign += 1

    def file_path(self, request, response=None, info=None):
        image_url = request.url
        item = request.meta['item']
        sign = request.meta['sign']
        base_dir = '结果文件' + os.sep + item['keyword'] + os.sep + 'images'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        image_suffix = image_url[image_url.rfind('.'):]
        file_path = base_dir + os.sep + item['weibo'][
            'id'] + sign + image_suffix
        return file_path


class MyVideoPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item['weibo']['video_url']:
            yield scrapy.Request(item['weibo']['video_url'],
                                 meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        base_dir = '结果文件' + os.sep + item['keyword'] + os.sep + 'videos'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + item['weibo']['id'] + '.mp4'
        return file_path

class MysqlPipeline(object):
    def open_spider(self, spider):
        try:
            import pymysql
            mysql_config = {
                'host': settings.MYSQL_HOST,
                'port': settings.MYSQL_PORT,
                'user': settings.MYSQL_USER,
                'password': settings.MYSQL_PASSWORD,
                'charset': 'utf8mb4'
            }
            self.create_database(mysql_config)
            mysql_config['db'] = settings.MYSQL_DATABASE
            self.db =pymysql.connect(**mysql_config)
            self.cursor = self.db.cursor()
            self.create_table()
        except ImportError:
            spider.pymysql_error = True
        except pymysql.OperationalError:
            spider.mysql_error = True

    def create_database(self, mysql_config):
        import pymysql
        sql = """CREATE DATABASE IF NOT EXISTS %s DEFAULT
                    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""" % settings.MYSQL_DATABASE
        db = pymysql.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute(sql)
        cursor.close()
    def create_table(self):
        sql = """
                        CREATE TABLE IF NOT EXISTS weibo (
                        id varchar(20) NOT NULL,
                        bid varchar(12) NOT NULL,
                        user_id varchar(20),
                        screen_name varchar(30),
                        text varchar(2000),
                        article_url varchar(100),
                        topics varchar(200),
                        at_users varchar(1000),
                        pics varchar(3000),
                        video_url varchar(1000),
                        location varchar(100),
                        created_at DATETIME,
                        source varchar(30),
                        attitudes_count INT,
                        comments_count INT,
                        reposts_count INT,
                        retweet_id varchar(20),
                        PRIMARY KEY (id)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self.cursor.execute(sql)
    def process_item(self, item):
        data = dict(item['weibo'])
        data['pics'] = ', '.join(data['pics'])
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                             DUPLICATE KEY UPDATE""".format(table='weibo',
                                                            keys=keys,
                                                            values=values)
        update = ','.join([" {key} = {key}".format(key=key) for key in data])
        sql += update
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
        except Exception:
            self.db.rollback()
        return item
    def close_spider(self, spider):
        try:
            self.db.close()
        except Exception:
            pass

class DbscrapyPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['weibo']['id'] in self.ids_seen:
            raise DropItem("过滤重复微博: %s" % item)
        else:
            self.ids_seen.add(item['weibo']['id'])
            return item
