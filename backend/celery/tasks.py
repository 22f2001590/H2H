from celery import shared_task 
import time
import flask_excel
from backend.tabels import *
from flask import current_app
import logging
import datetime
# from Backend.celery.mail_service import send_email

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

@shared_task(ignore_result=False)
def add(x, y):
    time.sleep(10)
    return x + y

@shared_task(bind=True, ignore_result=False)
def create_csv(self, model_name=None):
    try:
        if model_name == 'ServiceRequest':
            service_requests = ServiceRequest.query.all()   
            task_id = self.request.id
            service_requests_filename = f'ServiceRequest_data_{task_id}.csv'
            service_requests_columns = [column.name for column in ServiceRequest.__table__.columns]
            csv_out = flask_excel.make_response_from_query_sets(service_requests, column_names=service_requests_columns, file_type='csv')
            with open(f'backend/celery/user_downloads/{service_requests_filename}', 'wb') as file:
                file.write(csv_out.data)
            logger.info(f"CSV files for ServiceRequests models created successfully")
            return {
                "message": "CSV files for ServiceRequests created successfully",
                "filename": service_requests_filename,
            }
        elif model_name == 'Service':
            services = Service.query.all()
            task_id = self.request.id
            services_filename = f'Services_data_{task_id}.csv'
            services_columns = [column.name for column in Service.__table__.columns]
            csv_out = flask_excel.make_response_from_query_sets(services, column_names=services_columns, file_type='csv')
            with open(f'backend/celery/user_downloads/{services_filename}', 'wb') as file:
                file.write(csv_out.data)
            logger.info(f"CSV files for Services models created successfully")
            return {
                "message": "CSV files for Services created successfully",
                "filename": services_filename,
            }   
        elif model_name == 'User':
            users = User.query.all()
            task_id = self.request.id
            users_filename = f'Users_data_{task_id}.csv'
            users_columns = [column.name for column in User.__table__.columns]
            csv_out = flask_excel.make_response_from_query_sets(users, column_names=users_columns, file_type='csv')
            with open(f'backend/celery/user_downloads/{users_filename}', 'wb') as file:
                file.write(csv_out.data)
            logger.info(f"CSV files for Users models created successfully")
            return {
                "message": "CSV files for Users created successfully",
                "filename": users_filename,
            } 
    except Exception as e:
        logger.error(f"An error occurred while creating CSV files: {str(e)}")
        return {
            "message": "An error occurred while creating CSV files",
            "error": str(e)
        }

@shared_task(bind=True, ignore_result=False)
def create_csv_by_id(self, model_name=None, cid=None, pid=None):
    try:
        if model_name == 'ServiceRequest':
            service_requests = None 
            if cid:
                service_requests = ServiceRequest.query.filter_by(customer_id=cid).all() 
            elif pid:
                service_requests = ServiceRequest.query.filter_by(professional_id=pid).all() 

            task_id = self.request.id
            service_requests_filename = f'ServiceRequest_data_{task_id}.csv'
            service_requests_columns = [column.name for column in ServiceRequest.__table__.columns]
            csv_out = flask_excel.make_response_from_query_sets(service_requests, column_names=service_requests_columns, file_type='csv')
            with open(f'backend/celery/user_downloads/{service_requests_filename}', 'wb') as file:
                file.write(csv_out.data)
            logger.info(f"CSV files for ServiceRequests models created successfully")
            return {
                "message": "CSV files for ServiceRequests created successfully",
                "filename": service_requests_filename,
            }
    except Exception as e:
        logger.error(f"An error occurred while creating CSV files: {str(e)}")
        return {
            "message": "An error occurred while creating CSV files",
            "error": str(e)
        }

# @shared_task(ignore_result=True)
# def email_reminder(to, subject, content):
#     send_email(to, subject, content)
