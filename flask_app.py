from application import create_app

# Create the app by calling create_app and passing the environment configuration
app = create_app('development')

if __name__ == '__main__':
    # Run the app with the Flask built-in development server
    # The host='0.0.0.0' makes the app externally visible (if needed for testing in networks)
    app.run(host='0.0.0.0', port=5000, debug=True)
