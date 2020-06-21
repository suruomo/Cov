import pymysql
import traceback
import datetime
import time
from spider import get_tencent_data, get_baidu_hot


# pymysql使用
def get_conn():
    # 建立连接
    conn = pymysql.connect(host="127.0.0.1", user="root", password="suruomo", db="cov", charset="utf8")
    # 创建游标，默认是元组型
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# 清空数据库数据，重新爬取
def delete_all():
    cursor = None
    conn = None
    try:
        conn,cursor=get_conn()
        sql="DELETE  FROM details"
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("删除详情数据成功")
        sql = "DELETE  FROM history"
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("删除历史数据成功")
        sql = "DELETE  FROM hotsearch"
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("删除热搜数据成功")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

# 定义更新细节函数
def update_details():
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]  # 1代表最新数据
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,suspect,heal,dead) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
        # 对比当前最大时间戳
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}更新到最新数据")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# 插入历史数据
def insert_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0代表历史数据字典
        print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add"), v.get("importedCase"), v.get("importedCase_add"),
                                 v.get("noInfect"), v.get("noInfect_add")])
        conn.commit()
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# 更新历史数据
def update_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0代表历史数据字典
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add"), v.get("importedCase"), v.get("importedCase_add"),
                                     v.get("noInfect"), v.get("noInfect_add")])
        conn.commit()
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# 插入数据库
def update_hotsearch():
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()}开始更新数据")
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))
        conn.commit()
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# def spider():
#     # 把爬虫程序放在这个类里 zhilian_spider 是爬虫的name
#     cmdline.execute('scrapy crawl spider'.split())


# 想几点更新,定时到几点
def main(h=4, m=22):
    while True:
        now = datetime.datetime.now()
        # print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            delete_all()
            update_details()
            insert_history()
            update_history()
            update_hotsearch()
            # spider()
        # 每隔60秒检测一次
        time.sleep(60)


if __name__ == '__main__':
    main()
