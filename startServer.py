from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


#Creating flask app
app = Flask(__name__)

#Password hashing
bcrypt = Bcrypt(app=app)

#Configuring app for database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://demo_db_oq5f_user:ioHUbrsyz2Y4fjwuH6WcoKPPKeZG5Za9@dpg-ckong8vkc2qc73ekavc0-a.oregon-postgres.render.com/demo_db_oq5f"
db = SQLAlchemy(app)

#initialize JWT 
app.config["JWT_SECRET_KEY"] = "stocktradingdemo"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False 
jwt = JWTManager(app=app)



#Usermodel for postgres
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email= db.Column(db.String(80),unique=True,nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


#Creating database if doesn't exist
with app.app_context():
    db.create_all()


@app.route("/",methods=["GET","POST"])
def home():
    return "</h1>Hello world!</h1>"

@app.route("/api/auth/register",methods=["GET","POST"])
def register():
    data = request.get_json()

    name = data["username"]
    email = data["email"]
    password = data["password"]

    #checking if email already in use
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message":"Email address already registered"}), 400
    
    existing_user = User.query.filter_by(name=name).first()

    if existing_user:
        return jsonify({"message":"Username already taken"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(name=name, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"Registration successful"}), 201
    
    except Exception as e:
        return jsonify({"message":"Registration failed"}), 500
    


@app.route("/api/auth/login",methods=["GET","POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        return jsonify({"message":"Login successfuly","token":access_token}), 200
    
    return jsonify({"message":"Invalid email or password"}), 401


# protected route
@app.route("/api/data/user",methods=["GET","POST"])
@jwt_required
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({"message": "This is a protected route for user: " + current_user}), 200





if __name__ == "__main__":
    app.run(debug=True)



