from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5050) # because apple silicon is using port 5000