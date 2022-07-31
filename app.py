from flask import Flask, render_template, request
from flask_cors import CORS
import pymysql
import json
# ======================================================================
# 以下為投資組合
import pandas as pd
from pandas_datareader import data
# from pandas_datareader.yahoo.daily import YahooDailyReader
import requests
import csv
import time as ti
from datetime import datetime
# from datetime import date
import datetime  as dt
# ======================================================================
# 以下為選股組合
import bs4

# ======================================================================

app = Flask(__name__)
CORS(app) # 處理跨域同源政策問題
# 首頁
@app.route('/',methods=['GET'])
def index():
    active = 'active'
    tiele = 'EZ-GU'
    name_ha = '2330.tw'
    return render_template('index.html', active01 = active, tiele = tiele, name_ha = name_ha)


# /Elements
@app.route('/element',methods=['GET'])
def elements():
    return render_template('element.html')

@app.route('/button',methods=['GET'])
def button():
    return render_template('button.html')

@app.route('/typography',methods=['GET'])
def typography():
    return render_template('typography.html')


# /選股
@app.route('/widget',methods=['GET','POST'])
def widget():
    active = 'active'
    tiele = '選股推薦'
    return render_template('widget.html', active02 = active, tiele = tiele)

# /投資組合
@app.route('/form',methods=['GET','POST'])
def form():
    active = 'active'
    tiele = '投資組合分析'
    return render_template('form.html', active03 = active, tiele = tiele)

# /table
@app.route('/table',methods=['GET'])
def table():
    return render_template('table.html')

# /chart
@app.route('/chart',methods=['GET'])
def chart():
    return render_template('chart.html')

# /SP_01/to_name
@app.route('/SP_01/<name>',methods=['GET','POST'])
def to_name_01(name):
    tiele = name + '.tw 券商買賣排行'
    return render_template('ByS_Ranking.html',name = name ,tiele = tiele)

# /SP_02/to_name
@app.route('/SP_02/<name>',methods=['GET','POST'])
def to_name_02(name):
    tiele = name + '.tw 融資融券資訊'
    return render_template('Margin_Trading_and_Short_Selling.html',name = name ,tiele = tiele)



# /404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('parts/404.html' ,tiele = tiele), 404

# ===================================================(以下為路由)


# /K_line路由 接收前端的ajax請求
@app.route('/K_line',methods=['GET','POST'])

def my_echart():
    # 接收前端的傳值
    q = request.values.get('q')
    url_name = request.form.get('name')
    # print(url_name)


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info where Symbol="'+q+'.tw" AND Date BETWEEN "2022-04-29" AND "2022-07-13"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()
        

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)
            

            cur.close()
    # 用在選推薦分頁
    elif url_name :
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info where Symbol="'+url_name+'.tw" '
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()
        

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)
            

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-01-05" AND "2022-07-13"' 
        cur.execute(sql)
        u = cur.fetchall()
        # print(u)

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)
            

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /MACD路由 接收前端的ajax請求
@app.route('/MACD',methods=['GET','POST'])

def my_MACD():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, MACD, MACDsignal, MACDhist FROM stock_info where Symbol="'+q+'.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, MACD, MACDsignal, MACDhist FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()
        # print(u)

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /Change_MK(漲跌幅)路由 接收前端的ajax請求
@app.route('/Change_MK',methods=['GET','POST'])

def my_Change_MK():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, Change_MK FROM stock_info where Symbol="'+q+'.tw" AND Date BETWEEN "2020-05-13" AND "2022-07-12"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, Change_MK FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2020-05-13" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]), 2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /BBAND(布林通道)路由 接收前端的ajax請求
@app.route('/BBAND',methods=['GET','POST'])

def my_BBAND():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume, upper, middle, lower FROM stock_info where Symbol="'+q+'.tw" AND Date BETWEEN "2022-01-05" AND "2022-07-13"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[7]),2))
            result.append(round((data[8]),2))
            result.append(round((data[9]),2))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume, upper, middle, lower FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-01-05" AND "2022-07-13"' 
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[7]),2))
            result.append(round((data[8]),2))
            result.append(round((data[9]),2))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /KDJ路由 接收前端的ajax請求
