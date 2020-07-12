from flask import Flask, request, url_for, render_template
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fox.db'
db = SQLAlchemy(app)

import time

import requests 


class City(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50) , nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/temperature" method="POST"><input name="city">'


@app.route('/temperature', methods=['POST'])
def temperature():
    l = []
    m = 0 
    data = []
    hen = ''
    zipc = request.form['city']
    zipc = zipc.upper()
    cities  = City.query.all()
    for city in cities :
        if(zipc == city.name):
            m = 100
    if(m!=100):
        new_city = City(name =zipc)
        db.session.add(new_city)
        db.session.commit()

    cities  = City.query.all()
    for city in cities :
        print(city.name)
        he = ((requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city.name+',us&appid=db1e707798c09c1ef9681eec261913b7')).json())
        check = he['cod']
        if(check != '404') :
            tempq = float(he["main"]['temp'])
            tempm = tempq - 273.15 
            tempf = ( tempm*(9/5) ) + 32 
            weather = {
                'city' : city.name ,
                'tempr' : tempm , 
                'tempf' : tempf , 
            }
            data.append(weather)
        else:
            print('no such city exists in the api')
    
    return render_template('hello.html' , data = data)

if __name__ == '__main__':
    app.run(debug=True)
