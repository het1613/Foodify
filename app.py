from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
app.config['SQLALCHEMY_BINDS'] = {'goal':'sqlite:///goal.db'}
db=SQLAlchemy(app)

class FoodList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, default=0)
    fat = db.Column(db.Integer, default=0)
    protein = db.Column(db.Integer, default=0)
    carbs = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Goal(db.Model):
    __bind_key__ = 'goal'

    id = db.Column(db.Integer, primary_key=True)
    calories_goal = db.Column(db.Integer, default=0)
    fat_goal = db.Column(db.Integer, default=0)
    protein_goal = db.Column(db.Integer, default=0)
    carbs_goal = db.Column(db.Integer, default=0)


@app.route('/', methods=['POST', 'GET'])
def index():
    user_calories_goal = 0
    user_fat_goal = 0
    user_protein_goal = 0
    user_carbs_goal = 0

    if request.method=='POST':

        if "food-log" in request.form:
            food_content = request.form['food']
            calories_content = request.form['calories']
            fat_content = request.form['fat']
            protein_content = request.form['protein']
            carbs_content = request.form['carbs']

            new_food = FoodList(food=food_content, calories=calories_content, fat=fat_content, protein=protein_content, carbs=carbs_content)

            try:
                db.session.add(new_food)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your food item!'
        
        else:
            user_calories_goal = request.form['calorie-goal']
            user_fat_goal = request.form['fat-goal']
            user_protein_goal = request.form['protein-goal']
            user_carbs_goal = request.form['carbs-goal']

            new_goal = Goal(calories_goal=user_calories_goal, fat_goal=user_fat_goal, protein_goal=user_protein_goal, carbs_goal=user_carbs_goal)

            try:
                db.session.add(new_goal)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue setting your goal!"
    
    else:
        items = FoodList.query.order_by(FoodList.date_created).all()
        goals = Goal.query.all()
        total_calories = 0
        total_fat = 0
        total_protein = 0
        total_carbs = 0

        if items:
            for food in items:
                total_calories += float(food.calories)
                total_fat += float(food.fat)
                total_protein += float(food.protein)
                total_carbs += float(food.carbs)
        else:
            print('list empty')

        if not goals:
            goals.append(Goal(calories_goal=user_calories_goal, fat_goal=user_fat_goal, protein_goal=user_protein_goal, carbs_goal=user_carbs_goal))

        return render_template('index.html', items = items, goals = goals[-1], total_calories = total_calories, total_fat = total_fat, total_protein = total_protein, total_carbs = total_carbs)
 

@app.route('/delete/<int:id>')
def delete(id):
    food_to_delete = FoodList.query.get_or_404(id)

    try:
        db.session.delete(food_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting that food item.'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item=FoodList.query.get_or_404(id)

    if request.method=='POST':
        item.food=request.form['food']
        item.calories = request.form['calories']
        item.fat = request.form['fat']
        item.protein = request.form['protein']
        item.carbs = request.form['carbs']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating that food item."
    
    else:
        return render_template('update.html', item=item)

@app.route('/reset')
def reset():
    items = FoodList.query.order_by(FoodList.date_created).all()
    goals = Goal.query.all()
    
    for i in range(len(items)):
        try:
            db.session.delete(FoodList.query.get_or_404(i+1))
            db.session.commit()
        except:
            return "There was an issue resetting the app."

    for i in range(len(goals)):
        try:
            db.session.delete(Goal.query.get_or_404(i+1))
            db.session.commit()
        except:
            return "There was an issue resetting the app."

    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
