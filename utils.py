# -*- coding: utf-8 -*-
__author__ = 'suruomo'
__date__ = '2020/6/15 16:15'

import time
import pymysql


# 获取时间
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


def get_conn():
    # 建立连接
    conn = pymysql.connect(host="127.0.0.7", user="root", password="suruomo", db="cov", charset="utf8")
    # c创建游标A
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    """

    :param sql:
    :param args:
    :return:
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def get_c1_data():
    """

    :return: 返回大屏总统计数据div id=c1的数据
    """
    # 因为会更新多次数据，取时间戳最新的数据
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal),sum(dead) from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    return res[0]


def get_c2_data():
    """

    :return: 获取中国地图数据 id=c2数据
    """
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_l1_data():
    """

    :return: 获取左上角历史数据折线趋势图 id=l1数据
    """
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


def get_l2_data():
    """

    :return: 获取左下角新增趋势折线趋势图 id=l2数据
    """
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res


def get_r1_data():
    """

    :return: 获取右上角非湖北Top5统计图 id=r1数据
    """
    sql = 'select city,confirm from ' \
          '(select city,confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'order by confirm desc limit 5'
    res = query(sql)
    return res


def get_r2_data():
    """

    :return: 获取右下角词云图 id=r2数据，查询最新20条数据
    """
    sql = "select content from hotsearch order by id desc limit 20"
    res = query(sql)
    return res


if __name__ == "__main__":
    print(get_c1_data())
