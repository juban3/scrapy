import pymysql

class mysqldb(object):
    def __init__(self):

    #连接数据库
        db = pymysql.connect(
            host = '106.14.31.146',
            port = 3306,
            user = 'scrapy',
            passwd = 'Scrapy@123',
            db = 'read_books'
        )

        #创建游标
        self.cursor = db.cursor()

    def process_getbook(self):
#sql语句
        sql = 'select bookName,edition from books;'
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
        self.db.close()
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
