import streamlit as st
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime,timedelta,date
from jugaad_data.nse import NSELive
n = NSELive()
import pandas_ta as ta
import requests
from py5paisa import FivePaisaClient
import websocket

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")

headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        "x-requested-with": "XMLHttpRequest"
    }

cred={
    "APP_NAME":"5P54504289",
    "APP_SOURCE":"7050",
    "USER_ID":"byNY6tfyKQY",
    "PASSWORD":"3QxsV4SHMWV",
    "USER_KEY":"TbcrPHDEDeOCkgi4Aim3huicnCvSOcAx",
    "ENCRYPTION_KEY":"xwuGHmI3oRROIzKY5rmGwkwzS6b22ffH"
    }

client = FivePaisaClient(email="rishabh.maniyar@gmail.com", passwd="5paisa@123", dob="19990831",cred=cred)
client.login()

st.write("Hey Rishabh")
st.sidebar.title("Dashboard")

left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

option=st.sidebar.selectbox("Looking for ?",('Option Chain (Index)','Option Chain (Stock)','Stock Info','Backtest','Results','Trades','Market Movers','E'))
if option=='E':
    def delete_selenium_log():
        if os.path.exists('selenium.log'):
                os.remove('selenium.log')


        def show_selenium_log():
            if os.path.exists('selenium.log'):
                with open('selenium.log') as f:
                    content = f.read()
                    st.code(content)


        def get_chromedriver_path():
            results = glob.glob('/**/chromedriver', recursive=True)  # workaround on streamlit sharing
            which = results[0]
            return which


        def run_selenium():
            name = str()
            with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
                url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
                driver.get(url)
                xpath = '//*[@class="ui-mainview-block eventpath-wrapper"]'
                # Wait for the element to be rendered:
                element = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_xpath(xpath))
                # element = driver.find_elements_by_xpath(xpath)
                name = element[0].get_property('attributes')[0]['name']
                # print(name)
            return name


        if __name__ == "__main__":
            delete_selenium_log()
            st.set_page_config(page_title="Selenium Test", page_icon='✅',
                initial_sidebar_state='collapsed')
            st.title('🔨 Selenium Test for Streamlit Sharing')
            st.markdown("""
                This app is only a very simple test for **Selenium** running on **Streamlit Sharing** runtime. <br>
                The suggestion for this demo app came from a post on the Streamlit Community Forum.  <br>
                <https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563>  <br>
                Unfortunately this app has deployment issues on Streamlit Sharing, sometimes deployment fails, sometimes not... 😞
                This is just a very very simple example and more a proof of concept.
                A link is called and waited for the existence of a specific class and read it. If there is no error message, the action was successful.
                Afterwards the log file of chromium is read and displayed.
                ---
                """, unsafe_allow_html=True)
            # executable_path = get_chromedriver_path()
            executable_path = "notset"
            # st.info(f'Chromedriver Path: {str(executable_path)}')
            st.balloons()
            if st.button('Start Selenium run'):
                st.info('Selenium is running, please wait...')
                result = run_selenium()
                st.info(f'Result -> {result}')
                st.info('Successful finished. Selenium log file is shown below...')
                show_selenium_log()
        
        
if option=='Option Chain (Index)':
    index=st.sidebar.selectbox("Select Index ",('NIFTY','BANKNIFTY'))
    if index=='NIFTY':
        option_chain = n.index_option_chain("NIFTY")
        oc=[]
        for option in option_chain['filtered']['data']:
            (oc.append([option['CE']['openInterest'],option['CE']['changeinOpenInterest'],option['CE']['lastPrice'], option['strikePrice'], option['PE']['lastPrice'],option['PE']['changeinOpenInterest'],option['PE']['openInterest']]))
        df1=pd.DataFrame(oc)
        df1.columns=['CE OI','CE COI','CE LTP','SP','PE LTP','PE COI','PE OI']
        df1=df1.set_index('SP')
        #st.write(df1)
        st.bar_chart(df1)
    if index=='BANKNIFTY':
        option_chain = n.index_option_chain("BANKNIFTY")
        oc=[]
        for option in option_chain['filtered']['data']:
            (oc.append([option['CE']['openInterest'],option['CE']['changeinOpenInterest'],option['CE']['lastPrice'], option['strikePrice'], option['PE']['lastPrice'],option['PE']['changeinOpenInterest'],option['PE']['openInterest']]))
        df2=pd.DataFrame(oc)
        df2.columns=['CE OI','CE COI','CE LTP','SP','PE LTP','PE COI','PE OI']
        df2=df2.set_index('SP')
        #st.write(df2)
        st.bar_chart(df2)
