from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

fruits=["apple","Banana","Watermelon","Orange","Stroberry"]
name = "70359 Shimpei"

#TODOリスト用のデータベースを作成（ sqlAlchemyを使用）
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#db Table　の作成
#dbの内容は、DB Browser からみる　（不具合でstudio codeから見れない）
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.today())

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/' )
def index():
    return render_template('index.html',pagetitle ="INDEX PAGE",name=name)
    
@app.route('/about')
def about():
 
   return render_template('about.html',pagetitle="ABOUT PAGE" ,fruits=fruits,name=name)


#task投稿メソッドを作成し、todoページに埋め込み
@app.route('/todo',methods=['POST', 'GET'])
def todo():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task' 
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html',pagetitle="TODO PAGE",tasks=tasks,name=name)


""" 入力したtaskを削除するメソッド """
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was a problem deleting that task'

""" 入力情報をupdateするメソッド """
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue updating your task' 
    else:
        return render_template('update.html',task = task)



if __name__ == "__main__":
 app.run(debug=True)