# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from datetime import datetime
import finnhub
import requests
import os
from flask import session
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import bcrypt

# finnhub_client = finnhub.Client(api_key="bscrtk7rh5rcu5phgmc0")


# -- Initialization section --
app = Flask(__name__)
load_dotenv()
finnhub_client = os.getenv("finnhub_key")
app.secret_key = os.getenv("SECRET_KEY")
Mongo_User = os.getenv("Mongo_User")
Mongo_Password = os.getenv("Mongo_Password")
app.config['MONGO_DBNAME'] = 'login'


app.config['MONGO_URI'] = f'mongodb+srv://{Mongo_User}:{Mongo_Password}@cluster0.a3ibi.mongodb.net/login?retryWrites=true&w=majority'
mongo = PyMongo(app)

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",time=datetime.now())
@app.route('/home')
def home():
    return render_template("home.html", time=datetime.now())
@app.route('/signup', methods=["GET", "POST"])
def signup():
    users = mongo.db.users
    hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
   
    # existing_user = users.find_one({'name' : request.form['name']})

    if users.find_one({'name' : request.form['name']}):
        return "This name is taken, try another name!"
    else: 
        users.insert({"name": request.form["name"], "password": str(hashpass, 'utf-8')})
        session["user"] = request.form["name"]
        
        return "success"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['name']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['user'] = request.form['name']
                return "success"
        
        # if no successful match, display an error 
        return redirect('/index')

    
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
        companies = []
        

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


        companies = requests.get(f'https://finnhub.io/api/v1/stock/peers?symbol={company}&token={finnhub_client}').json()
        # goes through every company in the companies list
        for c in companies:
            # adds each company's price dictionary into a list called prices
            # adds each company's low,high, and annual return into stats list
            print(c)
            prices.append(requests.get(f'https://finnhub.io/api/v1/quote?symbol={c}&token={finnhub_client}').json())
            names.append(requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={c}&token={finnhub_client}').json())
            stats.append(requests.get(f'https://finnhub.io/api/v1/stock/metric?symbol={c}&metric=all&token={finnhub_client}').json())
            print(prices)
            print(names)
            print(stats)

        for i in range (0,len(prices)):
                print(prices[i]['c'])
                if float(budget[0]) > prices[i]['c']:
                    affordable.append(names[i])
                    aPrices.append(prices[i])
                    affordStats.append(stats[i])

        print(companies)
        print(affordable)
        print(aPrices)
        

        return render_template('results.html',names=names,affordStats=affordStats,stats=stats,aPrices=aPrices,prices=prices,investment=investment,field=field,budget=budget,companies=companies,affordable=affordable,time=datetime.now())
        
    else:
        return render_template('results.html',time=datetime.now())
        