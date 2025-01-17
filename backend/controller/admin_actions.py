from flask import Flask, jsonify, make_response, request, render_template, session, flash, redirect, url_for, send_file
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt, jwt_required
from app import app
from backend.tabels import *
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from backend.celery.tasks import *
from celery.result import AsyncResult

# @app.route('/celery', methods=['GET'])
# def celery():
#     task = add.delay(10, 20)
#     return {'task_id' : task.id}

# @app.route('/get-data/<id>', methods=['GET'])
# def result(id):
#     result = AsyncResult(id)
#     if result.ready():
#         return {'result' : result.result}, 200
#     else:
#         return {'message' : 'task not ready'}, 405

@app.route('/create-csv/<model_name>', methods=['GET'])
def createCSV(model_name):
    for file in os.listdir('backend/celery/user_downloads'):
        os.remove(f'backend/celery/user_downloads/{file}')
    task = create_csv.delay(model_name=model_name)
    return {'task_id' : task.id}, 200 

@app.route('/create-csv/customer/<model_name>/<int:cid>', methods=['GET'])
def createCSVbyCID(model_name, cid):
    for file in os.listdir('backend/celery/user_downloads'):
        os.remove(f'backend/celery/user_downloads/{file}')
    task = create_csv_by_id.delay(model_name=model_name, cid=cid)
    print(task.id)
    return {'task_id' : task.id}, 200 

@app.route('/create-csv/professional/<model_name>/<int:pid>', methods=['GET'])
def createCSVbyPID(model_name, pid):
    for file in os.listdir('backend/celery/user_downloads'):
        os.remove(f'backend/celery/user_downloads/{file}')
    task = create_csv_by_id.delay(model_name=model_name, pid=pid)
    print(task.id)
    return {'task_id' : task.id}, 200 

@app.route('/get-csv/<id>', methods=['GET'])
def getCSV(id):
    result = AsyncResult(id)
    if result.ready():
        return send_file(f"backend/celery/user_downloads/{result.result['filename']}"), 200
    else:
        return {'message' : 'task not ready'}, 405           

# # functions to calculate the average rating
# def avg_rating(sr):
#     sums = [s.rating for s in sr]
#     return sum(sums) / len(sums) if sums else 0

# # Admin Dashboard
@app.route('/admin_dashboard', methods=['GET'])
# @jwt_required()
def admin_dashboard():

    live_requests = ServiceRequest.query.filter(ServiceRequest.status != 'closed').all()
    live_requests = [lr.to_dict() for lr in live_requests]
    in_active_users = [u.to_dict() for u in User.query.all() if  u.is_active==False or u.service_id==-1]

    return jsonify(live_requests, in_active_users)

