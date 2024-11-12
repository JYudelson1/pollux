import ngrok
import dotenv
import os

dotenv.load_dotenv()
print(os.getenv("NGROK_AUTHTOKEN"))
listener = ngrok.forward("localhost:8080", authtoken_from_env=True)
print(listener.url())