@app.route('/KDJ',methods=['GET','POST'])

def my_KDJ():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, SLOWK, SLOWD, SLOWJ FROM stock_info where Symbol="'+q+'.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, SLOWK, SLOWD, SLOWJ FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()
        # print(u)

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /OBV路由 接收前端的ajax請求
@app.route('/OBV',methods=['GET','POST'])

def my_OBV():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, OBV FROM stock_info where Symbol="'+q+'.tw" AND Date BETWEEN "2020-05-13" AND "2022-07-12"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, OBV FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2020-05-13" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /RSI路由 
@app.route('/RSI',methods=['GET','POST'])

def my_RSI():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, RSI9, RSI14, RSI25 FROM stock_info where Symbol="'+q+'.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"'
        # print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='localhost',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, RSI9, RSI14, RSI25 FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()
        # print(u)

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /from_in路由
# /投資組合
@app.route('/form_in',methods=['GET','POST'])
def form_in():
    start_yt = '2002/01/01'
    end_yt = '2021/12/31'

    #接收輸入值
    name_st = request.values.get('name_st')
    input_Date = request.values.get('input_Date')
    input_Cost = request.values.get('input_Cost')
    input_Share = request.values.get('input_Share')
    SL_buy = []
    SD_buy = []
    SC_buy = []
    SS_buy = []
    standard_deviation_list = []
    IRR_list = []
    sharpe_list = []
    Beta_list = []

    if name_st:
        #2021年美國聯邦銀行利率
        url = "https://api.finmindtrade.com/api/v4/data"
        parameter = {
        "dataset": "InterestRate",
        "data_id": "FED",
        "start_date": "2021-03-17",
        }
        Interest_rate_data = requests.get(url, params=parameter)
        Interest_rate_data = Interest_rate_data.json()
        Interest_rate_data = pd.DataFrame(Interest_rate_data['data'])

        # 新增空DataFrame
        stock_NB_buy = pd.DataFrame()
        stock_YAHOO_ORDER_buy = pd.DataFrame()
        stock_ALL_INFO_buy = pd.DataFrame()
        IP_buy = pd.DataFrame()

        # 18-21年台灣加權指數平均報酬率
        name_mk = '^twii'
        df_mk = data.DataReader(name_mk,'yahoo', start_yt, end_yt)
        df_mk['Change%MK'] = (df_mk['Close']/df_mk['Close'].shift(1)-1)*100
        change_mk_avg = df_mk['Change%MK'].mean() * 100

        # 18-21年美國10年國債平均利率
        name_usyt = '^TNX'
        df_us10yt = data.DataReader(name_usyt,'yahoo', start_yt, end_yt)
        df_us10yt['Change%USYT'] = (df_us10yt['Close'] / df_us10yt['Close'].shift(1)-1)*100
        us10yt_avg = df_us10yt['Change%USYT'].mean() * 100

        print('18-21年美國10年國債平均利率=',us10yt_avg)
        print('18-21年{}平均報酬率='.format(name_mk),change_mk_avg)

        if name_st:
            SL_buy.append(name_st)

        if input_Date:
            SD_buy.append(input_Date)

        if input_Cost:
            SC_buy.append(input_Cost)

        if input_Share:
            SS_buy.append(input_Share)

            
        # 確認當前日期是否為週末
        # 確認當前時間是否早於09:30(若早於上午0930，則自動抓取前一天之資訊) 
        today = dt.date.today()
        yahoo_limit_time = dt.time(9, 30)
        localtime = dt.datetime.now().time()
        def check_weekend(today):
            if today.weekday() == 5:
                return str(today + dt.timedelta(days=-1))
            if today.weekday() == 6:
                return str(today + dt.timedelta(days=-2))
            if localtime < yahoo_limit_time:
                return str(today + dt.timedelta(days=-1))
            if localtime > yahoo_limit_time:
                return datetime.strftime(today, "%Y-%m-%d")
            else:
                return datetime.strftime(today, "%Y-%m-%d")
        # 調整輸入日期，輸入予證交所爬取資料
        # 市場未結束時(09:00 - 13:30)，證交所資料尚未統整，故抓取前一天資料
        input_Date = datetime.strptime(input_Date, "%Y-%m-%d").date()
        today = dt.date.today()
        time = dt.time(14, 40) # 設定1430等待證交所完整資料上傳
        localtime = dt.datetime.now().time()
        def check_datetime(input_Date):
            if input_Date == today:
                if input_Date.weekday() == 0:
                    if localtime < time:
                        return str(input_Date + dt.timedelta(days=-3))
                    if localtime > time:
                        return datetime.strftime(input_Date, "%Y-%m-%d")
            if input_Date.weekday() == 5:
                return str(input_Date + dt.timedelta(days=-1))
            if input_Date.weekday() == 6:
                return str(input_Date + dt.timedelta(days=-2))
            if input_Date == today:
                if localtime < time:
                    return str(input_Date + dt.timedelta(days=-1))
                if localtime > time:
                    return datetime.strftime(input_Date, "%Y-%m-%d")
            else:
                return datetime.strftime(input_Date, "%Y-%m-%d")
        
        date_range = [i.strftime("%Y%m%d") for i in pd.date_range(
            check_datetime(input_Date),
            check_datetime(input_Date)
        )]

        for d in date_range:
            url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX'
            formdata = {
                'response': 'csv',
                'date': d, 
                'type': 'ALLBUT0999',
            }
            # 取得資料並且解析
            r = requests.get(url, params=formdata)
            r.text.encode('utf8')
            cr = csv.reader(r.text.splitlines(), delimiter=',')
            my_list = list(cr)

            # print(my_list)

            # 資料整理
            if len(my_list) > 0:
                for i in range(len(my_list)):
                    if len(my_list[i]) > 0:
                        if my_list[i][0] == '證券代號':
                            new_list = my_list[i:]
                            break
                for j in range(len(new_list)):
                    if j != 0:
                        try:
                            new_list[j][0] = new_list[j][0].split('"')[1]
                        except:
                            break
                df = pd.DataFrame(new_list[1:], columns=new_list[0])

                print('已篩選出 {} 全上市股票行情資料'.format(date_range))
                ti.sleep(1)
            else:
                print('No Data')
                No_Data = pd.DataFrame({
                'Date' : SD_buy[0]+" 當日無開盤",
                'id' : SL_buy
                },index = range(len(SL_buy)))
                data_in = No_Data.to_json(orient = 'records',force_ascii=False)
                
                return(data_in)
            

        # 18-21年指定個股平均報酬率
        name_rr = str('{}.tw'.format(name_st))
        df_rr = data.DataReader(name_rr, 'yahoo', start_yt, end_yt)
        df_rr['Change%RR'] = (df_rr['Close'] / df_rr['Close'].shift(1)-1)*100
        change_rr_avg = df_rr['Change%RR'].mean() * 100

        # 篩選資料並加入新DataFrame
        stock_NB_buy = pd.concat([stock_NB_buy, df.loc[df['證券代號'] == name_st]], axis = 0)

        # 篩出指定欄位
        stock_LS_buy = stock_NB_buy[['證券代號','證券名稱','開盤價','最高價','最低價','收盤價','漲跌(+/-)','漲跌價差','本益比']]
        # 增加欄位至指定位置
        stock_LS_buy.insert(0,'交易日期',SD_buy)
        stock_LS_buy = stock_LS_buy.reset_index()

        # yahoo DataReader:當下股票資訊
        start = check_weekend(today)
        end = check_weekend(today)
        # start = "2022-07-24"
        # end = "2022-07-24"
        name = str('{}.tw'.format(name_st))
        df_st_buy = data.DataReader(name, 'yahoo', start, end)
        # print(df_st_buy)
        
        # 將證交所、Yahoo Finance資料合併
        stock_YAHOO_ORDER_buy = pd.concat([stock_YAHOO_ORDER_buy, df_st_buy],axis = 0,ignore_index = True)
        
        # 彙整所有DataFrame
        stock_ALL_INFO_buy = pd.concat([stock_LS_buy, stock_YAHOO_ORDER_buy], axis = 1)
        stock_ALL_INFO_buy['收盤價'] = stock_ALL_INFO_buy['收盤價'].astype(float, errors = 'raise')

        # 18-21年個股曝險程度及報酬率
        name = str('{}.tw'.format(name_st))
        df_days_st = data.DataReader(name, 'yahoo', start_yt, end_yt)

        # 個股標準差(standard_deviation)
        standard_deviation = df_days_st['Close'].std()
        if standard_deviation != 0:
            standard_deviation_list.append(standard_deviation)

        # 年化報酬率(IRR)
        TR = df_days_st['Close'].iloc[-1] / df_days_st['Close'].iloc[0] - 1
        days = len(df_days_st)
        IRR = ((1+TR)**(270/days)-1)*100
        if IRR != 0:
            IRR_list.append(IRR)

        # 個股夏普值
        sharpe = (IRR - us10yt_avg) / standard_deviation
        if sharpe != 0:
            sharpe_list.append(sharpe)
            
        # 貝他值 Beta
        # 股票收益率 減去 無風險利率
        SV = change_rr_avg - us10yt_avg
        # 加權指數收益率 減去 無風險利率
        MV = change_mk_avg - us10yt_avg
        # 貝他值 = (股票收益率 減去 無風險利率之差) / (加權指數收益率 減去 無風險利率之差)
        beta = SV / MV
        if beta != 0:
            Beta_list.append(beta)
        
        risk = pd.DataFrame({
            'ID' : SL_buy,
            'SD' : standard_deviation_list,
            'IRR' : IRR_list,
            'Sharpe' : sharpe_list,
            'Beta' : Beta_list
        },index = SL_buy)
        risk.insert(5, 'RR', 0)
        risk.insert(6, 'MR', 0)
        risk.insert(7, 'Rate', 0)
        
        # 蒐集input元素並製成DataFrame
        all_INPUT_buy = pd.DataFrame({
            'Number' : SL_buy,
            'Date' : SD_buy,
            'Cost' : SC_buy,
            'Share' : SS_buy
        },index = range(len(SL_buy)))
        all_INPUT_buy['Number'] = all_INPUT_buy['Number'].astype(float, errors = 'raise')
        all_INPUT_buy['Cost'] = all_INPUT_buy['Cost'].astype(float, errors = 'raise')
        all_INPUT_buy['Share'] = all_INPUT_buy['Share'].astype(float, errors = 'raise')

        # 建立投資組合表格
        IP_buy = pd.DataFrame(columns=['id','id_name','YEAR','SP','BT','現價','成本基準','買入股數','買進手續費','買價','現值','持股漲跌幅'],index = SD_buy)
        if len(stock_ALL_INFO_buy) > 0:
            for NM in range(len(stock_ALL_INFO_buy)):
                IP_buy.at[IP_buy.index[NM], 'id'] = stock_ALL_INFO_buy.at[stock_ALL_INFO_buy.index[NM], '證券代號']
                IP_buy.at[IP_buy.index[NM], 'id_name'] = stock_ALL_INFO_buy.at[stock_ALL_INFO_buy.index[NM], '證券名稱']
        if len(risk) > 0:
            for NR in range(len(risk)):
                IP_buy.at[IP_buy.index[NR], 'YEAR'] = risk.at[risk.index[NR], 'IRR']
                IP_buy.at[IP_buy.index[NR], 'SP'] = risk.at[risk.index[NR], 'Sharpe']
                IP_buy.at[IP_buy.index[NR], 'BT'] = risk.at[risk.index[NR], 'Beta']
        if len(stock_YAHOO_ORDER_buy) > 0:
            for NY in range(len(stock_YAHOO_ORDER_buy)):
                IP_buy.at[IP_buy.index[NY], '現價'] = stock_YAHOO_ORDER_buy.at[stock_YAHOO_ORDER_buy.index[NY], 'Close']
        if len(all_INPUT_buy) > 0:
            for NB in range(len(all_INPUT_buy)):
                IP_buy.at[IP_buy.index[NB], '成本基準'] = all_INPUT_buy.at[all_INPUT_buy.index[NB], 'Cost']
                IP_buy.at[IP_buy.index[NB], '買入股數'] = all_INPUT_buy.at[all_INPUT_buy.index[NB], 'Share']
                IP_buy.at[IP_buy.index[NB], '買進手續費'] = float(IP_buy.at[IP_buy.index[NB], '成本基準']) * float(IP_buy.at[IP_buy.index[NB], '買入股數']) * 0.001425
                IP_buy.at[IP_buy.index[NB], '買價'] = float(IP_buy.at[IP_buy.index[NB], '成本基準']) * float(IP_buy.at[IP_buy.index[NB], '買入股數']) + float(IP_buy.at[IP_buy.index[NB], '買進手續費'])
                IP_buy.at[IP_buy.index[NB], '現值'] = float(stock_ALL_INFO_buy.at[stock_ALL_INFO_buy.index[NB], '收盤價']) * float(IP_buy.at[IP_buy.index[NB], '買入股數'])
                IP_buy.at[IP_buy.index[NB], '持股漲跌幅'] = (IP_buy.at[IP_buy.index[NB], '現值']-IP_buy.at[IP_buy.index[NB], '買價'])/IP_buy.at[IP_buy.index[NB], '買價'] * 100
                
                # 將指定欄位整行轉型
                IP_buy['買價'] = IP_buy['買價'].astype(float, errors = 'raise')

        
    # IP_buy.insert(12, 'MV', change_mk_avg-us10yt_avg)
    IP_buy.insert(12, 'change_mk_avg', change_mk_avg)
    IP_buy.insert(13, 'us10yt_avg', us10yt_avg)
    IP_buy.insert(0,'Date',SD_buy)
    # MV加權指數收益率 減去 無風險利率
    IP_buy['MV'] = IP_buy['change_mk_avg'] - IP_buy['us10yt_avg']
    # IP_buy = stock_LS_buy.reset_index()
    # IP_buy = IP_buy.reset_index(inplace=True)

    data_in = IP_buy.to_json(orient = 'records',force_ascii=False)
    print(data_in)

    return(data_in)

