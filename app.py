from flask import Flask,request
app=Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"
db=SQLAlchemy(app)

class Drink(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    desc=db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name}-{self.desc}"


@app.route('/')
def index():
    return "Hello!"

@app.route('/drinks')
def get_drinks():
    drinks=Drink.query.all()
    print(drinks)
    output=[]
    for drink in drinks:
        drink_data={'name':drink.name,'description':drink.desc,}
        output.append(drink_data)

    return {"drinks":output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink=Drink.query.get_or_404(id)
    return {'name':drink.name,'description':drink.desc}

@app.route('/drinks',methods=['POST'])
def add_drink():
    drink=Drink(name=request.json['name'], desc=request.json['desc'])
    db.session.add(drink)
    db.session.commit()
    return f"successfully added id:{drink.id}"

@app.route('/drinks/<id>',methods=['DELETE'])
def delete_drink(id):
    drink=Drink.query.get(id)
    if drink is None:
        return "not found"
    db.session.delete(drink)
    db.session.commit()
    return "deleted."

@app.route('/drinks/<id>',methods=['PATCH'])
def update_drink(id):
    drink=Drink.query.get(id)
    if drink is None:
        return "no record found to update"
    data=request.get_json()
    # print("blah....blah",drink)
    if 'name' in data:
        drink.name=data['name']
    if 'desc' in data:
        drink.desc=data['desc']
    db.session.commit()
    return f"record {drink.id} updated"
if __name__ == '__main__':  
   app.run(debug=True)