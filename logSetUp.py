from ursina import *
import functools
import logging
import logging.config
import os
import sys
import inspect
import traceback
#from ursina import Entity



class LogSystem():
    def __init__(Self):
        Self.log = logging.getLogger("mainLog")
        Self.logPath = "./Logs/TestLogs/testLog.log"
        Self.num = 0
        Self.verifyLogPath()
        Self.menu = None
        Self.loggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(levelname)s: %(message)s"},
            "detailed": {"format": "[%(levelname)s]|%(asctime)s|%(module)s|%(lineno)d|%(message)s"}
            },
        "handlers": {
            "stdout":{
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
                },
            "file":{
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": f"{Self.logPath}",
                "maxBytes": 100000,
                "backupCount": 3
                },

            },
        "loggers":{
            "root": {"level": "DEBUG", "handlers": {"stdout", "file"}}
            },
        }
        logging.config.dictConfig(config=Self.loggingConfig)

    def exitGame(Self):
        Self.menu.clearMenu()
        Self.menu.singlePlay()
        
    def handleException(Self,ex):
        print("HANDLING EXCEPTION")
        Self.menu.menuItems.append(Entity(parent=camera.ui, model='quad', scale=(0.5, 0.4), color=color.gray))#bg
        Self.menu.menuItems.append(Text(parent=camera.ui, text="Runtime Exception", position=(0, 0.15), origin=(0, 0)))#title
        Self.menu.menuItems.append(Text(parent=camera.ui, text=f"An error has occured \n '{ex}' \n you may reset from the last known board state, or otherwise exit the game", position=(0, 0), origin=(0, 0)))#content
        Self.menu.menuItems.append(Button(parent = camera.ui,model='quad', scale=(0.04, 0.05), color=color.red,position=(-0.1, -0.15), text = "reset", on_click=Self.exitGame))
        Self.menu.menuItems.append(Button(parent = camera.ui,model='quad', scale=(0.04, 0.05), color=color.red,position=(0.1, -0.15), text = "exit", on_click=Self.exitGame))
        
    def verifyLogPath(Self): #Could be changed to set log path in later iterations
        curtName = ""
        curtPath = ""
        for index, char in enumerate(Self.logPath):
            curtPath += char
            if char == "/":
                if not os.path.exists(curtPath): os.mkdir(curtPath)
                continue
            curtName += char


    def logFunctionCall(Self, func):#This was generated with chatgpt
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logged = False
            callerFrame = inspect.stack()[1]
            lineNum = callerFrame.lineno
            try:
                result = func(*args, **kwargs)
            except Exception as ex:
                Self.log.debug(f"{lineNum}|Function Call: '{func.__name__}' with args {args} and kwargs {kwargs} | Result !!ERROR!!")# | returned {result}")
                logged = True
                Self.log.error(f"\n --- \n {traceback.format_exc()} ---")
                result = ex
                Self.handleException(ex)
            if not logged: Self.log.debug(f"{lineNum}|Function Call: '{func.__name__}' with args {args} and kwargs {kwargs} | Result: {result}")
            return result
        return wrapper

def apply_decorator_to_all_functions(module):
    # Check if the input is a module, and use module.__dict__ if so
    if hasattr(module, '__dict__'):
        # Iterate over the items in the module's dictionary
        for name, obj in module.__dict__.items():
            if isinstance(obj, type):  # If it's a class, apply decorator to its methods
                for method_name, method_obj in obj.__dict__.items():
                    if callable(method_obj) and not method_name.startswith("_"):  # Skip private methods
                        setattr(obj, method_name, log_function_call(method_obj))
            elif callable(obj) and not name.startswith("_"):  # Apply decorator to functions
                setattr(module, name, log_function_call(obj))
    else:
        raise TypeError("The provided module is not valid.")
        

#@log_function_call
def changeVar():
    global persistentTestVar
    persistentTestVar -=1
    return(persistentTestVar)

#@log_function_call
def randomFunc():
    num = 1/0
    return num

#@log_function_call      
class testClass:
    def __init__(Self):
        Self.val1 = 0
        Self.val2 = 1
    #@log_function_call
    def print(Self):
        print(Self.val1 + Self.val2)

ls = LogSystem()
log = ls.log
logFunctionCall = ls.logFunctionCall
