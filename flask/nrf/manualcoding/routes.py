from flask import render_template, url_for, flash, redirect, request, Blueprint
from nrf.models.model_user import Post
from nrf.models.models import Comment, Manual, ManualNews, News
from nrf.manualcoding.forms import ManualcodingForm, ManualNewsForm, SectionInputForm, ManualCommentForm, ManualReporterForm
from nrf import db
from sqlalchemy import and_
import datetime

manualcoding = Blueprint('manualcoding', __name__)


# @manualcoding.route("/manualcoding2", methods=['GET', 'POST'])
# # @manualcoding.route("/manualcoding", methods=['GET', 'POST'])
# def insert():
#     form = ManualcodingForm()
#     comment = Comment.query.filter(and_(Comment.sympathycount < 100, Comment.bool_manual == False, Comment.deleted != True)).first()
#     news = News.query.filter(News.aid == comment.aid).first()
#
#     if form.validate_on_submit():
#         # update_comment = Comment.query.get(comment.commentno)
#         update_comment = comment
#         update_comment.bool_manual = True
#         input_data = Manual(etc=form.etc.data, commentno=comment.commentno, oid=comment.oid, aid=comment.aid,
#                             correlation=form.correlation.data)
#
#         db.session.merge(update_comment)
#         db.session.add(input_data)
#         db.session.commit()
#         db.session.close()
#         flash('입력되었습니다!', 'success')
#         return redirect(url_for('manualcoding.insert'))
#     return render_template('manualcoding.html', title="ManualCoding", comment=comment, news=news, form=form)


@manualcoding.route("/manualcoding", methods=['GET', 'POST'])
# @manualcoding.route("/manualnews", methods=['GET', 'POST'])
def manualNews():
    form = ManualNewsForm()
    comment = Comment.query.filter(and_(Comment.sympathycount < 100, Comment.bool_manual == False, Comment.deleted != True)).first()
    news = News.query.filter(News.aid == comment.aid).first()

    if form.validate_on_submit():
        # update_comment = Comment.query.get(comment.commentno)
        update_comment = comment
        update_comment.bool_manual = True
        input_data = ManualNews(oid=comment.oid, aid=comment.aid, commentno=comment.commentno,
                            opinion=form.opinion.data, improvement=form.improvement.data, relation=form.relation.data, positive=form.positive.data, negative=form.negative.data, neutrality=form.neutrality.data)

        db.session.merge(update_comment)
        db.session.add(input_data)
        db.session.commit()
        db.session.close()
        flash('입력되었습니다!', 'success')
        return redirect(url_for('manualcoding.manualNews'))
    return render_template('manual_news.html', title="Manual News", comment=comment, news=news, form=form)


@manualcoding.route("/newsdaylist", methods=['GET', 'POST'])
def newsdaylist():
    form = SectionInputForm()

    if form.validate_on_submit():
        sid1 = form.sid1.data
        searchw = form.searchw.data
        startday_r = form.startday.data + ' 00:00:00'
        endday_r = form.endday.data + ' 00:00:00'
        startday = startday_r[0:4] + '-' + startday_r[4:6] + '-' + startday_r[6:8] + ' 00:00:00'
        endday = endday_r[0:4] + '-' + endday_r[4:6] + '-' + endday_r[6:8] + ' 00:00:00'
        # 수정필요
        # startday = form.startday.data
        # endday = form.endday.data
        # data = db.session.query(News.simple_dt).distinct().filter(and_(News.sid1 == sid1, News.title.like('%' + searchw + '%'))).all()
        # data.sort(reverse=True)
        # result = []
        #
        # for date in data:
        #     result.append(date[0])

        news = News.query.filter(and_(News.sid1 == sid1, News.title.like('%' + searchw + '%'), News.regtime >= startday, News.regtime <= endday)).all()
        newsnum = News.query.filter(and_(News.sid1 == sid1, News.title.like('%' + searchw + '%'), News.regtime >= startday, News.regtime <= endday)).count()

        return render_template('manual_newslist.html', title="Newsday List", news=news, newsnum=newsnum, startday=startday, endday=endday)
        # return render_template('manual_daylist.html', title="Newsday List", result=result)
    return render_template('newsdaylist_input.html', title='Newsday List', form=form)


#아직 예제 manual comment라는 가제 붙임
# @manualcoding.route("/newslist", methods=['GET', 'POST'])
# def newslist():
#     sid1 = request.args.get('sid1')
#
#     news = News.query.filter(and_(News.regtime >= '2018-04-14 00:00:00', News.regtime <= '2018-04-15 00:00:00', News.title.like('%' + '갑질' + '%'))).all()
#     newsnum = News.query.filter(and_(News.regtime >= '2018-04-14 00:00:00', News.regtime <= '2018-04-15 00:00:00', News.title.like('%' + '갑질' + '%'))).count()
#
#     return render_template('manual_newslist.html', title="News List", news=news, newsnum=newsnum)


@manualcoding.route("/newslist/<aid>/commentlist", methods=['GET', 'POST'])
def commentlist(aid):
    form = ManualNewsForm()
    form_re = ManualReporterForm()
    form_co = ManualCommentForm()
    comment = Comment.query.filter(and_(Comment.aid == aid, Comment.bool_manual == False, Comment.deleted != True)).all()
    commentnum = Comment.query.filter(and_(Comment.aid == aid, Comment.bool_manual == False, Comment.deleted != True)).count()

    return render_template('manual_comment.html', title="Comment List", comment=comment, form=form, commentnum=commentnum, form_co=form_co, form_re=form_re)


# @app.route('/processmanual', methods=['POST'])
# def processmanual(commentno):
#     commentno = commentno
#     opinion = form.opinion.data
#     improvement = form.improvement.data
#     relation = form.relation.data
#     positive = form.positive.data
#     negative = form.negative.data
#     neutrality = form.neutrality.data
#     # user =  request.form['username']
#     # password = request.form['password']
#     return json.dumps({'status':'OK', 'commentno':commentno, 'opinion':opinion, 'improvement':improvement, 'relation':relation, 'positive':positive, 'negative':negative, 'neutrality':neutrality})
@manualcoding.route('/processmanual', methods=['POST'])
def processmanual():
    commentno = commentno
    opinion = form.opinion.data
    improvement = form.improvement.data
    relation = form.relation.data
    positive = form.positive.data
    negative = form.negative.data
    neutrality = form.neutrality.data

    if form.validate_on_submit():
        return jsonify({'status':'OK', 'commentno':commentno, 'opinion':opinion, 'improvement':improvement, 'relation':relation, 'positive':positive, 'negative':negative, 'neutrality':neutrality})
    return jsonify({'error': 'missing data..'})


# @manualcoding.route("/newslist", method=['GET,POST'])
# def newslist():
#     sid1 = form.sid1.data
#     data = db.session.query(News).filter(and_(News.sid1 == sid1)).all()
#     data.sort(reverse=True)
#
#     result = []
#
#     for date in data:
#         result.append(date[0])
#     return render_template('manual_daylist.html', title="News List", result=result)
