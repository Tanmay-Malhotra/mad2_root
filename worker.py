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