"""Main web application logic module"""
import logging
import bleach
from flask import Flask, render_template, request, make_response
import url_mgmt as urls
import redis_mgmt as db

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def input_url():
    """Main page process"""
    match request.method:
        case "GET":
            # Return homepage
            resp = make_response(render_template("index.html"))
            return resp

        case "POST":
            # Retrieve user input from html form on index page
            # Perform syntax checks
            received_request = dict(request.form.to_dict())
            user_input = bleach.clean(str(received_request["URL"]))
            error = ""
            if urls.check_url_whitespace(user_input) is False:
                error = "URL has whitespace"
            if urls.check_url_security(user_input) is False:
                error = "HTTPS links only"
            if len(error) != 0:
                # If there is an error string,
                # Return homepage with error message
                resp = make_response(render_template("index.html", error_reason=error))
                return resp
            path = urls.generate_path(str(user_input))

            # Check for existing path
            # Generate new path if it does not already exist
            while db.check_link(path) is True:
                logging.warning("Collision detected")
                path = urls.generate_path(str(user_input))
            if db.insert_link(path, user_input) is False:
                # 500 error returned for database failure
                resp = make_response(render_template("500.html", code=500))
                return resp

            # Return link page with URL if successful
            resp = make_response(render_template("link.html", extension=str(path)))
            return resp

        case _:
            # Catch all to return 500 error for any unexpected cases
            resp = make_response(render_template("500.html", code=500))
            return resp


@app.route("/<arg>", methods=["GET"])
def redirect_url(arg):
    """Redirect logic for any GET requests to any URI on top of base URL"""

    # Clean arg, return 404 for inncorrect extension length
    path = bleach.clean(str(arg[:7]))

    # Get the original URL from the database, clean it, and redirect to it
    link = db.get_link(path)
    if link is not False:
        resp = make_response(render_template("redirect.html", link=link))
        return resp
    resp = make_response(render_template("404.html", code=404))
    return resp


@app.after_request
def add_security_headers(resp):
    """Add CSP headers to all responses generated"""
    resp.headers["Content-Security-Policy"] = "default-src 'self'"
    return resp


# # Flask app DEV main function
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
