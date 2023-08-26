#coding=utf-8
import pymysql # 导入连接Mysql的库
# 连接数据库
connection = pymysql.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = 'hb123456',
        db='ALphapose_byguan',)

# # 通过获取到的数据库conection下的cursor()方法来创建游标操作数据库
# cursor = connection.cursor() # 开始使用数据库
# #cursor.execute("INSERT INTO `USER` (`USER_ID`,`PASSWARD`)VALUES('kangsiting', 666);")
# connection.commit()

def user_data():  # 该函数用于获取数据库的用户数据
        connection.ping(reconnect=True) # 若mysql连接失败就重新连接
        cursor = connection.cursor()  # 开始使用数据库
        connection.commit()  # 在SQL语句都成功执行后，调用Connection的commit()方法提交事务
        cursor.execute('SELECT * FROM `USERINFO`;')

        mysql_result = cursor.fetchall()  # 获取数据库的数据，数据类型为一个个元组
        mysql_result = sum(mysql_result, ())  # 将所有元组合成为一个大元组
        cursor.close()
        connection.close()  # 关闭与数据库的连接
        return mysql_result

def VIDEO_data():  # 该函数用于获取视频的标准数据
        connection.ping(reconnect=True) # 若mysql连接失败就重新连接
        cursor = connection.cursor()  # 开始使用数据库
        connection.commit()  # 在SQL语句都成功执行后，调用Connection的commit()方法提交事务
        cursor.execute('SELECT * FROM `VIDEO_INFO`;')

        mysql_result = cursor.fetchall()  # 获取数据库的数据，数据类型为一个个元组
        mysql_result = sum(mysql_result, ())  # 将所有元组合成为一个大元组
        cursor.close()
        connection.close()  # 关闭与数据库的连接
        return mysql_result

def VIDEO_data2():  # 该函数用于获取视频的基础数据
        connection.ping(reconnect=True) # 若mysql连接失败就重新连接
        cursor = connection.cursor()  # 开始使用数据库
        connection.commit()  # 在SQL语句都成功执行后，调用Connection的commit()方法提交事务
        cursor.execute('SELECT * FROM `VIDEO_ID`;')

        mysql_result = cursor.fetchall()  # 获取数据库的数据，数据类型为一个个元组
        mysql_result = sum(mysql_result, ())  # 将所有元组合成为一个大元组
        cursor.close()
        connection.close()  # 关闭与数据库的连接
        return mysql_result

def delete_VIDEO_data2(key):
        connection.ping(reconnect=True)  # 若mysql连接失败就重新连接
        cursor = connection.cursor()  # 开始使用数据库
        cursor.execute("DELETE FROM `video_id` WHERE video_id.Vname = '%s';" % key)
        connection.commit()  # 在SQL语句都成功执行后，调用Connection的commit()方法提交事务
        mysql_result = cursor.fetchall()  # 获取数据库的数据，数据类型为一个个元组
        mysql_result = sum(mysql_result, ())  # 将所有元组合成为一个大元组
        cursor.close()
        connection.close()  # 关闭与数据库的连接
        return mysql_result


# 存储用户信息
def insert_mysql(register_username, register_password):
        connection.ping(reconnect=True) # 若mysql连接失败就重新连接
        cursor = connection.cursor()  # 开始使用数据库
        connection.commit()
        # 执行sql语句，向数据库中的表格写入用户数据
        cursor.execute("INSERT INTO `USERINFO` (`USER_ID`,`PASSWARD`)VALUES('{}','{}')"
                       .format(register_username,register_password))
        connection.commit()   # 在SQL语句都成功执行后，调用Connection的commit()方法提交事务
        cursor.close()
        connection.close()

# 存储视频标准数据信息
def insert_mysql2(num, line, pt1, pt2, line1, line2, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move, time_start, time_end, tips):
        connection.ping(reconnect=True) # 若mysql连接失败就重新连接
        cursor = connection.cursor()  # 开始使用数据库
        connection.commit()
        # 执行sql语句，向数据库中的表格写入用户数据
        cursor.execute("INSERT INTO `VIDEO_INFO`  VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
                       .format(num, line, pt1, pt2, line1, line2, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move, time_start, time_end, tips))
        connection.commit()   # 在SQL语句都成功执行后，调用Connection的commit()方法提交事务
        cursor.close()
        connection.close()

# 存储视频基础参数数据
def insert_mysql3(Vname, Vtime):
        connection.ping(reconnect=True) # 若mysql连接失败就重新连接
        cursor = connection.cursor()  # 开始使用数据库
        connection.commit()
        # 执行sql语句，向数据库中的表格写入用户数据
        cursor.execute("INSERT INTO `VIDEO_ID` VALUES('{}','{}')"
                       .format(Vname, Vtime))
        connection.commit()   # 在SQL语句都成功执行后，调用Connection的commit()方法提交事务
        cursor.close()
        connection.close()

# print(user_data())
# print(user_data()[0::2])
#
# cursor.execute("INSERT INTO `USER` (`USER_ID`,`PASSWARD`)VALUES('{}',{})".format('aaa',111))
# connection.commit()
#

# connection.commit()
# cursor.execute('SHOW DATABASES;')
# mysql_result = cursor.fetchall()
# mysql_result = sum(mysql_result,()) # 将所有元组合成为一个大元组
# base = mysql_result[1]
# print(mysql_result)
# print(base)
#
# cursor.execute('SELECT * FROM `USER`;')
# mysql_result = cursor.fetchall()
# mysql_result = sum(mysql_result,()) # 将所有元组合成为一个大元组
# print(mysql_result)
# cursor.close()
# connection.close()
