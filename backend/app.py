from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)  # フロントエンド（React）と通信するためにCORSを許可

# SQLite データベースの設定
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# データベース初期化
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ToDoモデル
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "completed": self.completed}

# ToDo一覧を取得
@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

# ToDoを追加
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    new_todo = Todo(title=data["title"])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# ToDoを取得
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    return jsonify(todo.to_dict()) if todo else ("Not Found", 404)

# ToDoを更新
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    todo = Todo.query.get(todo_id)
    if todo:
        todo.title = data.get("title", todo.title)
        todo.completed = data.get("completed", todo.completed)
        db.session.commit()
        return jsonify(todo.to_dict())
    return "Not Found", 404

# ToDoを削除
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return "", 204
    return "Not Found", 404

# サーバー起動
if __name__ == "__main__":
    app.run(debug=True)




