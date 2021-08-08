from django.shortcuts import render,redirect
from  app01 import models
import json
from django.db.models.base import ModelState

from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
# Create your views here.
def index(request):
    if request.method == "POST":
        ts_code = request.POST.get('name', '000001.sz')
        ret=models.StockIndex.objects.get(ts_code=ts_code)



        return render(request,'stock_rearch.html',{"publisher_obj": ret})
    elif request.method =='GET':
        x=models.StockIndex.objects.all()
        paginator = Paginator(x, 10)  # 每页显示10条数据
        # print(paginator.count)  # 总数据条数
        # print(paginator.num_pages)  # 总页数
        # print(paginator.page_range)  # 页数范围

        current_page_num = int(request.GET.get('page', 1))  # 通过a标签的GET方式请求，默认显示第一页
        x = paginator.page(current_page_num)  # 获取当前页面的数据
        if x.has_previous():  # 当前页面是否有前一页
            print(x.previous_page_number())  # 当前页面的前一页页码
        if x.has_next():  # 当前页面是否有后一页
            print(x.next_page_number())  # 当前页面的后一页页码

        page_range = paginator.page_range
        if paginator.num_pages > 5:  # 页码只显示5页，总页数小于5页时，直接全部显示
            if current_page_num < 3:
                page_range = range(1, 6)
            elif current_page_num + 2 > paginator.num_pages:
                page_range = range(paginator.num_pages - 5, paginator.num_pages + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 3)

        return render(request, 'index.html',
                      {'x':x, 'page_range': page_range, 'current_page_num': current_page_num})

def draw(request):

    ts_code = request.GET.get('id')
    print(ts_code)
    a = ts_code.replace('.', '').title()
    a = a.replace(' ', '')
    x, x1 = test('Stock{}'.format(a))


    # print(a)
    # name='Stock{}'.format(a)
    # print(type(Stock000413Sz))
    # print(name,type(name))
    #user_db = getattr(models, 'Stock{}'.format(a))


    #getattr(models, 'Stock{}'.format(a)).objects.all()
    # with 'stock_'+ts_code as A:
    #     publisher_obj1 = models.A.objects.all()

     # 每页显示10条数据
    # print(paginator.count)  # 总数据条数
    # print(paginator.num_pages)  # 总页数
    # print(paginator.page_range)  # 页数范围


    return render(request,'darw.html',{'publisher_obj1':x,'publisher_obj':x1})


def test(requset):
    user_db_name = requset
    user_db = getattr(models, user_db_name)
    user_data = user_db.objects.all()
    user_data1 = user_db.objects.get(id='0')
    return user_data,user_data1

    # ret = serialize("json",ret)
    # print(ret)
def d_stoke(request):
    import pandas as pd
    ts_code = request.GET.get('id','000001.sz')
    print(ts_code)
    a = ts_code.replace('.', '').title()
    a = a.replace(' ', '')
    x, x1 = test('Stock{}'.format(a))
    ret = x

    json_list = []

    for row in ret:

        json_dict = {}
        # row = str(row)


        json_dict["id"] = row.id
        json_dict["ts_code"] = row.ts_code
        json_dict["trade_date"] = row.trade_date
        json_dict["open"] = row.open
        json_dict["high"] = row.high
        json_dict["low"] = row.low
        json_dict["close"] = row.close
        json_dict["pre_close"] = row.pre_close
        json_dict["change"] = row.change
        json_dict["pct_chg"] = row.pct_chg
        json_dict["vol"] = row.vol
        json_dict["amount"] = row.amount
        json_dict["ma5"] = row.ma5
        json_dict["ma10"] = row.ma10
        json_dict["ma15"] = row.ma15
        json_dict["ma20"] = row.ma20
        json_dict["ma60"] = row.ma60


        json_list.append(json_dict)


    ret1 = json.dumps(json_list)

    print(ret1,type(ret1))
    return render(request,'income.html',{"ret": json.dumps(ret1),'ts_code':ts_code})



def predict(request):
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    ts_code = request.GET.get('id','000001.sz')
    print(ts_code)
    a = ts_code.replace('.', '').title()
    a = a.replace(' ', '')
    x, x1 = test('Stock{}'.format(a))
    ret = x
    print(ret)
    from django_pandas.io import read_frame

    df = read_frame(ret)
    df=df.dropna()
    xs = df.drop([ 'id','ts_code','ma60', 'ma5', 'ma10', 'ma20', 'ma15'], 1)
    if len(xs)%2!=0:
        xs=xs.iloc[1:]
    print(df)
    xt = xs.T

    x = xs.index
    print(x)
    print(xt.index)
    train_x = xt[x[:int(len(x) / 2) - 1]]
    print(train_x)
    train_y = xt[x[int(len(x) / 2) - 1]]
    print(train_y)
    test_x = xt[x[int(len(x) / 2):len(x) - 1]]
    print(test_x)

    x_train = np.array(train_x)
    y_train = np.array(train_y)
    x_test = np.array(test_x)

    forest = RandomForestClassifier(criterion='entropy', n_estimators=10, random_state=1, n_jobs=2)
    forest.fit(x_train, y_train.astype('str'))
    y_test = forest.predict(x_test)
    print(y_test)
    y_test[0]='20210730'

    a=y_test[0]
    b=y_test[1]
    c = y_test[2]
    d = y_test[3]
    e = y_test[4]
    f = y_test[5]
    g = y_test[6]
    h = y_test[7]
    i = y_test[8]
    j = y_test[9]

    print(y_test)
    # print("预测明天的股价{}".format(y_test))
    t = x_test[:, -1]

    a1=t[0]
    b1=t[1]
    c1=t[2]
    d1=t[3]
    e1=t[4]
    f1=t[5]
    g1=t[6]
    h1=t[7]
    i1=t[8]
    j1=t[9]

    # print("今天的股价{}".format(x_test[:, -1]))
    return render(request,'predict.html',locals())



