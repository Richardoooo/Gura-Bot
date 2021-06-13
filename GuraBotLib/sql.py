###库###

import pymysql

###检查数据库这个人的资料
def checkdb(account,item):
    conn = pymysql.connect(host='localhost',user='root',password='richard5296867',db="qqmember",charset='utf8mb4')
    try:
        cur = conn.cursor()
        cur.execute('SELECT {} FROM qqbot where qqid={}'.format(item,account))
        result = cur.fetchall()
        if len(result) == 0 :
            return 0
        else:
            return result[0][0]
    except Exception as e:
        print("出问题了",e)
        pass
    finally:
        cur.close()
        conn.close()

###更新数据库
def updatedb(account,item,value):
    #item:你要改的数值,pull,like之类的
    conn = pymysql.connect(host='localhost',user='root',password='richard5296867',db="qqmember",charset='utf8mb4')
    try:
        cur = conn.cursor()
        cur.execute('select {} from qqbot where qqid={}'.format(item, account))
        result = cur.fetchall()
        if len(result) == 0:
            #如果没有则新建  
            cur.execute('insert into qqbot (qqid,good,times,pull,admin,sign_in,game_1) values({},0,0,0,0,0,0)'.format(account))
            cur.execute('update qqbot set {}={} where qqid={}'.format(item, value, account))
            conn.commit()
            return 1
        else:
            cur.execute('update qqbot set {}={} where qqid={}'.format(item, value, account))
            conn.commit()
    except Exception as e:
        print(e)
        return "cnmd 数据库出问题了",e
        pass
    finally:
        cur.close()
        conn.close()


##重置
def reset():
    conn = pymysql.connect(host='localhost',user='root',password='richard5296867',db="qqmember",charset='utf8mb4')
    try:
        cur = conn.cursor()
        cur.execute('update qqbot set times = 0 ,pull = 0,sign_in = 0, game_1 = 0')
        conn.commit()
        return "重置好啦主人"
    except Exception as e:
        print(e)
        return "cnmd 数据库出问题了",e
        pass
    finally:
        cur.close()
        conn.close()


