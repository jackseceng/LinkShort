"""Modules: Database handler, timestamp library, flask dependencies and local modules"""

from flask import Flask, render_template, request, redirect, make_response, logging

import logging

import url_mgmt as urls

import db_mgmt as db

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def input_url():
    """Main page process"""
    match request.method:
        case 'GET':
            logging.warning("Home GET request")
            resp = make_response(render_template('index.html')) # Return index page for GET method
            return resp
        case 'POST':
            logging.warning("Home POST request")
            user_input = dict(request.form.to_dict())
            ui_log = (f"User input: {user_input}")
            logging.warning(ui_log)
            # Retrieve user input from html form on index page
            error = ""
            if urls.check_url(user_input['URL'], 1) is False:  # Check if input is a URL
                error = 'URL has whitespace'
                logging.warning(error)
                # Error for invalid input
            if urls.check_url(user_input['URL'], 2) is False:  # Check if URL uses https
                error = 'HTTPS links only'
                logging.warning(error)
                # Error for non-https link
            if len(error) != 0:
                error = (f"URL check failed, URL: {user_input['URL']} | Failure error: {error}")
                logging.warning(error)
                resp = make_response(render_template('index.html', error_reason=error))
                return resp
            logging.warning("Generating path initial value")
            path = urls.generate_path(str(user_input))
            logging.warning("Path generated")
            logging.warning(path)
            # Generate path for shortened URL
            logging.warning("Initial check for collisions")
            check = db.check_link(path)
            logging.warning(check)
            while db.check_link(path) is True:
                logging.warning("Collision detected")
                # Check for collisions with existing paths
                path = urls.generate_path(str(user_input))
                # Regenrate path value until there is no longer a collision
            if db.insert_link(path, user_input['URL']) is False:
            # Insert new path and matching original URL into DB
                resp = make_response(render_template('500.html', code=500))
                return resp
                # If failure, render 500 error page to front end
            output = (f"URL generated for: {user_input['URL']} | URL subdirectory: {path}")
            logging.warning(output)
            # Print new URL and path to console
            resp = make_response(render_template('index.html',
                                shorten_message="Shortened URL",
                                extension=str(path)))
            return resp
            # Render link page with URL
        case _:
            logging.warning("Catch all home 500 error")
            resp = make_response(render_template('500.html', code=500))
            return resp
            # Catch all to handle unexpected errors, render 500 error page to front end


@app.route('/<arg>', methods=['GET'])  # Handle any GET requests for paths
def redirect_url(arg):
    """Redirect logic for any GET requests to any URI on top of base URL"""
    logging.warning("Redirect GET request")
    path = str(arg)
    logging.warning(path)
    if urls.check_url(path, 3) is False: # Run check to see if path format is valid
        logging.warning("Invalid path")
        resp = make_response(render_template('404.html', code=404))
        return resp
        # Return 404 not found if URL is invalid
    # Execute query to obtain original URL that matches provided path
    link = db.get_link(arg)
    if link is not False: # Fetch the original URL
        output = (f"Redirecting to original URL {link}")
        logging.warning(output)
        resp = make_response(redirect(link, code=302))
        return resp
        # Return 302 response to client, with original URL as redirect
    logging.warning("Path not found")
    resp = make_response(render_template('404.html', code=404))
    return resp
    # Catch all 404 error handler for unknown paths


@app.after_request
def add_security_headers(resp):
    """Add any headers to all responses generated"""
    resp.headers['Content-Security-Policy']='default-src \'self\''
    return resp

# Flask app entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
