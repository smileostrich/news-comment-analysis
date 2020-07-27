from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class VisualizeForm(FlaskForm):
    sid1 = StringField('Section')
    startday = StringField('시작일', validators=[DataRequired(), Length(min=8, max=8)])
    endday = StringField('종료일', validators=[DataRequired(), Length(min=8, max=8)])
    submit = SubmitField('submit')
