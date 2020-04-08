from application import db

class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key = True, index = True)
	date_created = db.Column(db.DateTime, default = db.func.current_timestamp(), index = True)
	date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())