from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class ManualcodingForm(FlaskForm):
    etc = StringField('기타', validators=[DataRequired()])
    correlation = BooleanField('기사와 상관없는 댓글')
    submit = SubmitField('등록')


class ManualNewsForm(FlaskForm):
    opinion = StringField('의견 표현')
    improvement = StringField('개선 대상/방향')
    relation = SelectField(
        '관련성',
        choices=[('0', '직접 관련'), ('1', '간접 관련'), ('2', '무관')]
    )
    positive = StringField('긍정')
    negative = StringField('부정')
    neutrality = StringField('중립')
    submit = SubmitField('등록')


class SectionInputForm(FlaskForm):
    sid1 = StringField('Section', validators=[DataRequired(), Length(min=3, max=3)])
    searchw = StringField('단어')
    startday = StringField('시작일', validators=[DataRequired(), Length(min=8, max=8)])
    endday = StringField('종료일', validators=[DataRequired(), Length(min=8, max=8)])
    submit = SubmitField('등록')


class ManualCommentForm(FlaskForm):
    posorneg = StringField('긍정/부정 여부')
    reason = StringField('이유')


class ManualReporterForm(FlaskForm):
    posorneg = StringField('긍정/부정 여부')
    reason= StringField('이유')