# /SPK_1路由
# /選股-投信
@app.route('/SPK_1',methods=['GET','POST'])
def SPK_1():

    #使用requests
    url = "https://goodinfo.tw/tw/StockList.asp?RPT_TIME=&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E6%8A%95%E4%BF%A1%E7%B4%AF%E8%A8%88%E8%B2%B7%E8%B6%85%E5%BC%B5%E6%95%B8+%E2%80%93+%E7%95%B6%E6%97%A5%40%40%E6%8A%95%E4%BF%A1%E7%B4%AF%E8%A8%88%E8%B2%B7%E8%B6%85%40%40%E6%8A%95%E4%BF%A1%E8%B2%B7%E8%B6%85%E5%BC%B5%E6%95%B8+%E2%80%93+%E7%95%B6%E6%97%A5"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    res = requests.get(url,headers=headers)
    res.encoding = "utf-8"
    ti.sleep(2)

    #使用bs4的BeautifulSoup
    soup = bs4.BeautifulSoup(res.text,"lxml")
    data = soup.select_one("#txtStockListData")

    #使用pandas
    df = pd.read_html(data.prettify())
    dfs = df[1]
    dfs.drop(['外資  買進  張數','外資  賣出  張數','外資  買賣超  張數','自營  買進  張數','自營  賣出  張數','自營  買賣超  張數','合計  買進  張數','合計  賣出  張數','合計  買賣超  張數'], axis=1 ,inplace = True)
    dfs.drop([18],axis=0,inplace=True)

    stock20 = dfs.head(20)

    # ascii：預設值True，如果資料中含有非ASCII的字元，則會類似\uXXXX的顯示資料，設定成False後，就能正常顯示
    # records為切割DataFrame資料方法之一(allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.)。
    stock20_in = stock20.to_json(orient = 'records',force_ascii=False)
    print(stock20_in)

    return(stock20_in)

