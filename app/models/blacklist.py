from datetime import datetime

from ..db import db


class Blacklist(db.Model):
    ''' Class representing the blacklisted table '''

    __tablename__ = 'blacklisted'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklist_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklist_date = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
