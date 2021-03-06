import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError


def character_check(form, field):
    excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    phone = StringField(validators=[Required()])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be between 6 and 12 characters in length.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must be equal!')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='PIN Key must be exactly 32 characters in length.')])
    submit = SubmitField()

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit, 1 lowercase letter, 1 uppercase letter, and 1 special character.")

    def validate_phone(self, phone):
        ph = re.compile(r'^(?:\s*)\d{4}-\d{3}-\d{4}(?:\s*)$')
        if not ph.match(self.phone.data):
            raise ValidationError("Phone must be in the format XXXX-XXX-XXXX (with the dashes)")


class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = StringField(validators=[Required()])
    submit = SubmitField()

    def validate_pin(self, pin):
        pi = re.compile(r'^(?:\s*)\d{6}(?:\s*)$')
        if not pi.match(self.pin.data):
            raise ValidationError("PIN must only contain integers and have a length of 6.")
