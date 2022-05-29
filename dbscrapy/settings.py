# -*- coding: utf-8 -*-

# 项目名
BOT_NAME = 'dbscrapy'

# USER_AGENT 默认是注释的，这个东西非常重要，如果不写很容易被判断为电脑，简单点洗一个Mozilla/5.0即可
# ROBOTSTXT_OBE：是否遵循机器人协议，默认是true，需要改为false，否则很多东西爬不
# CONCURRENT_REQUESTS 最大并发数，很好理解，就是同时允许开启多少个爬虫线程

SPIDER_MODULES = ['dbscrapy.spiders']
NEWSPIDER_MODULE = 'dbscrapy.spiders'

# 是否保存COOKIES，默认关闭，开机可以记录爬取过程中的COKIE，非常好用的一个参数
COOKIES_ENABLED = False

TELNETCONSOLE_ENABLED = False
LOG_LEVEL = 'ERROR'


# 访问完一个页面再访问下一个时需要等待的时间，默认为10秒
DOWNLOAD_DELAY = 10
DEFAULT_REQUEST_HEADERS = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie': 'SINAGLOBAL=1771210902711.764.1641005237806; ALF=1685268595; SCF=Aq-25cRQHvQ8SguS8IADmOgZpGPA9yeJZLT3WXhWmBfsqr9PNbiPwzLJjRFviVEGg4SsdAOdwejwDhcZNBkDypU.; _s_tentry=login.sina.com.cn; Apache=8847460505673.232.1653732598907; UOR=,,login.sina.com.cn; ULV=1653732598982:4:3:3:8847460505673.232.1653732598907:1653544699694; SSOLoginState=1653734433; SUB=_2A25PlYxxDeRhGeFL7VsQ-SzFyj2IHXVteRQ5rDV8PUJbkNB-LXTAkW1NfdJaJUUKP8vzkF-wKe6PTrybQT7TS3zO; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF3lbM_X05cB0PNHBP1y3dx5NHD95QNSKq4eK.E1K2pWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-c1K24eo.peBtt'
}
# 项目管道，300为优先级，越低越爬取的优先度越高
ITEM_PIPELINES = {
    'dbscrapy.pipelines.DbscrapyPipeline': 300,
    'dbscrapy.pipelines.CsvPipeline': 301,
    # 'dbscrapy.pipelines.MysqlPipeline': 302,
    # 'dbscrapy.pipelines.MongoPipeline': 303,
    # 'dbscrapy.pipelines.MyImagesPipeline': 304,
    # 'dbscrapy.pipelines.MyVideoPipeline': 305
}
# 要搜索的关键词列表，可写多个, 值可以是由关键词或话题组成的列表，也可以是包含关键词的txt文件路径，
# 如'keyword_list.txt'，txt文件中每个关键词占一行
KEYWORD_LIST = ['人工智能']  # 或者 KEYWORD_LIST = 'keyword_list.txt'
# 要搜索的微博类型，0代表搜索全部微博，1代表搜索全部原创微博，2代表热门微博，3代表关注人微博，4代表认证用户微博，5代表媒体微博，6代表观点微博
WEIBO_TYPE = 1
# 筛选结果微博中必需包含的内容，0代表不筛选，获取全部微博，1代表搜索包含图片的微博，2代表包含视频的微博，3代表包含音乐的微博，4代表包含短链接的微博
CONTAIN_TYPE = 0
# 筛选微博的发布地区，精确到省或直辖市，值不应包含“省”或“市”等字，如想筛选北京市的微博请用“北京”而不是“北京市”，想要筛选安徽省的微博请用“安徽”而不是“安徽省”，可以写多个地区，
# 具体支持的地名见region.py文件，注意只支持省或直辖市的名字，省下面的市名及直辖市下面的区县名不支持，不筛选请用“全部”
REGION = ['全部']
# 搜索的起始日期，为yyyy-mm-dd形式，搜索结果包含该日期
START_DATE = '2015-03-01'
# 搜索的终止日期，为yyyy-mm-dd形式，搜索结果包含该日期
END_DATE = '2020-03-01'
# 进一步细分搜索的阈值，若结果页数大于等于该值，则认为结果没有完全展示，细分搜索条件重新搜索以获取更多微博。数值越大速度越快，也越有可能漏掉微博；数值越小速度越慢，获取的微博就越多。
# 建议数值大小设置在40到50之间。
FURTHER_THRESHOLD = 46
# 图片文件存储路径
IMAGES_STORE = './'
# 视频文件存储路径
FILES_STORE = './'
# 配置MongoDB数据库
# MONGO_URI = 'localhost'
# 配置MySQL数据库，以下为默认配置，可以根据实际情况更改，程序会自动生成一个名为weibo的数据库，如果想换其它名字请更改MYSQL_DATABASE值
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'weibo'

