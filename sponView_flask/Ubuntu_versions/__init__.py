from flask import Flask
app = Flask(__name__)
app._static_folder = "/home/ubuntu/sponView_flask/static"
from sponView_flask import views
