# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
import finnhub
import requests
import os
from dotenv import load_dotenv

# finnhub_client = finnhub.Client(api_key="bscrtk7rh5rcu5phgmc0")


# -- Initialization section --
app = Flask(__name__)
load_dotenv()
finnhub_client = os.getenv("finnhub_key")

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",time=datetime.now())
    
@app.route('/survey')
def survey():
    return render_template("survey.html", time=datetime.now())

@app.route('/search')
def search():
    return render_template("search.html", time=datetime.now())

@app.route('/ticker',  methods=['GET','POST'])
def ticker():
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        data = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={finnhub_client}').json()
        currentPrice = data['c']
        print(currentPrice)

    return render_template("ticker.html",ticker=ticker,currentPrice=currentPrice,time=datetime.now())

@app.route('/result',  methods=['GET','POST'])
def result():
    if request.method == "POST":
        
        userdata =dict(request.form)
        print(userdata['investment'])
        print(request.form.getlist('investment'))
        investment= request.form.getlist('investment')
        field = request.form.getlist('field')
        budget = request.form.getlist('budget')
        company = ''
        prices = []
        affordable = []
        aPrices = []
        stats = []
        affordStats = []
        names = []
        affordNames = []

        if field[0] == 'Technology':
            company = 'MSFT'
        elif field[0] == 'Health care':
            company = 'CVS'
        elif field[0] == 'Real Estate':
            company = 'O'
        elif field[0] == "Telecommunication":
            company = 'CHTR'
        elif field[0] == 'Energy':
            company = 'NEE'
        
        print(company)
        print(field)

        # name = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol=UNH&token={finnhub_client}').json()
       

        companies = requests.get(f'https://finnhub.io/api/v1/stock/peers?symbol={company}&token={finnhub_client}').json()
        # goes through every company in the companies list
        for c in companies:
            # adds each company's price dictionary into a list called prices
            # adds each company's low,high, and annual return into stats list
            prices.append(requests.get(f'https://finnhub.io/api/v1/quote?symbol={c}&token={finnhub_client}').json())
            names.append(requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={c}&token={finnhub_client}').json())
            stats.append(requests.get(f'https://finnhub.io/api/v1/stock/metric?symbol={c}&metric=all&token={finnhub_client}').json())

        for i in range (0,len(prices)):
                print(prices[i]['c'])
                if float(budget[0]) > prices[i]['c']:
                    affordable.append(companies[i])
        print(affordable)
        for a in affordable:
            aPrices.append(requests.get(f'https://finnhub.io/api/v1/quote?symbol={a}&token={finnhub_client}').json())
            affordStats.append(requests.get(f'https://finnhub.io/api/v1/stock/metric?symbol={a}&metric=all&token={finnhub_client}').json())
            affordNames.append(requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={a}&token={finnhub_client}').json())
        # price = data['c']
        # industry = data1['finnhubIndustry']
        # print(data1)
        # print(data)
        print(companies)
        print(affordNames)
        print(aPrices)

        return render_template('results.html',affordNames=affordNames,names=names,affordStats=affordStats,stats=stats,aPrices=aPrices,prices=prices,investment=investment,field=field,budget=budget,companies=companies,affordable=affordable,time=datetime.now())
        
    else:
        return render_template('results.html',time=datetime.now())
        