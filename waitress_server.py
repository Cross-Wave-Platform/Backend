from waitress import serve
from app import app
# for waitress web traffic logging
from paste.translogger import TransLogger

serve(TransLogger(app), host='127.0.0.1', port=5000)