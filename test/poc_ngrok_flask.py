import ngrok
import threading
import time

def start_ngrok():
    # Start the tunnel
    listener = ngrok.forward(9000, "tcp", authtoken="1vXTCJ2yaLwhWb0nFOFfm5OLAWi_2in3zT9ULBRABS7G9FeGx")
    print(f"Ingress established at {listener.url()}")

    # Keep it alive
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        listener.close()
        print("Ngrok tunnel closed.")

# Start ngrok in a background thread
ngrok_thread = threading.Thread(target=start_ngrok, daemon=True)
ngrok_thread.start()

# Your main program continues here
for i in range(10):
    print(f"Main program working... {i}")
    time.sleep(1)

# (You can join the thread if you want to wait for it to end)
# ngrok_thread.join()