# /選股-投信-券商買賣排行
@app.route('/ByS_Ranking',methods=['GET','POST'])
def ByS_Ranking():

    url_name = request.form.get('name')
    print(url_name)

    lst = {url_name}
    url_test = 'https://histock.tw/stock/branch.aspx?no=%s'
    for i in lst:
        url = url_test %i
            
    tables = pd.read_html(url)

    df1 = tables[0]
    # df1.rename(columns ={'券商名稱.1': '券商名稱', '買張.1': '買張', '賣張.1': '賣張', '均價.1': '均價'},inplace = True)
    df1.fillna({'買張':0,'買張.1':0,'賣張':0,'賣張.1':0}, inplace=True )
    df1 = df1.astype({"買張":"int","賣張":"int",'買張.1':"int","賣張.1":"int"})
    blankIndex=[''] * len(df1)
    df1.index=blankIndex

    # stock20 = dfs.head(20)

    # ascii：預設值True，如果資料中含有非ASCII的字元，則會類似\uXXXX的顯示資料，設定成False後，就能正常顯示
    # records為切割DataFrame資料方法之一(allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.)。
    ByS_Ranking = df1.to_json(orient = 'records',force_ascii=False)
    print(ByS_Ranking)

    return(ByS_Ranking)

# /SPK_2路由
# /選股-週轉率Turnover
@app.route('/SPK_2',methods=['GET','POST'])
def SPK_2():

    #使用requests
    url = 'https://goodinfo.tw/tw/StockList.asp?RPT_TIME=&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E7%B4%AF%E8%A8%88%E6%88%90%E4%BA%A4%E9%87%8F%E9%80%B1%E8%BD%89%E7%8E%87%28%E7%95%B6%E6%97%A5%29%40%40%E7%B4%AF%E8%A8%88%E6%88%90%E4%BA%A4%E9%87%8F%E9%80%B1%E8%BD%89%E7%8E%87%40%40%E7%95%B6%E6%97%A5'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    res = requests.get(url,headers=headers)
    res.encoding = "utf-8"

    #使用bs4的BeautifulSoup
    soup = bs4.BeautifulSoup(res.text,"lxml")
    data = soup.select_one("#txtStockListData")

    #使用pandas
    df = pd.read_html(data.prettify())
    dfs = df[1]
    dfs.drop(['10日  累計  成交量  週轉率','一個月  累計  成交量  週轉率','三個月  累計  成交量  週轉率','半年  累計  成交量  週轉率','今年  累計  成交量  週轉率','一年  累計  成交量  週轉率', '二年  累計  成交量  週轉率', '三年  累計  成交量  週轉率'],axis=1,inplace=True)
    dfs.drop([18],axis=0,inplace=True)

    Turnover20 = dfs.head(20)

    # ascii：預設值True，如果資料中含有非ASCII的字元，則會類似\uXXXX的顯示資料，設定成False後，就能正常顯示
    # records為切割DataFrame資料方法之一(allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.)。
    Turnover20_in = Turnover20.to_json(orient = 'records',force_ascii=False)
    print(Turnover20_in)

    return(Turnover20_in)

