from celery.schedules import crontab
from flask import current_app as app
from backend.celery.tasks import email_reminder, email_monthly_report
from backend.tabels import *

celery_app = app.extensions['celery']


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # sender.add_periodic_task(10.0, email_reminder.s('Reminder to Login', '<h1>Hello User</h1>'))

    # daily message at 9:00 pm, everyday
    sender.add_periodic_task(crontab(hour=9, minute=0), email_reminder.s('Reminder to Login', '<h1>Hello User, How can we help you tomorrow?</h1>'), name='daily reminder')

    # to demonstrate
    sender.add_periodic_task(crontab(hour=10, minute=30), email_reminder.s('Reminder to Login', '<h1>Hello User, How can we help you tomorrow?</h1>'), name='daily reminder')

    # montly message at 9:00 am, every monthstart crontab(day_of_month=1, hour=9, minute=0)
    sender.add_periodic_task(crontab(day_of_month=1, hour=9, minute=0), email_monthly_report.s(), name='monthly reminder')

    # to demonstrate
    sender.add_periodic_task(crontab(hour=11, minute=51), email_monthly_report.s(), name='monthly reminder')
