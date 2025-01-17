from flask import Flask, jsonify, make_response, request, render_template, session, flash, redirect, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import app
from backend.tabels import *
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

# checking the caching
# @app.route('/cache', methods=['GET'])
# @app.cache.cached(timeout=10)
# def cache():
#     return {'time': str(datetime.now())}

@app.route('/customer_signup', methods=['POST'])
def customer_signup():
    data = request.get_json()  # Get data from JSON payload

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    address = data.get('address')
    pincode = data.get('pincode')

    # Check if the email already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'Email already exists'}, user.to_dict()), 400

    # Create a new customer
    new_customer = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        phone=phone,
        address=address,
        pincode=pincode,
        is_active=True,
        roles=[Role.query.filter_by(name="Customer").first()]
    )
    db.session.add(new_customer)
    db.session.commit()

    return jsonify(new_customer.to_dict()), 201

# # Professsional sign up
@app.route('/professional_signup', methods=['POST'])
def professional_signup():
    data = request.get_json()  # Get data from JSON payload

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    address = data.get('address')
    pincode = data.get('pincode')

    service_id = data.get('service_id')
    doc_loc = data.get('doc_loc')

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'Email already exists'}, user.to_dict()), 400

    new_professional = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        phone=phone,
        address=address,
        pincode=pincode,
        is_active=False,
        service_id=service_id,
        doc_loc=doc_loc,
        roles=[Role.query.filter_by(name="Professional").first(), Role.query.filter_by(name="Customer").first()]
    )
    db.session.add(new_professional); db.session.commit()
    return jsonify(new_professional.to_dict()), 201


# # customer login
@app.route('/customer_login', methods=['POST'])
def customer_login():
    # Parse JSON data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Enter registered email ID only!'}), 404

    # Verify password
    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid password'}), 401

    # Generate access token for valid user
    access_token = create_access_token(identity=user.id)

    # print(email, password, access_token, sep='\n')
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'role': 'Customer',
        'roles': [r.name for r in user.roles]
    }, user.to_dict()), 200


# # professional login
@app.route('/professional_login', methods=['POST'])
def professional_login():
    # Parse JSON data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Enter registered email ID only!'}), 404

    # Verify password
    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid password'}), 401

    if 'Professional' not in [r.name for r in user.roles]:
        return jsonify({'message': 'You are not a professional'}), 401

    # Generate access token for valid user
    access_token = create_access_token(identity=user.id)

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'role': 'Professional',
        'roles': [r.name for r in user.roles]
    }, user.to_dict()), 200
  

# admin login
@app.route('/admin_login', methods=['POST'])
def admin_login():
    # Parse JSON data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Enter registered email ID only!'}), 404

    # Verify password
    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid password'}), 401

    if 'Admin' not in [r.name for r in user.roles]:
        return jsonify({'message': 'You are not an Admin'}), 401

    # Generate access token for valid user
    access_token = create_access_token(
        identity=user.id,
        additional_claims={
            'roles': [r.name for r in user.roles],
            'role': 'Admin'
        }
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'role': 'Admin',
        'roles': [r.name for r in user.roles]
    }, user.to_dict()), 200 

# all user logout
@app.route('/logout', methods=['GET'])
def logout():
    # Create response to redirect to the login page or index
    response = jsonify({'message': 'Logged out successfully'})
    response.delete_cookie('access_token')  # Delete server-side session cookie
    return response, 200