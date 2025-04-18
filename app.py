import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world!"

if __name__ == '__main__':
    # Get the port number from the environment variable (or default to 5000)
    port = int(os.environ.get("PORT", 5000))  # Ensure it's cast to an integer
    # Run the Flask app on 0.0.0.0 with the specified port
    app.run(host="0.0.0.0", port=port, debug=False)
