from MobileAPP import app
from flask import request,Response,session
from MobileAPP.models import User,Car
from MobileAPP.forms import RegisterForm, LoginForm ,CarForm
from MobileAPP import db
from flask_login import login_user,current_user,login_required
import json
from twilio.rest import Client

#otp api twilio
with open('.\OTP\keys.json', 'r') as file:
    keys = json.load(file)
client = Client(keys['account_sid'], keys['auth_token'])

# Registration API endpoint
@app.route('/api/register', methods=['POST'])
def register_page():
    data = request.get_json()  
    form = RegisterForm(data=data)
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              phone_number=form.phone_number.data,
                              cin=form.cin.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        response_data={"message": "User registered successfully"}
        status_code=201
    if form.errors !={}:
        errors = [error for error in form.errors.items()]
        response_data={'errors': errors}
        status_code=400
    json_response = json.dumps(response_data)
    return Response(response=json_response,status=status_code,content_type='application/json')
    
# Login API endpoint
@app.route('/api/login', methods=['POST'])
def iniate_login():
    data = request.get_json()
    form = LoginForm(data=data)
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            #otp send
            verification = client.verify.v2.services(keys['verify_sid']) \
                .verifications \
                .create(to="+216"+attempted_user.phone_number, channel="sms")
            session['user_id'] = attempted_user.id
            session['verification_sid'] = verification.sid
            response_data = {"message": "OTP sent for verification"}
            status_code = 201
        else:
            response_data={'error': 'Invalid username or password'}
            status_code=401
    else:
        errors = [error for error in form.errors.items()]
        response_data={'errors': errors}
        status_code=401
    json_response = json.dumps(response_data)
    return Response(response=json_response,status=status_code,content_type='application/json')

@app.route('/api/submit_otp', methods=['POST'])
def submit_otp():
    data = request.get_json()
    otp_code = data.get('otp_code')
    user_id = session.get('user_id')
    verification_sid = session.get('verification_sid')

    if not otp_code or not user_id or not verification_sid:
        json_response=json.dumps({'error': 'Invalid OTP submission'})
        status_code=401
    attempted_user = User.query.get(user_id)
    verification_check = client.verify.v2.services(keys['verify_sid']) \
        .verification_checks \
        .create(code=otp_code, verification_sid=verification_sid)

    if verification_check.status == "approved":
        login_user(attempted_user)
        session.pop('verification_sid', None)
        json_response=json.dumps({"message": "User logged in successfully"})
        status_code=201
    else:
        json_response=json.dumps({'error': 'Invalid OTP'})
        status_code=401
    return Response(response=json_response,status=status_code,content_type='application/json')

# Logout API endpoint
@login_required
@app.route('/api/logout', methods=['POST'])
def logout_page():
    if 'user_id' in session:  
        session.pop('user_id')
        response_data = {"message": "User logged out successfully"}
        status_code = 201
    else:
        response_data = {'error': 'User not logged in'}
        status_code = 401
    json_response = json.dumps(response_data)
    return Response(response=json_response, status=status_code, content_type='application/json')

# create CAR API endpoint
@app.route('/api/addcar', methods=['POST'])
@login_required
def create_car_page():
    data = request.get_json()  
    form = CarForm(data=data)
    if form.validate_on_submit():
        car_to_create = Car(
                            left_number=form.left_number.data,
                            right_number=form.right_number.data,
                              user_id=current_user.id)
        combined_number=Car.query.filter_by(combined_number=form.left_number.data+form.right_number.data,user_id=current_user.id).first()
        if combined_number:
            response_data={'errors': "car already exist"}
            status_code=400
        else:
            db.session.add(car_to_create)
            db.session.commit()
            response_data={"message": "car  added successfully"}
            status_code=201
    json_response = json.dumps(response_data)
    return Response(response=json_response,status=status_code,content_type='application/json')

@app.route('/api/getcars', methods=['GET'])
@login_required
def get_cars_page():
    cars = Car.query.all()
    car_list = [{'car_id': car.car_id, 'left_number': car.left_number, 'right_number': car.right_number,'combined_number':car.combined_number} for car in cars]
    return json.dumps({'cars': car_list})