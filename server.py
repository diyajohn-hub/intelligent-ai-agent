import logging
from waitress import serve
from app import app
import sys

# Windows console encoding fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Logging setup
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    app.debug = False # Ensure production mode
    
    print("\n-------------------------------------------------------")
    print("  INTELLIGENT AI AGENT - PRODUCTION SERVER")
    print("  Powered by Waitress WSGI")
    print("-------------------------------------------------------")
    print("  Status: Online")
    print("  URL:    http://127.0.0.1:8080")
    print("-------------------------------------------------------\n")
    
    # Run server on port 8080 to distinguish from dev
    serve(app, host='127.0.0.1', port=8080, threads=8)
