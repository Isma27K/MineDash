# import ngrok python sdk
import ngrok
import time

# Establish connectivity
listener = ngrok.forward(9000, "tcp",  authtoken="1vXTCJ2yaLwhWb0nFOFfm5OLAWi_2in3zT9ULBRABS7G9FeGx")

# Output ngrok url to console
print(f"Ingress established at {listener.url()}")

# Keep the listener alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing listener")