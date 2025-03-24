from app import create_app

app, db = create_app()

if __name__ == "__main__":
    cert_path = 'certificates/certificate.crt'
    key_path = 'certificates/private.key'

    app.run(host="0.0.0.0", port=1200, debug=True)
    
    #app.run(host="0.0.0.0", port=1200, debug=True, ssl_context=(cert_path, key_path))
