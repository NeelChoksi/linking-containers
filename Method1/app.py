from flask import Flask, request, jsonify, make_response, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import environ
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))

    def json(self):
        return {'id': self.id, 'fname': self.fname, 'lname': self.lname}

    def lastName(self):
        return str(self.lname)


db.create_all()


@app.route('/', methods=['GET'])
def index():
    try:
        new_student = Student(fname='Dave', lname='Smith')
        db.session.add(new_student)
        db.session.commit()
        return "Dave Smith created.go to http://localhost:4000/greet and enter Dave as first name."
    except Exception as e:
        return make_response(jsonify({'message': 'error creating student'}), 500)


@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


@app.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        new_student = Student(fname=data['fname'], lname=data['lname'])
        db.session.add(new_student)
        db.session.commit()
        return make_response(jsonify({'message': 'student created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating student'}), 500)


@app.route('/students', methods=['GET'])
def get_students():
    try:
        students = Student.query.all()
        return make_response(jsonify({'students': [s.json() for s in students]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting students'}), 500)


@app.route('/greet', methods=['GET', 'POST'])
def greet():
    if request.method == 'POST':
        fname = request.form['firstname']
        return redirect(url_for("get_stud_by_fname", fname=fname))
    else:
        return render_template("greeting.html")


@app.route('/greet_student/<fn>', methods=['GET'])
def greet_student(fn):
    try:
        student = Student.query.filter_by(fname=fn).first()
        x = student.json()
        y = json.loads(x)
        return make_response(jsonify({'student': student.json()}), 200)

        return f"<h6> Hello {y['fname']} {y['lname']} </h6>"
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'error getting student'}), 500)


@app.route('/get_student_by_fname/<fname>', methods=["GET"])
def get_stud_by_fname(fname):
    try:
        student = Student.query.filter_by(fname=fname).first()
        ln = student.lastName()
        return f"<h6> Hello {fname} {ln} </h6>"
        # return make_response(jsonify({'student': student.json(), 'dt': str(type(student))}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting student'}), 500)
