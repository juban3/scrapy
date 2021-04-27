import pymysql

#连接数据库
db = pymysql.connect(
    host = '106.14.31.146',
    port = 3306,
    user = 'scrapy',
    passwd = 'Scrapy@123',
    db = 'read_books'
)


#创建游标
cursor = db.cursor()

#sql语句
sql = 'select bookName,edition from books;'
cursor.execute(sql)

try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表

    results = cursor.fetchall()
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
db.close()
