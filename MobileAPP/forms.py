from flask_wtf import FlaskForm
from wtforms import SearchField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError,Regexp
from MobileAPP.models import User,Car


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False
    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('username already exist ! try another')
    
    def validate_phone_number(self,number_to_check):
        number=User.query.filter_by(phone_number=number_to_check.data).first()
        if number:
            raise ValidationError('phone number already exist ! try another')
        
    def validate_cin(self,cin_to_check):
        cin=User.query.filter_by(cin=cin_to_check.data).first()
        if cin:
            raise ValidationError('cin already exist ! try another')
            
    username=SearchField(label='Username:',validators=[Length(min=4,max=30),DataRequired()])
    phone_number=SearchField(label='number:',validators=[Length(8),DataRequired(),Regexp(r'^\d+$')])
    cin=SearchField(label='cin:',validators=[Length(8),DataRequired(),Regexp(r'^\d+$')])
    password=PasswordField(label='Password:',validators=[Length(min=6),DataRequired()])
    passwordConfirm=PasswordField(label='Confirm Password:',validators=[EqualTo('password'),DataRequired()])
    submit=SubmitField(label='Create Account')
    
    
class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    username=SearchField(label='Username:',validators=[DataRequired()])
    password=PasswordField(label='Password:',validators=[DataRequired()])
    submit=SubmitField(label='Sign in')
    

class CarForm(FlaskForm):
    class Meta:
        csrf = False   
    
    """def validate_combined_number(self,left_number_to_check,right_number_to_check):
        combined_number=Car.query.filter_by(combined_number=left_number_to_check.data+right_number_to_check.data).first()
        if combined_number:
            raise ValueError('car already exist')"""

    left_number = SearchField(label='Left Number:', validators=[Length(max=3),DataRequired(), Regexp(r'^\d+$')])
    right_number = SearchField(label='Right Number:', validators=[Length(max=4),DataRequired(), Regexp(r'^\d+$')])
    submit = SubmitField(label='Create Car')