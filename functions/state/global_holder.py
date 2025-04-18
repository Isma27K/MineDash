# globals.py
import threading

server_process = None
server_log = {}

server_ip = ""

active_listener = None
stop_event = threading.Event()