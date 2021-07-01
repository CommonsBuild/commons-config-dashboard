from app import app, server


if __name__ == "__main__":
    app.run_server(
        host='127.0.0.1',
        port=8085,
        debug=True,
    )