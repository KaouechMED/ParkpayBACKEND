from MobileAPP import db,bcrypt,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    phone_number=db.Column(db.String(length=8),nullable=False,unique=True)
    cin=db.Column(db.String(length=8),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf_8')
        
    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)
    
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    left_number=db.Column(db.String(length=3), nullable=False)
    right_number=db.Column(db.String(length=4), nullable=False)
    combined_number = db.Column(db.String(length=7),default=left_number + right_number,unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Ticket(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    position=db.Column(db.String(length=20),nullable=False)
    start_datetime=db.Column(db.String(length=20),nullable=False)
    finish_datetime=db.Column(db.String(length=20),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    car_id=db.Column(db.Integer,db.ForeignKey('car.id'),nullable=False)

    
   