# # Service management: View all the services and create a new service
@app.route('/services', methods=['GET', 'POST'])
def services():
    if request.method == 'POST':
        
        try:
            # Parse JSON data
            data = request.get_json()
            service_name = data.get('name')
            service_price = data.get('price')
            service_time = data.get('time_required')
            service_description = data.get('description')
            # Validate required fields
            if not all([service_name, service_price, service_time, service_description]):
                return jsonify({'error': 'All fields are required'}), 400

            # Create new service instance
            new_service = Service(
                name=service_name,
                price=service_price,
                time_required=service_time,
                description=service_description
            )

            # Add to database
            db.session.add(new_service)
            db.session.commit()

            return jsonify({'message': 'Service added successfully'}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    if request.method == 'GET':
        services = Service.query.all()
        services = [s.to_dict() for s in services]
        return jsonify(services)

# # Service management: search for services
# @app.route('/service_search', methods=['GET', 'POST'])
# def services_search():
#     if not verify_jwt_in_request(optional=True):
#         return redirect(url_for('index'))
#     if 'Admin' not in get_jwt()['roles']:
#         return redirect(url_for('index'))
#     if request.method == 'POST':
#         search_term = request.form['search_term']
#         ids = db.session.query(
#                     Service.id
#                 ).filter(
#                     (Service.name.like(f'%{search_term}%')) | 
#                     (Service.description.like(f'%{search_term}%'))
#                 ).all()
#         services = db.session.query(Service).filter(Service.id.in_([id for id, in ids])).all()
#         return render_template('services.html', services=services, avg_rating=avg_rating)

@app.route('/services/edit/<int:id>', methods=['PUT'])
def edit_service(id):
    # if not verify_jwt_in_request(optional=True):
    #     return jsonify({"error": "Unauthorized", "message": "JWT is missing or invalid"}), 401

    # # Get the current user from the database using the JWT identity
    # user = User.query.get(get_jwt_identity())
    # if not user:
    #     return jsonify({"error": "Unauthorized", "message": "User not found"}), 404

    # # Check if the user has the 'Admin' role
    # if 'Admin' not in get_jwt().get('roles', []):
    #     return jsonify({"error": "Forbidden", "message": "Admin role required"}), 403
    from flask_jwt_extended import verify_jwt_in_request, get_jwt

    try:
        # Verify JWT and check roles
        # if not verify_jwt_in_request(optional=True):
        #     return jsonify({'error': 'Unauthorized access'}), 401
        # if 'Admin' not in get_jwt().get('roles', []):
        #     return jsonify({'error': 'Forbidden: Insufficient permissions'}), 403

        # Fetch service by ID
        service = Service.query.get(id)
        if not service:
            return jsonify({'error': 'Service not found'}), 404

        # Parse JSON data
        data = request.get_json()
        service.name = data.get('name', service.name)
        service.price = data.get('price', service.price)
        service.time_required = data.get('time_required', service.time_required)
        service.description = data.get('description', service.description)

        # Save changes to the database
        db.session.commit()

        return jsonify({'message': 'Service updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# # Service management: edit a service
# @app.route('/services/edit/<int:id>', methods=['POST', 'GET'])
# def edit_service(id):
#     if not verify_jwt_in_request(optional=True):
#         return redirect(url_for('index'))
#     if 'Admin' not in get_jwt()['roles']:
#         return redirect(url_for('index'))
#     if request.method == 'POST':
#         service = Service.query.get(id)
#         service.name = request.form['service_name']
#         service.price = request.form['service_price']
#         service.time_required = request.form['service_time']
#         service.description = request.form['service_description']
#         db.session.add(service); db.session.commit()
#         return redirect(url_for('services'))
       
# # Service management: delete a service
# @app.route('/services/delete/<int:id>', methods=['GET', 'DELETE', 'POST'])
# def delete_service(id):
#     if not verify_jwt_in_request(optional=True):
#         return redirect(url_for('index'))
#     if 'Admin' not in get_jwt()['roles']:
#         return redirect(url_for('index'))
#     if request.method == 'POST':
#         service = Service.query.get(id)
#         if service.users:
#             flash("Service cannot be deleted becuase there are professionals associated")
#             return redirect(url_for('services'))
#         db.session.delete(service); db.session.commit()
#         return redirect(url_for('services'))
@app.route('/services/delete/<int:id>', methods=['DELETE'])
def delete_service(id):
    # from flask_jwt_extended import verify_jwt_in_request, get_jwt

    try:
        # Verify JWT and check roles
        # if not verify_jwt_in_request(optional=True):
        #     return jsonify({'error': 'Unauthorized access'}), 401
        # if 'Admin' not in get_jwt().get('roles', []):
        #     return jsonify({'error': 'Forbidden: Insufficient permissions'}), 403

        # Find the service
        service = Service.query.get(id)
        if not service:
            return jsonify({'error': 'Service not found'}), 404

        # Check if service has associated users
        if service.users:
            return jsonify({'error': 'Service cannot be deleted because professionals are associated'}), 400

        # Delete the service
        db.session.delete(service)
        db.session.commit()

        return jsonify({'message': 'Service deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# # User management: view all users
@app.route('/users', methods=['GET', 'POST'])
@app.cache.cached(timeout=10)
def users():
    # if not verify_jwt_in_request(optional=True):
    #     return jsonify({"error": "Unauthorized", "message": "JWT is missing or invalid"}), 401
    # if 'Admin' not in get_jwt()['roles']:
    #     return jsonify({"error": "Forbidden", "message": "Admin role required"}), 403

    customers = Role.query.filter_by(name="Customer").first().users
    customers = [c.to_dict() for c in customers]
    professionals = Role.query.filter_by(name="Professional").first().users
    professionals = [p.to_dict() for p in professionals]
    # return render_template('users.html', customers=customers, professionals=professionals, avg_rating=avg_rating)
    return jsonify(customers, professionals)

@app.route('/delete_user', methods=['POST'])
def admin_delete_user():
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))
    # if 'Admin' not in get_jwt()['roles']:
    #     return redirect(url_for('index'))
    data = request.get_json()
    user = User.query.get(data.get('id'))
    if 'Admin' in [r.name for r in user.roles]:
        return jsonify({"message": "Admin cannot be deleted"})
    db.session.delete(user); db.session.commit()
    return jsonify({"message": "Deleted"})

# # User management: Customer booking history view
@app.route('/customer_history', methods=['GET', 'POST'])
def customer_history():
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))
    # if not ('Admin' in get_jwt().get('roles') or id==get_jwt_identity()):
    #     flash('Only Admin and Corresponding User can view customer history')
    #     return redirect(url_for('index'))
    # user = User.query.get(id)
    # nav_user_role = get_jwt().get('role')
    data = request.get_json()
    user = User.query.get(data.get('id'))        
    service_requests = ServiceRequest.query.filter_by(customer_id=user.id).all()
    return jsonify([sr.to_dict() for sr in service_requests])
    # return render_template('customer_history.html', user=user, nav_user_role=nav_user_role, service_requests=service_requests)

# # User management: Professional working history view
@app.route('/professional_history', methods=['GET', 'POST'])
def professional_history():
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))
    # if not ('Admin' in get_jwt().get('roles') or id==get_jwt_identity()):
    #     flash('Only Admin and Corresponding Professional can view professional history')
    #     return redirect(url_for('index'))
    data = request.get_json()
    user = User.query.get(data.get('id'))
    # nav_user_role = get_jwt().get('role')
    service_requests = ServiceRequest.query.filter_by(professional_id=user.id).all()
    service_requests = [sr.to_dict() for sr in service_requests]
    return jsonify(service_requests)
    # return render_template('professional_history.html', user=user, nav_user_role=nav_user_role, service_requests=service_requests)

