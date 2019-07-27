from waitress import serve
import os
from croma.wsgi import application
from whitenoise import WhiteNoise
import logging

if __name__ == '__main__':
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	logger = logging.getLogger('waitress')
	logger.setLevel(logging.INFO)
	my_application = serve(application, listen='*:8000')
	application = WhiteNoise(my_application, root=os.path.join(BASE_DIR, "static"))	
