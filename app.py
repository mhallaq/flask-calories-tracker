from flask import Flask, render_template ,request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from datetime import datetime
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://qatraining:Qatraining@1975@localhost/flask_project1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db=SQLAlchemy(app)

class Log_date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)

class Food(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40),nullable=False)
    protein=db.Column(db.Integer, nullable=False)
    carb=db.Column(db.Integer, nullable=False)
    fat=db.Column(db.Integer, nullable=False)
    calories=db.Column(db.Integer, nullable=False)
    
class Food_date(db.Model):
    food_id=db.Column(db.Integer, primary_key=True)
    log_date_id=db.Column(db.Integer, primary_key=True)



@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        date=request.form['date']
        parsed_date=datetime.strptime(date,'%Y-%m-%d')
        database_date=datetime.strftime(parsed_date,'%Y%m%d')
        new_log_date=Log_date(entry_date=database_date)
        db.session.add(new_log_date)
        db.session.commit()
        # return database_date

    # db.drop_all()
    # db.create_all()
    # testLog_date = Log_date(entry_date='2021/02/05') # Extra: this section populates the table with an example entry
    # db.session.add(testLog_date)
    # test_food=Food(name='burger',protein=3,carb=2,fat=3,calories=120)
    # db.session.add(test_food)
    # db.session.commit()
    # test_food_date=Food_date(food_id=1,log_date_id=1)
    # db.session.add(test_food_date)
    # db.session.commit()
    
    # all_dates=Log_date.query.order_by(Log_date.entry_date.desc()).all()
    all_dates=db.session.query(db.func.sum(Food.protein),db.func.sum(Food.carb),db.func.sum(Food.fat),\
        db.func.sum(Food.calories),Log_date.entry_date).select_from(Food).fulljoin(Food_date,\
            Food.id==Food_date.food_id).outerjoin(Log_date,Log_date.id==Food_date.log_date_id).\
                group_by(Log_date.id).order_by(Log_date.entry_date.desc()).all()

    date_results=[]
    for i in all_dates:
        single_date={}
        single_date['protein']=i[0]
        # single_date['carb']=i[1]
        # single_date['fat']=i[2]
        # single_date['calories']=i[3]
        single_date['formatted_date']=datetime.strftime(i.entry_date,'%B %d %Y')
        single_date['entry_date']=i.entry_date
        date_results.append(single_date)
    return render_template('home.html',date_results=date_results)

@app.route('/view/<date>',methods=['GET','POST'])
def view(date):
    single_date=Log_date.query.filter_by(entry_date=date).first()
    # return '<h1> the date id is {}, for {}</h1>'.format(single_date.id,single_date.entry_date)
    if request.method=='POST':
        # return '<h1> the food item added is #{}</h1>'.format(request.form['food-select'])    
        # return request.form['food-select']    
        new_food_date=Food_date(food_id=request.form['food-select'],log_date_id=single_date.id)
        db.session.add(new_food_date)
        db.session.commit()

    
    formatted_date=datetime.strftime(single_date.entry_date,'%B %d %Y')
    # return '<h1> formatted date is :{} '.format(formatted_date)
    all_food=Food.query.all()
    # for i in all_food:
    #     print(i.name)
    log_results=db.session.query(Food.name,Food.protein,Food.carb,Food.fat,Food.calories,\
        Log_date.entry_date).select_from(Food).join(Food_date,Food.id==Food_date.food_id).\
        join(Log_date,Log_date.id==Food_date.log_date_id).filter(Log_date.entry_date==date)


    totals={}
    totals['protein']=0
    totals['carb']=0
    totals['fat']=0
    totals['calories']=0
    for food in log_results:
        totals['protein']+=food.protein
        totals['carb']+=food.carb
        totals['fat']+=food.fat
        totals['calories']+=food.calories

    return render_template('day.html',formatted_date=formatted_date,all_food=all_food,date=date,\
        log_results=log_results,totals=totals)

@app.route('/food',methods=['GET','POST'])
def food():
    if request.method=='POST':
        name=request.form['name']
        protein=int(request.form['protein'])
        carb=int(request.form['carb'])
        fat=int(request.form['fat'])
        
        #calculate calories
        calories=(protein+carb)*4+fat*9

        new_food=Food(name=name,protein=protein,carb=carb,fat=fat,calories=calories)
        db.session.add(new_food)
        db.session.commit()
    #Rendering all foods in the db   
    all_foods = Food.query.all()
    # for i in all_foods:
    #     print (i.name)

    return render_template('add_food.html',foods=all_foods)

if __name__ == '__main__':
    app.run(debug=True)