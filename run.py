#!/usr/bin/env python
from sponView_flask import app
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.run(debug = True, host = "localhost", port = 8080)