def nsefetch(payload):
    try:
        output = requests.get(payload,headers=headers).json()
    except ValueError:
        s =requests.Session()
        output = s.get("http://nseindia.com",headers=headers)
        output = s.get(payload,headers=headers).json()
    return output


if option=='Option Chain (Stock)':
    stock=st.sidebar.text_input(label='Search for Stock',value='NIFTY')
    exp_url='https://opstra.definedge.com/api/weeklies'
    exp=st.sidebar.radio('Select Expiry?',tuple(nsefetch(exp_url)))
    # url=f'https://www.nseindia.com/api/option-chain-equities?symbol={stock}'
    trendlyne_search_url=f'https://trendlyne.com/futures-options/search/30-dec-2021-near/optionchain/?term={stock}'
    # trendlyne_oc_url=f'https://trendlyne.com/futures-options/api/options/30-dec-2021-near/{sid}'
    opstra_oc=f'https://opstra.definedge.com/api/openinterest/optionchain/free/{stock}&{exp}'
    
    search=nsefetch(opstra_oc)
    df=pd.DataFrame(search['data'])
    df=df.set_index('StrikePrice')
    st.bar_chart(df)
#     url=f'https://www.nseindia.com/api/option-chain-equities?symbol={stock}'
    
end=date.today()

if option=='Results':
    res_url='https://opstra.definedge.com/api/resultscalendar?responseType=JSON'
    results=nsefetch(res_url)
    rls=[]
    for r in results:
        d=r['date']
        dt=datetime.strptime(d, '%Y-%m-%d')
        if dt>datetime.today():
            rls.append(r)
    
    df=pd.DataFrame(rls)
    st.write("Upcoming Results")
    st.write(df)
        
        
if option=='Stock Info':
    stock=st.sidebar.text_input(label='Search for Stock',value='LT')
    sid=st.sidebar.text_input(label='Enter for Stock SID',value='837957')
    # url=f'https://www.nseindia.com/api/option-chain-equities?symbol={stock}'
    mm_search_url=f'https://www.marketsmojo.com/portfolio-plus/frontendsearch?SearchPhrase={stock}'
    mm_about_url=f'https://frapi.marketsmojo.com/Stocks_Companycv/about_comp_full_det?sid={sid}&exchange=0&mob=1'
    mm_recomm_url=f'https://frapi.marketsmojo.com/Stocks_Recos/get_recos?sid={sid}&exchange=0'
    mm_stk_news_url='https://frapi.marketsmojo.com/stocks_news/listNews'
    search=nsefetch(mm_search_url)
    ss=pd.DataFrame(search)
    ss=ss.drop(['ScriptCode','url','price','Company','ExchangeName'],axis=1)
    st.sidebar.write(ss)
    st.write('About the Company')
    ab=nsefetch(mm_about_url)['data']['KNOW_YOUR_COMPANY']
    st.write(ab['full_details'])
    st.write('Recommendations for the Stock')
    rec=nsefetch(mm_recomm_url)['data']
    d2=pd.DataFrame(rec)
    if not d2.empty:
        d2=d2.drop(['graph_data','pdf_link','low_reco_dir','reco_potential_dir','peak_reco_dir','bse200_dir','reco_performance_dir'],axis=1)
    st.write(d2)
    
