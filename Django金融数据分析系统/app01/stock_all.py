import pandas as pd

import tushare as ts
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine


pro = ts.pro_api()

#查询当前所有正常上市交易的股票列表
cn = create_engine('mysql+pymysql://root:123456@localhost:3306/qwer?charset=utf8')
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data=pd.DataFrame(data)
print(data)
#data.to_sql(name='stock_info',con=cn ,index=False)






def stock_daily_get(code_wm,start_dt,end_dt):


    from sqlalchemy import create_engine

    #root后面为mysql数据库root密码

    cn = create_engine('mysql+pymysql://root:123456@localhost:3306/qwer?charset=utf8')

    #tushare.pro注册并获得token

    #设置tushare pro的token并获取连接

    ts.set_token('83ad002849edef4d3a054a27aa1d5387cc49d707956a5dc163e888a3')

    pro = ts.pro_api()


    stock_fields = 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'

    df = pro.daily(ts_code=code_wm, start_date=start_dt, end_date=end_dt,fields=stock_fields)

    df=df[::-1]
    df['id']=range(len(df))
    df['ma5']=df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma15'] = df['close'].rolling(15).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma60'] = df['close'].rolling(60).mean()
    df.to_sql(name='stock_{}'.format(code_wm),con=cn,index=False)
    # with cn.connect() as con:
    #     try:
    #         con.execute('ALTER TABLE `stock_{}` ADD PRIMARY KEY (`id`);'.format(code_wm))
    #         print(code_wm)
    #     except:
    #         print(1)

    print('{}日线行情成功导入数据库'.format(code_wm))



if __name__=='__main__':



    start_dt = '20080726'

    end_dt = '20210731'
    for i in data['ts_code']:
        stock_daily_get(i,start_dt,end_dt)