# User management: User profile view
@app.route('/user_profile/<int:id>', methods=['GET', 'POST'])
def user_profile(id):
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))
    # if not ('Admin' in get_jwt().get('roles') or id==get_jwt_identity()):
    #     flash('Only Admin and Corresponding User can view the profile')
    #     return redirect(url_for('index'))        
    user2 = User.query.get(id)
    # if not user2:
    #     flash('User does not exist')
    #     return redirect(url_for('index'))
    return jsonify(user2.to_dict())
    # nav_user_role = get_jwt().get('role')
    # return render_template('user_profile.html', user=user2, nav_user_role=nav_user_role)

# # User management: User flagging/unflagging to block the user to access the dashboard
@app.route('/user/flag/<int:id>', methods=['GET', 'DELETE', 'POST'])
def user_flag(id):
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))
    # if 'Admin' not in get_jwt()['roles']:
    #     return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.get(id)

        if not user:
            return jsonify({"success": False, "message": "User not found."}), 404

        if Role.query.filter_by(name='Admin').first() in user.roles:
            return jsonify({"success": False, "message": "You can't freeze Admin's Account."}), 403

        user.is_active = not user.is_active
        status = "accessible" if user.is_active else "inaccessible"
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"User's Dashboard is now {status}.",
            # "user_id": user.id,
            # "is_active": user.is_active
        }), 200


# # User management: Service professional's work experience pdf view
# @app.route('/<path:filename>')
# def download_file(filename):
#     if not verify_jwt_in_request(optional=True):
#         return redirect(url_for('index'))
#     if 'Admin' not in get_jwt()['roles']:
#         return redirect(url_for('index'))    
#     return send_from_directory('uploads', filename)

# # User management: Admin will approve newly onboarding service professionals    
@app.route('/approve', methods=['GET', 'DELETE', 'POST'])
def approve():
    # if not verify_jwt_in_request(optional=True):
    #     return redirect(url_for('index'))
    # if 'Admin' not in get_jwt()['roles']:
    #     return redirect(url_for('index'))
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.get(data.get('id'))
        if data.get('service') != '-1':
            user.is_active = True
            user.service_id = data.get('service')
        db.session.add(user); db.session.commit()
        return jsonify({'message': 'Approved'})

@app.route('/image', methods=['GET'])
def serve_image():
    try:
        # Assuming images are stored in a folder named "static/images"
        file_path = f"frontend/src/assets/service_requests_bar_graph.png"
        return send_file(file_path, mimetype='image/png')
    except FileNotFoundError:
        return "Image not found!", 404

# # app summary to see the trending services in the portal
@app.route('/app_summary', methods=['GET'])
def app_summary():
    service_requests = ServiceRequest.query.all()
    
    service_counts = {s.name: 0 for s in Service.query.all()}
    for request in service_requests:
        service_counts[request.service.name] += 1
    service_counts = dict(sorted(service_counts.items(), key=lambda item: item[1])   )
    folder_path  = 'frontend/src/assets'

    fig_bar = plt.figure()
    plt.bar(list(service_counts.keys()), list(service_counts.values()))          
    plt.xticks(rotation=90)
    plt.yticks(range(0, max(service_counts.values()) + 1))
    plt.xlabel('Service')
    plt.ylabel('Frequency of Service Requested')
    plt.tight_layout()
    file_path = os.path.join(folder_path,'service_requests_bar_graph.png')
    plt.savefig(file_path)
    plt.close()
    plt.close(fig_bar)
    service_requests = [sr.to_dict() for sr in service_requests]
    return jsonify(service_requests)

