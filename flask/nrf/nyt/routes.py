from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, Response
import json
import pandas
import psycopg2 as pg2

from nrf.models.models import Comment, Manual, ManualNews, News
from nrf import db
from sqlalchemy import and_
from sqlalchemy import and_

nyt = Blueprint('nyt', __name__)


# nyt module 보안상 생략