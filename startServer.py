from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


#Creating flask app
app = Flask(__name__)

#Password hashing
bcrypt = Bcrypt(app=app)

#Configuring app for database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://demo_db_s8s0_user:SEQuQsrWuljq89be522VUKo3an8GRf52@dpg-ckt9jrg168ec73b8l3l0-a.oregon-postgres.render.com/demo_db_s8s0"
db = SQLAlchemy(app)                    

#initialize JWT 
app.config["JWT_SECRET_KEY"] = "stocktradingdemo"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False 
jwt = JWTManager(app=app)



#Usermodel for postgres
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    card_number = db.Column(db.String(16), nullable=True)
    expiry_date = db.Column(db.String(5), nullable=True)
    cvv = db.Column(db.String(3), nullable=True)


#Creating database if doesn't exist
with app.app_context():
    db.create_all()


@app.route("/",methods=["GET","POST"])
def home():
    return "</h1>Hello world!</h1>"


#api for register 
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    first_name = data["first_name"]
    last_name = data["last_name"]
    username = data["username"]
    email = data["email"]
    password = data["password"]
    address = data.get("address")
    city = data.get("city")
    state = data.get("state")
    zip_code = data.get("zip")
    card_number = data.get("card_number")
    expiry_date = data.get("expiry_date")
    cvv = data.get("cvv")

    # Checking if email or username is already in use
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email address already registered"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "Username already taken"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=hashed_password,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        card_number=card_number,
        expiry_date=expiry_date,
        cvv=cvv,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        return jsonify({"message": "Registration failed","error":str(e)}), 500
    


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



