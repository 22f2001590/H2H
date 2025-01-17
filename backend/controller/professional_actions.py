from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
from app import app
from backend.tabels import *
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt

# # service professional dashboard
@app.route('/professional_dashboard', methods=['GET', 'POST'])
def professional_dashboard():
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))
    # user = User.query.get(get_jwt_identity())
    data = request.get_json()
    user = User.query.get(data.get('id'))
    # print(user)
    # if not user:
    #     return redirect(url_for('logout'))
    # if 'Professional' != get_jwt().get('role'):
    #     return redirect(url_for('index'))
    requested_services = ServiceRequest.query.filter_by(
        status='requested', 
        service_id=user.service.id if user.service else None
    ).all()
    requested_services = [sr.to_dict() for sr in requested_services]

    accepted_services = ServiceRequest.query.filter(
        ServiceRequest.status.in_(['accepted', 'paid']),
        ServiceRequest.professional_id == user.id
    ).all()
    accepted_services = [sr.to_dict() for sr in accepted_services]
    return jsonify(requested_services, accepted_services)

# # accept the service request created by a customer
@app.route('/accept_request', methods=['POST'])
def accept_request():
    data = request.get_json()
    sr = ServiceRequest.query.filter_by(id=data["service_request_id"]).first()
    sr.status = 'accepted'
    sr.professional_id = data["professional_id"]

    db.session.add(sr); db.session.commit()
    return jsonify(sr.to_dict())


@app.route('/reject_request', methods=['POST'])
def reject_request():
    data = request.get_json()
    sr = ServiceRequest.query.filter_by(id=data["service_request_id"]).first()
    sr.status = 'requested'
    sr.professional_id = None

    db.session.add(sr); db.session.commit()
    return jsonify(sr.to_dict())    


@app.route('/close_request', methods=['POST'])
def close_request():
    if request.method == 'POST':
        data = request.get_json()
        sr = ServiceRequest.query.filter_by(id=data.get('service_request_id')).first()
        sr.status = 'closed'
        sr.professional_feedback = data.get('feedback')
        db.session.add(sr); db.session.commit()
        return jsonify(sr.to_dict())

