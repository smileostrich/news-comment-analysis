from flask import render_template, url_for, flash, redirect, request, Blueprint
from nrf.models.models import Comment, Manual, News
from nrf.visualize.forms import VisualizeForm
from nrf import db
from datetime import datetime, date, timedelta

visualize = Blueprint('visualize', __name__)


@visualize.route("/visualize/main", methods=['GET', 'POST'])
def main():
    return render_template('visualize_main.html')


@visualize.route("/visualize/graph1")
def graph1():
    comment = Comment.query.count()
    news = News.query.count()

    return render_template('graph1.html', comment=comment, news=news)


@visualize.route("/visaulize/datainfo")
def info():
    return render_template('visualize/visualinfo.html')


@visualize.route("/visualize/graph2")
def graph2():
    # nowdate = comment.strftime('%Y-%m-%d')
    sday = datetime(2017, 5, 1)
    eday = datetime(2017, 6, 1)
    totday = (eday - sday).days

    c_list = []
    n_list = []
    c_list.append(1) # 1 == comment
    n_list.append(2) # 2 == news
    for v_day in range(0, totday+1):
        s_day = sday + timedelta(days=v_day)
        e_day = sday + timedelta(days=v_day+1)
        c_num = Comment.query.filter(Comment.regtime >= s_day, Comment.regtime < e_day).count()
        c_list.append(c_num)

    for v_day in range(0, totday+1):
        s_day = sday + timedelta(days=v_day)
        e_day = sday + timedelta(days=v_day+1)
        n_num = News.query.filter(News.regtime >= s_day, News.regtime < e_day).count()
        n_list.append(n_num)

    # test = len(c_list)
    # news = News.query.count()
    # news = News.query.filter(News.aid == comment.aid).first()

    return render_template('graph2.html', comment=c_list, news=n_list)


@visualize.route("/visualize/graph3")
def graph3():
    sday = datetime(2017, 5, 1)
    eday = datetime(2017, 5, 15)
    totday = (eday - sday).days

    c_list = []
    n_list = []
    c_list.append(1)  # 1 == comment
    n_list.append(2)  # 2 == news
    for v_day in range(0, totday + 1):
        s_day = sday + timedelta(days=v_day)
        e_day = sday + timedelta(days=v_day + 1)
        c_num = Comment.query.filter(Comment.regtime >= s_day, Comment.regtime < e_day).count()
        c_list.append(c_num)

    for v_day in range(0, totday + 1):
        s_day = sday + timedelta(days=v_day)
        e_day = sday + timedelta(days=v_day + 1)
        n_num = News.query.filter(News.regtime >= s_day, News.regtime < e_day).count()
        n_list.append(n_num)

    return render_template('visualize/graph3.html', comment=c_list, news=n_list)


@visualize.route("/visualize/graph4")
def graph4():
    sday = datetime(2017, 5, 1).date()
    eday = datetime(2017, 5, 20).date()
    totday = (eday - sday).days

    c_list = []
    n_list = []
    c_list.append(1)  # 1 == comment
    n_list.append(2)  # 2 == news
    for v_day in range(0, totday + 1):
        s_day = sday + timedelta(days=v_day)
        e_day = sday + timedelta(days=v_day + 1)
        c_num = Comment.query.filter(Comment.regtime >= s_day, Comment.regtime < e_day).count()
        c_list.append(c_num)

    for v_day in range(0, totday + 1):
        s_day = sday + timedelta(days=v_day)
        e_day = sday + timedelta(days=v_day + 1)
        n_num = News.query.filter(News.regtime >= s_day, News.regtime < e_day).count()
        n_list.append(n_num)

    return render_template('visualize/graph4.html', comment=c_list, news=n_list)


@visualize.route("/visualize/graph_condition", methods=['GET', 'POST'])
def graph_condition():
    form = VisualizeForm()

    if form.validate_on_submit():
        startday = form.startday.data
        endday = form.endday.data
        sid1 = form.sid1.data
        sday = datetime.strptime(startday, '%Y%m%d').date()
        eday = datetime.strptime(endday, '%Y%m%d').date()
        totday = (eday - sday).days

        c_list = []
        n_list = []
        c_list.append(1)  # 1 == comment
        n_list.append(2)  # 2 == news

        if sid1 == '':
            for v_day in range(0, totday + 1):
                s_day = sday + timedelta(days=v_day)
                e_day = sday + timedelta(days=v_day + 1)
                c_num = Comment.query.filter(Comment.regtime >= s_day, Comment.regtime < e_day).count()
                c_list.append(c_num)
        elif sid1 is not None:
            for v_day in range(0, totday + 1):
                s_day = sday + timedelta(days=v_day)
                e_day = sday + timedelta(days=v_day + 1)
                c_subq = db.session.query(News.aid, News.regtime).filter(News.sid1 == sid1).subquery()
                c_num = Comment.query.join(c_subq, Comment.aid == c_subq.c.aid).filter(Comment.regtime >= s_day, Comment.regtime < e_day).count()
                c_list.append(c_num)

        for v_day in range(0, totday + 1):
            s_day = sday + timedelta(days=v_day)
            e_day = sday + timedelta(days=v_day + 1)
            n_num = News.query.filter(News.regtime >= s_day, News.regtime < e_day).count()
            n_list.append(n_num)

        return render_template('visualize/graph_condition.html', comment=c_list, news=n_list)
    return render_template('visualize/condition_input.html', form=form)
