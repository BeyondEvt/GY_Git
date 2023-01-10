import mysql.connector

connection = mysql.connector.connect(host='localhost',
                                     port='3306',
                                     user='root',
                                     password='Yxb2003Kst2004'
                                     )
cursor = connection.cursor() # 开始使用数据库

# # 创建数据库`qq`
# cursor.execute("CREATE DATABASE `qq`;")
# cursor.execute("DROP DATABASE `qq`;")

# 取得所有资料库名称
# cursor.execute("SHOW DATABASES;")



# 选择数据库
cursor.execute("USE `sql_turorial`;")

# 取得资料
cursor.execute("SELECT * FROM `USER`;")
records = cursor.fetchall()
for r in records:
    print(r)

# 停止使用
cursor.close()
connection.close()

# 即执行指令
# cursor.execute("")