# /選股-投信-融資融券Margin_Trading_and_Short_Selling
@app.route('/MTaSS',methods=['GET','POST'])
def MTaSS():

    url_name = request.form.get('name')
    print(url_name)

    lst = {url_name}
    url_test = 'https://histock.tw/stock/chips.aspx?no=%s&m=mg'
    for i in lst:
        url = url_test %i
    tables = pd.read_html(url)    

    df1 = tables[0]
    df1.columns = df1.columns.to_flat_index()
    df1 = df1.rename(columns={(     '日期',     '日期'):     '日期',('資券互抵(張)','資券互抵(張)'):'資券互抵(張)',('資券當沖(%)','資券當沖(%)'):'資券當沖(%)',('券資比(%)','券資比(%)'):'券資比(%)'\
                            ,(     '價格',     '價格'):     '價格',(     '比例',     '比例'):     '比例',(    '成交量',    '成交量'):    '成交量'},errors='raise')
    df1.rename(columns ={   ('融資', '增加'): '融資增加',   ('融資', '餘額'):'融資餘額', ('融資', '使用率％'):'融資使用率%',('融券', '增加'):'融券增加',   ('融券', '餘額'): '融券餘額',(     '融券',    '使用率％'): '融券使用率%'},inplace = True)
    blankIndex=[''] * len(df1)
    df1.index=blankIndex

    # ascii：預設值True，如果資料中含有非ASCII的字元，則會類似\uXXXX的顯示資料，設定成False後，就能正常顯示
    # records為切割DataFrame資料方法之一(allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.)。
    MTaSS = df1.to_json(orient = 'records',force_ascii=False)
    print(MTaSS)
    return(MTaSS)




