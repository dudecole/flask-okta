from flask import Flask
from config import BaseConfig

# bootstrapping the app so all .py files can use
app = Flask(__name__)

# bootstrapping the baseconfig settings from the config.py file
app.config.from_object(BaseConfig)
