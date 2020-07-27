from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class DatacollectForm(FlaskForm):
    sid1 = StringField('Section', validators=[DataRequired(), Length(min=3, max=3)])
    startday = StringField('시작일', validators=[DataRequired(), Length(min=8, max=8)])
    endday = StringField('종료일', validators=[DataRequired(), Length(min=8, max=8)])
    submit = SubmitField('등록')


class SectionInputForm(FlaskForm):
    sid1 = StringField('Section', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('등록')
