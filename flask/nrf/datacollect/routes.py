from flask import render_template, url_for, flash, redirect, request, Blueprint
from nrf.models.models import Comment, News
from nrf.datacollect.forms import DatacollectForm, SectionInputForm
from nrf import db
from sqlalchemy import and_
from threading import Thread
from flask import request
from nrf.datacollect.utils import initial_request
import pandas
import time
from nrf.datacollect.crawl import main

datacollect = Blueprint('datacollect', __name__)


@datacollect.route("/datacollect", methods=['GET', 'POST'])
def dcollectmain():
    form = DatacollectForm()

    if form.validate_on_submit():
        startday = form.startday.data
        endday = form.endday.data
        sid1 = form.sid1.data

        main(sid1, startday, endday)
        flash('crawling done!', 'success')
        return redirect(url_for('datacollect.dcollectmain'))
    return render_template('collect.html', title="Data Collecting", form=form)


@datacollect.route("/datacheck", methods=['GET'])
def datacheck():
    comment = Comment.query.filter(Comment.blind == False).count()
    time.sleep(10)
    comment2 = Comment.query.filter(Comment.blind == False).count()

    if comment == comment2:
        result = '중지됨'
    else:
        result = '수집중'
    return render_template('datacheck.html', title="check", result=result)


@datacollect.route("/newsdaylistm", methods=['GET', 'POST'])
def newsdaylistm():
    form = SectionInputForm()

    if form.validate_on_submit():
        sid1 = form.sid1.data
        data = db.session.query(News.simple_dt).distinct().filter(News.sid1 == sid1).all()
        data.sort(reverse=True)

        result = []

        for date in data:
            result.append(date[0])
        return render_template('newsdaylist.html', title="News List", result=result)
    return render_template('manual_newsdaylist_input.html', title='News List', form=form)
