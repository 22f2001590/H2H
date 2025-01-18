from flask import Flask, jsonify, make_response, request, render_template, session, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, get_jwt, verify_jwt_in_request, jwt_required
from app import app
from backend.tabels import *
from sqlalchemy import func
from backend.celery.mail_service import send_email

# # customer dashboard
@app.route('/live_requests', methods=['POST'])
# @jwt_required()
def live_requests():
    data = request.get_json()  # Get the JSON data from the request body
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    # user = User.query.get(user_id)
    # Process the live requests based on the user_id
    live_requests = [lr.to_dict() for lr in ServiceRequest.query.all() if lr.customer_id == user_id and (lr.status=='accepted' or lr.status == 'requested')]
    # (For demonstration, just return the received user_id)
    return jsonify(live_requests)
    # return jsonify({"message": f"Live requests for user {user_id}"})
# @app.route('/customer_dashboard', methods=['GET', 'POST'])
# def customer_dashboard():
#     if not verify_jwt_in_request(optional=True):
#         return redirect(url_for('index'))
#     user = User.query.get(get_jwt_identity())
#     if not user:
#         return redirect(url_for('logout'))
#     services = Service.query.all()
#     live_requests = [lr for lr in ServiceRequest.query.all() if lr.customer_id == user.id and (lr.status=='accepted' or lr.status == 'requested')]
#     return render_template('customer_dashboard.html', user=user, services=services, live_requests=live_requests, 
#     current_date=datetime.now().strftime('%Y-%m-%d'), nav_user_role='Customer')

# # search for a service by a customer
# @app.route('/customer_search', methods=['GET', 'POST'])
# def customer_search():
#     if not verify_jwt_in_request(optional=True):
#         return redirect(url_for('index'))
#     user = User.query.get(get_jwt_identity())
#     if request.method == 'POST':
#         search_term = request.form['search_term']
#         ids = db.session.query(
#                     Service.id
#                 ).join(Service.users).filter(
#                     (Service.name.like(f'%{search_term}%')) | 
#                     (Service.description.like(f'%{search_term}%')) |
#                     (User.address.like(f'%{search_term}%')) |
#                     (User.pincode.like(f'%{search_term}%'))
#                 ).all()

#         services = db.session.query(Service).filter(Service.id.in_([id for id, in ids])).all()
#         live_requests = [lr for lr in ServiceRequest.query.all() if lr.customer_id == user.id and lr.status != 'closed']
#         return render_template('customer_search.html', user=user, services=services, live_requests=live_requests, 
#         current_date=datetime.now().strftime('%Y-%m-%d'), nav_user_role='Customer')

# # book a service request by a customer

@app.route('/book_now', methods=['POST'])
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
    
# @app.route('/book_now', methods=['GET', 'POST'])
# def book_now():
#     if request.method == 'POST':
#         if not verify_jwt_in_request(optional=True):
#             return redirect(url_for('index'))
#         if not 'Customer' in get_jwt().get('role'):
#             return "Please login as customer"

#         service_id = request.form['service_id']
#         customer_id = get_jwt_identity()
#         needed_at = datetime.strptime(f"{request.form['date']} {request.form['time']}", '%Y-%m-%d %H:%M')
#         requirement_message = request.form['requirement_message']
#         if needed_at < datetime.now():
#             flash('You cannot book a service in the past.', 'error')
#             print('You cannot book a service in the past')
#             return redirect(url_for('customer_dashboard'))
#         new_service_request = ServiceRequest(
#             service_id = service_id,
#             customer_id = customer_id,
#             professional_id = None, 
#             needed_at = needed_at,
#             requirement_message = requirement_message,
#             status = 'requested',
#             customer_feedback = None,
#             rating = 0
#         )
#         db.session.add(new_service_request); db.session.commit()
#         return redirect(url_for('customer_dashboard'))

# # edit a service request by a customer
@app.route('/edit_request/<int:id>', methods=['GET', 'POST'])
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

# @app.route('/cancel_request/<int:id>', methods=['POST', 'GET'])
# def cancel_request(id):
#     if request.method == 'GET':
#         service_request = ServiceRequest.query.get(id)
#         db.session.delete(service_request); db.session.commit()
#         return redirect(url_for('customer_dashboard'))

# # pay the fees for a service request by a customer
@app.route('/pay_request', methods=['POST'])
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

# # delete a user account by a user
# @app.route('/user/delete/<int:id>', methods=['GET', 'POST'])
# def delete_user(id):
#     if not verify_jwt_in_request(optional=True):
#         return redirect(url_for('index'))
#     if request.method == 'POST':
#         user = User.query.get(id)
#         if 'Admin' in [role.name for role in user.roles]:
#             flash("You cannot delete an admin user")
#             return redirect(url_for('user_profile', id=user.id))
#         session.clear()
#         # if user.doc_loc and os.path.exists(user.doc_loc): 
#         #     os.remove(user.doc_loc)
#         db.session.delete(user); db.session.commit()
#         flash("Account Deleted, We are sad to see you leaving our site")
#         return redirect(url_for('logout')) 
