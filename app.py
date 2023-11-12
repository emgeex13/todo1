from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
app.app_context().push()


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata') ) )

    # Runs when query is executed
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Done(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata') ) )

    # Runs when query is executed
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # return 'Hello, World!'
    # todo = Todo(title="Hello, World!", desc="This is a description")
    # db.session.add(todo)
    # db.session.commit()

    # posting a new todo
    if request.method=='POST':
        # print("posted")
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        print(f"Title: {title}, Desc: {desc} posted successfully!")

    allTodo = Todo.query.all()
    allDone = Done.query.all()
    print("All done: \n", allDone,"\n\n")

    # print(allTodo)
    return render_template('index.html', allTodo=allTodo, allDone=allDone)

@app.route('/showAll')
def showAll():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is the show all page!'

@app.route('/delete/<string:type1>/<int:sno>')
def delete(type1,sno):
    print("---------------\n\n\n\n")
    # type1=request.args.get('type1')
    print(type1)
    # if type1=="todo":
    #     todo = Todo.query.filter_by(sno=sno).first()
    # elif type1=="done":
    #     todo = Done.query.filter_by(sno=sno).first()
    todo = eval(f"{type1}.query.filter_by(sno=sno).first()")
    db.session.delete(todo)
    db.session.commit()
    print(f"Deleted sno: {sno} successfully!")
    return redirect('/')



@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.date_created = datetime.now(pytz.timezone('Asia/Kolkata') )
        db.session.add(todo)
        db.session.commit()
        print(f"Updated sno: {sno} successfully!")
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/done/<int:sno>')
def done(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    done = Done(title=todo.title, desc=todo.desc, date_created=todo.date_created)
    db.session.delete(todo)
    db.session.commit()
    db.session.add(done)
    db.session.commit()
    print(f"Moved sno: {sno} to done successfully!")
    return redirect('/')



@app.route('/undone/<int:sno>')
def undo(sno):
    done = Done.query.filter_by(sno=sno).first()
    todo = Todo(title=done.title, desc=done.desc, date_created=done.date_created)
    db.session.delete(done)
    db.session.commit()
    db.session.add(todo)
    db.session.commit()
    print(f"Moved sno: {sno} to todo successfully!")
    return redirect('/')

@app.route('/products')
def hello():
    return 'Hello, this is our products page!'


if __name__ == '__main__':
    app.run(debug=True, port=8080)