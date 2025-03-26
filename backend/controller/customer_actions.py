from flask import Flask, jsonify, make_response, request, render_template, session, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, get_jwt, verify_jwt_in_request, jwt_required
from app import app
from backend.tabels import *
from sqlalchemy import func
from backend.celery.mail_service import send_email

# # customer dashboard
@app.route('/live_requests', methods=['POST'])
@jwt_required()
def live_requests():
    data = request.get_json()  
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    live_requests = [lr.to_dict() for lr in ServiceRequest.query.all() if lr.customer_id == user_id and (lr.status=='accepted' or lr.status == 'requested')]
    return jsonify(live_requests)
    

# # book a service request by a customer
@app.route('/book_now', methods=['POST'])
@jwt_required()
def book_now():
    # Verify JWT or user authentication (optional, based on your setup)
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))

    data = request.get_json()  # Get the JSON data sent from the frontend

    # Check if required data is present
    if not all(key in data for key in ['service_id', 'customer_id', 'date', 'time', 'requirement_message']):
        return jsonify({"error": "Missing required fields"}), 400

    service_id = data['service_id']
    customer_id = data['customer_id']
    date_str = data['date']
    time_str = data['time']
    requirement_message = data['requirement_message']

    # Combine date and time and convert to datetime
    try:
        needed_at = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({"error": "Invalid date or time format"}), 400

    if needed_at < datetime.now():
        return jsonify({"error": "You cannot book a service in the past"}), 400

    # Create the new service request in the database
    new_service_request = ServiceRequest(
        service_id=service_id,
        customer_id=customer_id,
        professional_id=None,
        needed_at=needed_at,
        requirement_message=requirement_message,
        status='requested',
        customer_feedback=None,
        rating=0
    )

    db.session.add(new_service_request)
    db.session.commit()

    for professional in Service.query.get(service_id).users:
        send_email(f'{professional.email}', f'Got {professional.service.name} Request', f'<h1>Login and Accept</h1><p>Message: {requirement_message}</p>')

    # Return a success response
    return jsonify({"message": "Service booked successfully", "service_request_id": new_service_request.id}), 200


# # edit a service request by a customer
@app.route('/edit_request/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def edit_request(id):
    if request.method == 'POST':
        service_request = ServiceRequest.query.get(id)
        data = request.get_json()  # Get the JSON data sent from the frontend

    # Check if required data is present
        if not all(key in data for key in ['service_id', 'customer_id', 'date', 'time', 'requirement_message']):
            return jsonify({"error": "Missing required fields"}), 400

        service_id = data['service_id']
        customer_id = data['customer_id']
        date_str = data['date']
        time_str = data['time']
        requirement_message = data['requirement_message']

        # Combine date and time and convert to datetime
        try:
            needed_at = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        except ValueError:
            return jsonify({"error": "Invalid date or time format"}), 400

        if needed_at < datetime.now():
            return jsonify({"error": "You cannot book a service in the past"}), 400
        service_request.service_id = service_id
        service_request.customer_id = customer_id
        service_request.needed_at = needed_at
        service_request.requirement_message = requirement_message

        db.session.add(service_request); db.session.commit()
        return jsonify({"message": "Service edited successfully"}), 200
# # delete a service request by a customer
@app.route('/cancel_request/<int:id>', methods=['DELETE'])
@jwt_required()
def cancel_request(id):
    # Find the request by ID
    request = ServiceRequest.query.get(id)
    
    if request:
        # Delete the request (or update its status)
        db.session.delete(request)
        db.session.commit()
        return jsonify({"message": "Request cancelled successfully."}), 200
    else:
        return jsonify({"message": "Request not found."}), 404


# # pay the fees for a service request by a customer
@app.route('/pay_request', methods=['POST'])
@jwt_required()
def pay_request():
    if request.method == 'POST':
        data = request.get_json()
        service_request = ServiceRequest.query.get(data.get('service_request_id'))
        service_request.status = 'paid'
        service_request.customer_feedback = data.get('feedback')
        service_request.rating = data.get('rating')
        db.session.add(service_request); db.session.commit()
        return jsonify(service_request.to_dict())
    # return redirect(url_for('customer_dashboard'))

# # edit a user profile by a user
@app.route('/user/edit', methods=['POST'])
@jwt_required()
def edit_user():
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.get(data.get('user_id'))
        # user.phone = request.form['user_phone']
        user.phone = data.get('phone')
        # user.address = request.form['user_address']
        user.address = data.get('address')
        # user.pincode = request.form['user_pincode']
        user.pincode = data.get('pincode')
        db.session.add(user); db.session.commit()
        return jsonify(user.to_dict())
        # return redirect(url_for('user_profile', id=user.id))           
