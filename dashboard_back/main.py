import os
import time

import datetime as dt

import common_utils.date_utils
import pandas as pd
import structlog
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from common_utils import db, date_utils

import utils



app = Flask(__name__,
            static_folder="../dashboard-front/dist/",
            template_folder="../dashboard-front/dist")

cors = CORS(app, resources={r"/api/v1/status": {"origins": "http://localhost:port"}})

log = structlog.getLogger()

IS_LOCAL = os.environ.get('CHARIOTS_LOCAL') == 'true'


@app.route('/')
@cross_origin(origin='localhost', headers=['*'])
def index():
    return render_template("index.html")


@app.route('/api/v1/statuses', methods=['POST'])
@cross_origin(origin='localhost', headers=['*'])
def get_statuses():

    fake_today = date_utils.get_fake_today()
    max_records = request.json.get('max_records', 1000)
    session = utils.get_session()
    selected = session.query(
        db.HardDriveStatus.date,
        db.HardDriveStatus.model,
        db.HardDriveStatus.serial_number,
        db.HardDriveStatus.failure,
        db.HardDriveStatus.capacity_bytes,
        db.HardDriveStatus.prediction
    ).filter(
        db.HardDriveStatus.date.between(fake_today - dt.timedelta(days=1), fake_today)
    ).order_by(
        db.HardDriveStatus.date.desc()
    ).limit(max_records)
    res = jsonify([
        {
            "date": record[0].strftime("%Y-%m-%d %H:%M:%S"),
            "model": record[1],
            "serial_number": record[2],
            "failure": record[3],
            "capacity_bytes": record[4],
            "failure_probability": record[5]
        } for record in selected

    ])
    if IS_LOCAL:
        time.sleep(1)
    return res


@app.route('/api/v1/serial_statuses', methods=['POST'])
@cross_origin(origin='localhost', headers=['*'])
def get_statuses_for_serial():
    serial_number = request.json.get('serial_number')
    if not serial_number:
        return jsonify([])
    session = utils.get_session()
    selected = session.query(
        db.HardDriveStatus.date,
        db.HardDriveStatus.model,
        db.HardDriveStatus.serial_number,
        db.HardDriveStatus.failure,
        db.HardDriveStatus.capacity_bytes
    ).filter(
        db.HardDriveStatus.serial_number == serial_number
    ).order_by(
        db.HardDriveStatus.date.desc()
    )
    res = jsonify([
        {
            "date": record[0].strftime("%Y-%m-%d %H:%M:%S"),
            "model": record[1],
            "serial_number": record[2],
            "failure": record[3],
            "capacity_bytes": record[4]
        } for record in selected

    ])
    if IS_LOCAL:
        time.sleep(1)
    return res


@app.route('/api/v1/failures_per_day', methods=['POST'])
@cross_origin(origin='localhost', headers=['*'])
def get_failures_per_day():
    fake_today = date_utils.get_fake_today()
    n_days = request.json.get('n_days', 14)
    filters = request.json.get('filters', {
        'selectedModels': [],
        'selectFailures': True,
        'selectWarnings': True,
        'selectNominal': True,
    })
    session = utils.get_session()
    selected = session.query(
        db.HardDriveStatus.date,
        db.HardDriveStatus.failure,
        db.HardDriveStatus.model
    ).filter(db.HardDriveStatus.date.between(fake_today - dt.timedelta(days=n_days), fake_today))
    failures = list(selected.filter(db.HardDriveStatus.failure == 1))
    failures_dict = pd.DataFrame(
        failures, columns=['date_time', 'model', 'failure',]
    ).groupby(pd.Grouper(key='date_time', freq='D'))['failure'].count().to_dict()

    # if lenn(filters['selectedModels']) == 0:
    #     return jsonify({
    #         key.strftime("%Y-%m-%d"): value
    #         for key, value in
    #         failures_dict.items()
    #     })
    filtered_failures = failures
    if not filters['selectFailures']:
        filtered_failures = [record for record in filtered_failures if record.failure == 0]

    if not filters['selectNominal']:
        filtered_failures = [record for record in filtered_failures if record.failure == 1]

    if len(filters['selectedModels']) > 0:
        filtered_failures = [record for record in filtered_failures if record.model in filters['selectedModels']]

    if not filtered_failures:
        return jsonify({key.strftime("%Y-%m-%d"): 0 for key in failures_dict})
    filtered_failures_dict = pd.DataFrame(
        filtered_failures, columns=['date_time', 'model', 'failure',]
    ).groupby(pd.Grouper(key='date_time', freq='D'))['failure'].count().to_dict()
    if IS_LOCAL:
        time.sleep(5)
    return jsonify({
        key.strftime("%Y-%m-%d"): filtered_failures_dict.get(key, 0) for key in failures_dict
    })


@app.route('/api/v1/notifications', methods=['POST'])
@cross_origin(origin='localhost', headers=['*'])
def get_notifications():
    fake_today = date_utils.get_fake_today()
    n_days = request.json.get('n_days', 30)
    session = utils.get_session()
    selected = session.query(
        db.HardDriveStatus.date,
        db.HardDriveStatus.model,
        db.HardDriveStatus.serial_number,
        db.HardDriveStatus.failure,
        db.HardDriveStatus.capacity_bytes
    ).filter(db.HardDriveStatus.date.between(fake_today - dt.timedelta(days=n_days), fake_today))
    if IS_LOCAL:
        time.sleep(1)
    return jsonify([
        {
            "date": record[0].strftime("%Y-%m-%d %H:%M:%S"),
            "model": record[1],
            "serial_number": record[2],
            "failure": record[3],
            "capacity_bytes": record[4]
        } for record in selected.filter(db.HardDriveStatus.failure == 1)

    ])


@app.route('/api/v1/metrics', methods=['POST'])
@cross_origin(origin='localhost', headers=['*'])
def get_metrics():
    live = request.json['is_live']
    is_test = request.json.get('is_test', True)
    print(is_test)
    session = utils.get_session()
    query = session.query(
       db.ModelPerformance
    ).filter(
        db.ModelPerformance.is_live_perf == live
    ).filter(
        db.ModelPerformance.is_training_performance != is_test
    ).order_by(
        db.ModelPerformance.date.desc()
    )
    performances = list(query)
    latest_performance = performances[0]
    latest_performance = {
        'date': latest_performance.date,
        'confusion_matrix': latest_performance.confusion_matrix,
        'recalls': latest_performance.recall,
        'precisions': latest_performance.precision,
        'f1_scores': latest_performance.f1_score,
        'roc_auc': latest_performance.roc_auc
    }
    thresholds = list(latest_performance['confusion_matrix'].keys())
    history = [
        {
            'date': perf.date,
            'recalls': perf.recall,
            'precisions': perf.precision,
            'f1_scores': perf.f1_score,
            'roc_auc': perf.roc_auc
        } for perf in performances
    ]
    time.sleep(1)
    return jsonify({
        'latest': latest_performance,
        'history': history,
        'thresholds': thresholds
    })


if __name__ == '__main__':

    app.run(debug=True)




