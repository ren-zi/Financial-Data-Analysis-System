import tushare as ts
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import pandas as pd
#select top 1 * from a
ts.set_token('83ad002849edef4d3a054a27aa1d5387cc49d707956a5dc163e888a3')

pro = ts.pro_api()

#查询当前所有正常上市交易的股票列表
cn = create_engine('mysql+pymysql://root:123456@localhost:3306/qwer?charset=utf8')
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data=pd.DataFrame(data)

#data.to_sql(name='stock_info',con=cn ,index=False)

db = pymysql.connect("localhost", "root", "123456", "qwer")
cursor = db.cursor()
df_all = pd.DataFrame()
# a=[]
# a=pd.DataFrame(columns=["ts_code", "symbol", "name", "area", "industry","list_date", "ts_code(1)", "trade_date", "open", "high","low", "close", "pre_close", "change", "pct_chg","vol", "amount", "id"])
for i in data['ts_code']:
    sql = "SELECT * FROM STOCK_INFO A INNER JOIN `stock_{}.sz` B ON A.ts_code=B.ts_code LIMIT 1".format(i[:6])
    try:
        df=pd.read_sql(sql, db)
        print(i)
        df_all = df_all.append(df, ignore_index=True)
        # 执行SQL语句
    except:
        print('1')
    # cursor.execute(sql)
    # # 获取所有记录列表
    # results = cursor.fetchone()
    # columnDes = cursor.description  # 获取连接对象的描述信息
    # columnNames = [columnDes[i][0] for i in range(len(columnDes))]
    # df = pd.DataFrame([list(i) for i in results], columns=columnNames)


        # df_all = df_all.append(results, ignore_index=True)

        # sql= "INSERT INTO STOCK_INDEX(TS_CODE,SYMBOL,NAME,AREA, INDUSTRY,TS_CODE(1),TREADE_DATE,OPEN,HIGH,LOW,CLOSE,PRE_CLOSE,CHANGE,PCT_CHG,VOL,AMOUNT,ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (results)
        # try:
        #     # 执行sql语句
        #     cursor.execute(sql)
        #     # 执行sql语句
        #     db.commit()
        # except:
        #     # 发生错误时回滚
        #     db.rollback()
        #
        # # 关闭数据库连接

    #results = pd.DataFrame(list(results), columns=["ts_code", "symbol", "name", "area", "industry","list_date", "ts_code(1)", "trade_date", "open", "high","low", "close", "pre_close", "change", "pct_chg","vol", "amount", "id"])
    # results = pd.DataFrame(results)
    # results = pd.DataFrame(results)



    # 关闭数据库连接
df_all.to_excel(r"C:\Users\hp\Desktop\首页4.xlsx",index=False)
db.close()


# a RIGHT JOIN STOCK_.{} B WHERE a.ts_code=B.ts_code .format(i.upper())