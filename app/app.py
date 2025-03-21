"""Main web application logic module"""

import logging
from os import environ, path

import bleach
import turso_mgmt as db
import url_mgmt as urls
from flask import Flask, make_response, render_template, request, send_from_directory

application = Flask(__name__)

tld = environ["TLD"]

INTERNAL_REFRESH = 120


@application.route("/", methods=["POST", "GET"])
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
            user_input = bleach.clean(str(received_request["link"]))
            error = ""
            if urls.check_url_whitespace(user_input) is False:
                error = "whitespace"
            if urls.check_url_security(user_input) is False:
                error = "insecure"
            if urls.check_url_reputation(user_input) is False:
                error = "badsite"
            if len(error) != 0:
                # If there is an error string,
                # Return homepage with error message
                resp = make_response(render_template("index.html", errormessage=error))
                return resp
            path = urls.generate_path()

            # Check for existing path
            # Generate new path if it does not already exist
            while db.check_link(path) is True:
                logging.info("Collision detected")
                path = urls.generate_path()
            if db.insert_link(path, user_input) is False:
                # 500 error returned for database failure
                resp = make_response(
                    render_template("500.html", code=500, errormessage="None")
                )
                return resp

            # Return link page with URL if successful
            resp = make_response(
                render_template(
                    "link.html", tld=tld, extension=str(path), errormessage="None"
                )
            )
            return resp

        case _:
            # Catch all to return 500 error for any unexpected cases
            resp = make_response(
                render_template("500.html", code=500, errormessage="None")
            )
            return resp


@application.route("/<arg>")
def redirect_url(arg):
    """Redirect logic for any GET requests to any URI on top of base URL"""
    # Clean arg, return 404 for unfound URL
    requested_path = bleach.clean(str(arg))

    match requested_path:
        case "robots.txt":
            # Return robots.txt response
            resp = make_response("User-Agent: *\nDisallow: /\n")
            resp.headers["Content-Type"] = "text/plain; charset=utf-8"
            return resp
        case "favicon.ico":
            # Empty response for favicon get request
            return send_from_directory(
                path.join(application.root_path, "static"),
                "favicon.ico",
                mimetype="image/vnd.microsoft.icon",
            )
        case _:
            # Get the original URL from the database, clean it, and redirect to it
            if db.check_link(requested_path[:7]) is True:
                link = db.get_link(requested_path)
                resp = make_response(
                    render_template("redirect.html", tld=tld, link=link)
                )
                return resp
            resp = make_response(render_template("404.html", tld=tld, code=404))
            return resp


@application.after_request
def add_security_headers(resp):
    """Add CSP headers to all responses generated"""
    # Following the OWASP cheat sheet
    resp.headers.update(
        {
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "0",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
            "Content-Security-Policy": "default-src 'self' img-src 'self' data:;",
            "Access-Control-Allow-Origin": f"https://{tld}",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Resource-Policy": "same-site",
            "Permissions-Policy": "geolocation=(), camera=(), microphone=(), interest-cohort=()",
            "X-CSRFToken": "Required",
            "X-DNS-Prefetch-Control": "off",
        }
    )
    return resp


# Flask main function
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8080, debug=False)
