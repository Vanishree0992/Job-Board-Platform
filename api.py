from flask import Flask, jsonify
from extensions import db
from models import Job

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/api/jobs')
def api_list_jobs():
    jobs = Job.query.all()
    data = [{'id': j.id, 'title': j.title, 'description': j.description, 'posted': j.posted_on.isoformat()} for j in jobs]
    return jsonify(data)
