from app import create_app
from flask_cors import CORS

app = create_app()

if __name__ == "__main__":
    print("API rodando em http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
