import os
import time
import threading
from dotenv import load_dotenv
import ngrok

from functions.state import global_holder

load_dotenv()


def start_ngrok(port: int = 25565, protocol: str = "tcp"):

    # Start the tunnel
    global_holder.active_listener = ngrok.forward(port, protocol, authtoken=os.getenv("NGROK_TOKEN"))
    print(f"Ingress established at {global_holder.active_listener.url()}")

    # Keep it alive
    try:
        while not global_holder.stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_ngrok()


def stop_ngrok():
    if global_holder.active_listener:
        global_holder.active_listener.close()
        global_holder.active_listener = None
        global_holder.stop_event.set()
        print("Ngrok tunnel closed.")
        return True
    return False

# Example usage:
# Start ngrok in a background thread
# ngrok_thread = threading.Thread(target=start_ngrok, daemon=True)
# ngrok_thread.start()
#
# To stop it later:
# stop_ngrok()