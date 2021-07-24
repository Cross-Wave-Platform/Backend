bind = '0.0.0.0:5000'
timeout = 60

loglevel = 'debug'
errorlog = 'logs/error.log'
accesslog = 'logs/access.log'

workers = 1
worker_class = 'eventlet'
