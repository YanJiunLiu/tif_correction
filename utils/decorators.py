from . import WORKFLOWS, logger
from functools import wraps
from .workflow import Base
import importlib

def load_system(workflow):
    return workflow(logger=logger)

def decorator_app(app, workflow):
    setattr(app, 'workflow', load_system(workflow=workflow))
    return app

def workflow(function_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 嘗試從 args 或 kwargs 找出 Request 物件
            app =  kwargs['app']
            cls = Base
            if workflow := WORKFLOWS.get(function_name):
                if module_path := workflow.get('path'):
                    if class_name := workflow.get('name'):
                        module = importlib.import_module(module_path)
                        cls = getattr(module, class_name)     
            decorator_app(app, cls)

            return func(*args, **kwargs)
        return wrapper
    return decorator