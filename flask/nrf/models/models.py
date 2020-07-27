# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Comment(db.Model):
    __tablename__ = 'comment'

    contents = db.Column(db.Text, nullable=False)
    commentno = db.Column(db.String(11), primary_key=True)
    useridno = db.Column(db.String(50))
    userid = db.Column(db.String(50), nullable=False)
    regtime = db.Column(db.DateTime)
    modtime = db.Column(db.DateTime)
    sympathycount = db.Column(db.Integer)
    best = db.Column(db.Boolean)
    antipathycount = db.Column(db.Integer)
    aid = db.Column(db.ForeignKey('news.aid'), nullable=False)
    oid = db.Column(db.String(4), nullable=False)
    parentcommentno = db.Column(db.String(11))
    modtimegmt = db.Column(db.DateTime)
    regtimegmt = db.Column(db.DateTime)
    blind = db.Column(db.Boolean)
    expose = db.Column(db.Boolean)
    visible = db.Column(db.Boolean)
    secret = db.Column(db.Boolean)
    anonymous = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)
    blindreport = db.Column(db.Boolean)
    mentions = db.Column(db.Text)
    middleblindreport = db.Column(db.Boolean)
    replylevel = db.Column(db.Integer)
    replycount = db.Column(db.Integer)
    replyallcount = db.Column(db.Integer)
    idprovider = db.Column(db.String(20))
    idtype = db.Column(db.String(20))
    bool_manual = db.Column(db.Boolean, server_default=db.FetchedValue())

    news = db.relationship('News', primaryjoin='Comment.aid == News.aid', backref='comments')


class Manual(db.Model):
    __tablename__ = 'manual'

    manual_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    etc = db.Column(db.String(20))
    correlation = db.Column(db.Boolean, nullable=False)
    aid = db.Column(db.ForeignKey('news.aid'), nullable=False)
    oid = db.Column(db.String(4), nullable=False)
    commentno = db.Column(db.ForeignKey('comment.commentno'), nullable=False)

    news = db.relationship('News', primaryjoin='Manual.aid == News.aid', backref='manuals')
    comment = db.relationship('Comment', primaryjoin='Manual.commentno == Comment.commentno', backref='manuals')


class News(db.Model):
    __tablename__ = 'news'

    title = db.Column(db.String(500), nullable=False)
    oid = db.Column(db.String(4), nullable=False)
    aid = db.Column(db.String(11), primary_key=True)
    sid1 = db.Column(db.String(3), nullable=False)
    summary = db.Column(db.String(1000))
    officename = db.Column(db.String(20))
    sid2 = db.Column(db.String(3))
    total_cnt = db.Column(db.Integer)
    comment_cnt = db.Column(db.Integer)
    reply_cnt = db.Column(db.Integer)
    woman_rate = db.Column(db.Integer)
    man_rate = db.Column(db.Integer)
    teens_rate = db.Column(db.Integer)
    twenties_rate = db.Column(db.Integer)
    thirties_rate = db.Column(db.Integer)
    forties_rate = db.Column(db.Integer)
    fifties_rate = db.Column(db.Integer)
    regtime = db.Column(db.DateTime)
    modtime = db.Column(db.DateTime)
    like_cnt = db.Column(db.Integer)
    warm_cnt = db.Column(db.Integer)
    sad_cnt = db.Column(db.Integer)
    angry_cnt = db.Column(db.Integer)
    want_cnt = db.Column(db.Integer)
    contents = db.Column(db.Text)
    simple_dt = db.Column(db.DateTime)
    recommendmain_cnt = db.Column(db.Integer)
    deletedcomment_cnt = db.Column(db.Integer)
    violaterule_cnt = db.Column(db.Integer)
    blindcomment_cnt = db.Column(db.Integer)
    blindreply_cnt = db.Column(db.Integer)


class ManualComment(db.Model):
    __tablename__ = 'manual_comment'

    idx = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    oid = db.Column(db.String(4), nullable=False)
    aid = db.Column(db.ForeignKey('news.aid'), nullable=False)
    commentno = db.Column(db.ForeignKey('comment.commentno'), nullable=False)
    posorneg = db.Column(db.Text)
    reason = db.Column(db.Text)

    news = db.relationship('News', primaryjoin='ManualComment.aid == News.aid', backref='manual_comment')
    comment = db.relationship('Comment', primaryjoin='ManualComment.commentno == Comment.commentno', backref='manual_comment')


class ManualReporter(db.Model):
    __tablename__ = 'manual_reporter'

    idx = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    oid = db.Column(db.String(4), nullable=False)
    aid = db.Column(db.ForeignKey('news.aid'), nullable=False)
    commentno = db.Column(db.ForeignKey('comment.commentno'), nullable=False)
    posorneg = db.Column(db.Text)
    reason = db.Column(db.Text)

    news = db.relationship('News', primaryjoin='ManualReporter.aid == News.aid', backref='manual_reporter')
    comment = db.relationship('Comment', primaryjoin='ManualReporter.commentno == Comment.commentno', backref='manual_reporter')


class ManualNews(db.Model):
    __tablename__ = 'manual_news'

    idx = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    oid = db.Column(db.String(4), nullable=False)
    aid = db.Column(db.ForeignKey('news.aid'), nullable=False)
    commentno = db.Column(db.ForeignKey('comment.commentno'), nullable=False)
    opinion = db.Column(db.Text)
    improvement = db.Column(db.Text)
    relation = db.Column(db.Text)
    positive = db.Column(db.Text)
    negative = db.Column(db.Text)
    neutrality = db.Column(db.Text)

    news = db.relationship('News', primaryjoin='ManualNews.aid == News.aid', backref='manual_news')
    comment = db.relationship('Comment', primaryjoin='ManualNews.commentno == Comment.commentno', backref='manual_news')


