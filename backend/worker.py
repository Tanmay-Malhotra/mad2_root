from celery import Celery, Task

def celery_init_app(app):
    class FlaskTask(Task):
        def _call_(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object("backend.celery_config")
    
    return celery_app