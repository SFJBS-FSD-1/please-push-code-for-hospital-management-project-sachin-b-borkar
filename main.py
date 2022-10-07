import os
from flask import Flask,request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from http import HTTPStatus
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:welcome$1234@localhost/hospital"
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bed_type = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    patient_status = db.Column(db.String(80), nullable=False)

    @staticmethod
    def register_user(name, phone_number, age ,bed_type,address,state,city,patient_status):
        new_user= Hospital(name=name, phone_number=phone_number, age=age , bed_type=bed_type ,address=address,state=state,city=city,patient_status=patient_status)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_user():
        return Hospital.query.all()

    @staticmethod
    def get_one_user(id):
        return Hospital.query.filter_by(id=id).first()

    @staticmethod
    def delete_user(id):
        delete_user = Hospital.query.filter_by(id=id).delete()
        db.session.commit()
        return delete_user

    @staticmethod
    def update_user(id, address, age, bed_type , state ,city, patient_status):
        update_user = Hospital.query.filter_by(id=id).first()
        print(update_user)
        update_user.address = address
        update_user.age = age
        update_user.bed_type = bed_type
        update_user.state = state
        update_user.city = city
        update_user.patient_status = patient_status
        db.session.commit()
        return update_user

@app.route("/")
def homepage():
    return render_template("home.html")

class AllPatients(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        Hospital.register_user(name=data["name"], phone_number=data["phone_number"], age=data["age"] ,bed_type = data["bed_type"],address= data["address"],state= data["state"],city=data["city"],patient_status=data["patient_status"])
        return jsonify(data)

class GetUsers(Resource):
    def get(self):
        data = Hospital.get_user()
        print(data)
        user_list = []
        print(user_list)
        for i in data:
            temp_dict= {"name":i.name, "phone_number":i.phone_number, "age":i.age, "bed_type":i.bed_type , "address":i.address, "state":i.state , "city":i.city , "patient_status":i.patient_status}
            user_list.append(temp_dict)
            print(user_list)
        return jsonify(user_list)

class oneUser(Resource):
    def get(self, id):
        data = Hospital.get_one_user(id)
        print(data)
        if data:
            print(data.id)
            print(data.name)
            print(data.phone_number)
            print(data.age)
            print(data.bed_type)
            print(data.address)
            print(data.state)
            print(data.city)
            print(data.patient_status)
            return jsonify({"name": data.name, "phone_number": data.phone_number, "age": data.age ,"bed_type":data.bed_type, "address":data.address , "state":data.state ,"city":data.city ,"patient_status":data.patient_status }, {"status": HTTPStatus.OK})
        else:
            # return ({"message":"ID not found","status":404})
            return ({"message": "ID not found", "status": HTTPStatus.NOT_FOUND})

        def put(self, id):
            data = request.get_json()
            print(data)
            Hospital.update_user(id, data["address"], data["age"], data["bed_type"], data["city"],
                                 data["patient_status"])
            if data:
                return jsonify(
                    {"address": data["address"], "age": data["age"], "bed_type": data["bed_type"], "city": data["city"],
                     "patient_status": data["patient_status"]},
                    {"status": HTTPStatus.OK})
            else:
                return HTTPStatus.NOT_FOUND

class deletePatient(Resource):
    def delete(self, id):
        data = Hospital.delete_user(id)
        print(data)
        if data:
            return HTTPStatus.OK
        else:
            return HTTPStatus.NOT_FOUND



api.add_resource(AllPatients,"/register_patient")
api.add_resource(GetUsers,"/get_patients")
api.add_resource(oneUser,"/edit_patient/<int:id>")
api.add_resource(deletePatient,"/delete_patient/<int:id>")

app.run(port=5003)