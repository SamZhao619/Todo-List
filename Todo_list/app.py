import os

from flask import Flask, request, jsonify
from flask_admin import Admin, AdminIndexView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

admin = Admin(
    app,
    name='待办系统',
    index_view=AdminIndexView(
        name='待办列表',
        template='index.html',
        url='/admin'
    )
)

# 获取当前目录的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
# sqlite数据库文件存放路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
# 创建数据库对象
db = SQLAlchemy(app)
# 数据库
db.init_app(app)
# 迁移
migrate = Migrate(app, db)


def to_json(data):
    tem_data = []
    for i in data:
        dict = i.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        tem_data.append(dict)
    return tem_data


# 待办数据库模型
class todo(db.Model):
    __tablename__ = 'todo'
    todo_No = db.Column(db.Integer, primary_key=True)
    todo_name = db.Column(db.String(255), comment="待办名称")
    todo_desc = db.Column(db.String(255), comment="待办描述")
    isfinish = db.Column(db.Integer, comment="是否完成|0=未完成，1=已完成", default=0)
    todo_date = db.Column(db.String(255), comment="截止时间")


# 待办接口
# 创建待办
@app.route("/create_todo/", methods=['POST'])
def create_todo():
    rd = request.get_json()
    db.session.add(
        todo(
            todo_name=rd['todo_name'],
            todo_desc=rd['todo_desc'],
            isfinish=int(rd['isfinish']),
            todo_date=rd['todo_date'],
        )
    )
    try:
        db.session.commit()
        return jsonify(
            {"code": 0, "msg": "ok", "data": []}
        )
    except Exception as e:
        return jsonify(
            {"code": 9, "msg": "创建待办任务失败【%s】" % str(e), "data": []}
        )


# 更新待办
@app.route("/update_todo/", methods=['POST'])
def update_todo():
    rd = request.get_json()
    todo.query.filter(todo.todo_No == rd['todo_No']).update(rd)
    try:
        db.session.commit()
        return jsonify(
            {"code": 0, "msg": "ok", "data": []}
        )
    except Exception as e:
        return jsonify(
            {"code": 9, "msg": "更新待办任务失败【%s】" % str(e), "data": []}
        )


# 删除待办
@app.route("/delete_todo/", methods=['POST'])
def delete_todo():
    rd = request.get_json()
    todo.query.filter(todo.todo_No == rd['todo_No']).delete()
    try:
        db.session.commit()
        return jsonify(
            {"code": 0, "msg": "ok", "data": []}
        )
    except Exception as e:
        return jsonify(
            {"code": 9, "msg": "删除待办任务失败【%s】" % str(e), "data": []}
        )


# 获取所有待办
@app.route("/get_all_todo/", methods=['GET'])
def get_all_todo():
    try:
        data = {"todo_finish": to_json(todo.query.filter(todo.isfinish == 1).all()), "todo_nofinish": to_json(todo.query.filter(todo.isfinish == 0).all())}
        return jsonify(
            {"code": 0, "msg": "ok", "data": data}
        )
    except Exception as e:
        return jsonify(
            {"code": 9, "msg": "获取待办任务失败【%s】" % str(e), "data": []}
        )


if __name__ == '__main__':
    app.run(debug=True)
