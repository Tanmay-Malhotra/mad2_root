""" from celery import Celery, Task

def celery_init_app(app):
    class FlaskTask(Task):
        def _call_(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object("backend.celery_config")
    
    return celery_app """

""" from celery import Celery, Task
from flask import Flask

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):  # Fix: __call__ not _call_
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object("backend.celery_config")
    
    # Let's add this to ensure tasks can access the Flask app
    celery_app.flask_app = app
    
    return celery_app """

from celery import Celery, Task
from flask import Flask

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    
    # Configure Celery
    celery_app.config_from_object("celery_config")
    
    # Store the Flask app on the Celery app
    celery_app.flask_app = app
    
    # Update all tasks to use the Flask task base
    celery_app.Task = FlaskTask
    
    return celery_app