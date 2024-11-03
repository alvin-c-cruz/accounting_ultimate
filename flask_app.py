from application import create_app
import socket

app = create_app()

if __name__ == "__main__":   
    app.config["FLASKENV"] = "development"
    app.debug = True
    
    host = socket.gethostbyname(socket.gethostname())
    port = 8000
    
    web_site = f"http://{host}:{port}"
    print(f"Please type on your browser this web address: {web_site}")
    
    app.run(host="0.0.0.0", port=port)
