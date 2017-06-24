#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flaskr/")
from flaskr import app as application
application.secret_key = 'Xp9*Q-T1b'
