"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq



APP = Flask(__name__)

FLASK_ENV='development'
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()

class Record(DB.Model):
    __tablename__ = "records"
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Date /Time {} : Value {}>'.format(self.datetime, self.value)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    DB.session.commit()
    return 'Data refreshed!'

def create_list():
	aq_list = []
	status, body = api.measurements(city='Los Angeles', parameter='pm25')
	for result in range(len(body['results'])):
		data = (body['results'][result]['date']['utc'], body['results'][result]['value'])
		aq_list.append(data)
		db_result = Record(datetime=str(data[0]), value=data[1])
		DB.session.add(db_result)
		DB.session.commit()
	return aq_list

@APP.route('/')
@APP.route('/')
def root():
    """Base view."""
    returned_list = create_list()
    list_as_str = str(returned_list)
    filtered = Record.query.filter(Record.value >= 10).all()
    return render_template('output.html', filtered=filtered)