if option=='Backtest':
    days=st.sidebar.selectbox("Strategy?",('HH-LL','RSI','MA Crossover'))
    stock=st.text_input(label='stock name',value='LT')
    #st.write(stock)
    start = st.date_input ( label='start date' , value=end-timedelta(250) , min_value=None , max_value=None , key=None )
    end = st.date_input ( label='end date' , value=None , min_value=None , max_value=None , key=None )
    b=st.sidebar.number_input(label='Buffer %',min_value=1)
    df=client.historical_data('N','C',client.fetch_market_feed([{"Exch":"N","ExchType":"C","Symbol":stock}])['Data'][0]['Token'],'1d',start,end)
    # df=df.reset_index()
    print(type(df))
    df.rename(columns={'Datetime':'Date'},inplace=True)
    df=df.set_index('Date')   
    #st.write(df)
    st.line_chart(df['Close'])
    def crossup(fe_f,se_f,fe_s,se_s):
        if fe_f<fe_s and se_f>se_s:
            return (True)
    def crossdown(fe_f,se_f,fe_s,se_s):
        if fe_f>fe_s and se_f<se_s:
            return (True)
    def report(stock,trades,total_profit,max_profit,max_loss,returns):
        st.title("Report")
        st.write(f'Stock Name ->  {stock}')
        st.write(f'Total No. of Trades ->  {trades}')
        st.write(f'Total Profit Points Long ->  {total_profit}')
        st.write(f'Max. Profit ->  {max_profit}')
        st.write(f'Max. Loss ->  {max_loss}')
        st.write(f'Returns from {start} ->  {returns}%')
    if days=='HH-LL':
        df=df.reset_index()
        position=0
        buy=[]
        sell=[]
        pnl=[]
        for i in range(1,len(df)-1,1):
            th=df['High'][i]
            tph=df['High'][i-1]
            t_close=round(df['Close'][i+1])
            tnh=df['High'][i+1]
            tl=df['Low'][i]
            tpl=df['Low'][i-1]
            tnl=df['Low'][i+1]
            hh=max(th,tph)
            ll=min(tl,tpl)
            date=df['Date'][i]
            #LONG
            if position==0:
                buffer=(b/100)*t_close
                if tnh>hh+buffer:
                    position=1
                    buy.append([date,hh+buffer])
            if position==1:
                if tnl<ll-buffer:
                    position=0
                    sell.append([date,ll-buffer])

        if len(buy)>len(sell):
            position=0
            sell.append([date,t_close])
        buy_df=pd.DataFrame(buy) 
        sell_df=pd.DataFrame(sell)
        buy_df.columns=['Date','Price'] 
        sell_df.columns=['Date','Price'] 
        st.title("Buy Trades")
        st.write(buy_df)
        st.title("Sell Trades")
        st.write(sell_df)
        pnl=[]
        for i in range(0,len(buy)-1,1):
            pnl.append(sell[i][1]-buy[i][1])
        pnl_df=pd.DataFrame(pnl)
        pnl_df.columns=['PNL']
        st.title("PNL")
        st.write(pnl_df)
        r=(sum(pnl)*100)/round(df['Close'][0])
        report(stock,len(pnl)+1,round(sum(pnl)),round(max(pnl)),-round(min(pnl)),round(r,2))
        
        #print("Stock Name:- ",stock,"\nNo. of Trades -> ",len(pnl)+1,"\nProfit Points Long -> ",round(sum(pnl)),"\nMax. Profit -> ",round(max(pnl)),"\nMax. Loss -> ",round(min(pnl)),"\nReturn 1Yr Only Long from ",start,"-> ",(sum(pnl)*100)/round(df['Adj Close'][0]))
    
    if days=='RSI':
        df=df.reset_index()
        position=0
        buy=[]
        sell=[]
        pnl=[]
        b=st.sidebar.number_input(label='RSI Period',min_value=14)
        rsi = ta.rsi(df["Close"], length=b)
        df['RSI']=rsi
        go_long=st.sidebar.number_input(label='RSI Buy Level',min_value=0)
        exit=st.sidebar.number_input(label='RSI Exit Level',min_value=0)        
        for i in range(1,len(df)-1,1):
            rsi=df['RSI'][i]
            t_close=df['Close'][i]
            t_high=df['High'][i]
            tnhigh=df['High'][i+1]
            t_low=df['Low'][i]
            tnlow=df['Low'][i+1]
            date=df['Date'][i]
            #LONG
            if position==0:
                buffer=0.01*t_high
                if rsi>go_long:
                    position=1
                    buy.append([date,t_high+buffer])
            if position==1:
                if rsi<exit:
                    position=0
                    sell.append([date,t_low-buffer])
        if len(buy)>len(sell):
            position=0
            sell.append([date,t_close]) 
        buy_df=pd.DataFrame(buy) 
        sell_df=pd.DataFrame(sell)
        buy_df.columns=['Date','Price'] 
        sell_df.columns=['Date','Price'] 
        st.title("Buy Trades")
        st.write(buy_df)
        st.title("Sell Trades")
        st.write(sell_df)
        pnl=[]
        for i in range(0,len(buy),1):
            pnl.append(sell[i][1]-buy[i][1])
        pnl_df=pd.DataFrame(pnl)
        pnl_df.columns=['PNL']
        st.write(pnl_df)
        r=(sum(pnl)*100)/round(df['Close'][0])
        report(stock,len(pnl)+1,round(sum(pnl)),round(max(pnl)),-round(min(pnl)),round(r,2))
   
    if days=='MA Crossover':
        df=df.reset_index()
        position=0
        buy=[]
        sell=[]
        pnl=[]  
        fm=st.sidebar.number_input(label='Fast MA Period',min_value=2)  
        df['fma']=df.ta.ema(length=fm, append=True)
        sm=st.sidebar.number_input(label='Slow MA Period',min_value=5)        
        df['sma']=df.ta.ema(length=sm, append=True)
        df=df.dropna()
        for i in range(0,len(df)-1,1):
            fe_f=df.iloc[i]['fma']
            se_f=df.iloc[i+1]['fma']  
            fe_s=df.iloc[i]['sma']
            se_s=df.iloc[i+1]['sma']
            h=df.iloc[i+1]['High']
            l=df.iloc[i+1]['Low']
            t_close=df.iloc[i]['Close']
            date=df.iloc[i]['Date']
            if (crossup(fe_f,se_f,fe_s,se_s)) and position==0:
                position=1
                buy.append([date,h])
            if (crossdown(fe_f,se_f,fe_s,se_s)) and position==1:
                position=0
                sell.append([date,l])
        if len(buy)>len(sell):
            position=0
            sell.append([date,t_close]) 
        buy_df=pd.DataFrame(buy) 
        sell_df=pd.DataFrame(sell)
        buy_df.columns=['Date','Price'] 
        sell_df.columns=['Date','Price'] 
        st.title("Buy Trades")
        st.write(buy_df)
        st.title("Sell Trades")
        st.write(sell_df)
        pnl=[]
        for i in range(0,len(buy),1):
            pnl.append(sell[i][1]-buy[i][1])
        pnl_df=pd.DataFrame(pnl)
        pnl_df.columns=['PNL']
        st.write(pnl_df)
        r=(sum(pnl)*100)/round(df.iloc[0]['Close'])
        report(stock,len(pnl)+1,round(sum(pnl)),round(max(pnl)),-round(min(pnl)),round(r,2))
        

