import pymysql
from scrapy import crawler

from bdWenku import settings


class mysqldb(object):
    def __init__(self):
    #连接数据库
        db = pymysql.connect(
                host = settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE
            )

        #创建游标
        self.cursor = db.cursor()

    def process_getbook(self):
#sql语句
        sql = 'select id,bookName,edition,author,press from books;'
        self.cursor.execute(sql)

        try:
            # 执行SQL语句
            self.cursor.execute(sql)

            # 获取所有记录列表
            results = self.cursor.fetchall()
            '''
            for row in results:
                book_name = row[0]
                deition = row[1]
        
                # 打印结果
                print("book_name=%s,deition=%s" % \
                      (book_name, deition))
            '''
        except:
            print("Error: unable to fetch data")

        # 关闭数据库连接
        self.cursor.close()
        return results


    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into mingyan(tag, cont)
            value (%s, %s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['tag'],  # item里面定义的字段和表字段对应
             item['cont'],))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回
