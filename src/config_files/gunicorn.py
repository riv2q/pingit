"""Gunicorn config."""
import multiprocessing
bind = "0.0.0.0:8778"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
errorlog = "-"
loglevel = "info"
accesslog = "-"
graceful_timeout = 5 * 60