if option=='Market Movers':
    mkt_movers_link = "https://msi-gcloud-prod.appspot.com/gateway/simple-api/ms-india/instr/getMarketMovers.json?ms-auth=3990+MarketSmithINDUID-Web0000000000+MarketSmithINDUID-Web0000000000+0+210127215830+-457924016"
    movers = requests.get(mkt_movers_link,headers=headers).json()
    up_move_no=len(movers['upOnPriceList'])
    down_move_no=len(movers['downOnPriceList'])
    up_name=[]
    up_perchange=[]
    up_symbol=[]
    down_name=[]
    down_perchange=[]
    down_symbol=[]
    for i in range(0,up_move_no-1,1):
        up_name.append(movers['upOnPriceList'][i]['coName'])
        up_perchange.append(movers['upOnPriceList'][i]['pricePercChg'])
        up_symbol.append(movers['upOnPriceList'][i]['symbol'])
    
    for i in range(0,down_move_no-1,1):
        down_name.append(movers['downOnPriceList'][i]['coName'])
        down_perchange.append(movers['downOnPriceList'][i]['pricePercChg'])
        down_symbol.append(movers['downOnPriceList'][i]['symbol'])
    up_df=pd.DataFrame(list(zip(up_name,up_perchange , up_symbol)),columns=('Company Name','% Change','Symbol')).sort_values(by='% Change')
    down_df=pd.DataFrame(list(zip(down_name,down_perchange , down_symbol)),columns=('Company Name','% Change','Symbol')).sort_values(by='% Change')
    up_df=up_df.reset_index(drop=True)
    down_df=down_df.reset_index(drop=True)
    st.write(up_df)
    st.write(down_df)
