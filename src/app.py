"""Modules: Database handler, timestamp library, flask dependencies and local modules"""
import sqlite3

from datetime import datetime

from flask import Flask, render_template, request, redirect, make_response

import url_mgmt as urls

app = Flask(__name__)

connection = sqlite3.connect('links.sqlite', check_same_thread=False)

cursor = connection.cursor()
# Set up SQLite connection and cursor


INSERT_QUERY = """INSERT INTO urls (urn,link,doc) VALUES( ?,?,? );"""  # Insert new URL entry

PATH_QUERY = """SELECT link FROM urls where urn = ?;"""  # Select original link from DB

COLLISION_QUERY = """SELECT EXISTS(SELECT 1 FROM urls WHERE urn = ?);"""
# Select any urn's that match query

URL_QUERY = """SELECT urn FROM urls where link = ?;"""
# Select URN from DB row with link that matches query


# SQLite queries


@app.route('/', methods=['POST', 'GET'])
def input_url():
    """Main page process"""
    match request.method:
        case 'GET':
            resp = make_response(render_template('index.html')) # Return index page for GEt method
            return resp
        case 'POST':
            user_input = dict(request.form.to_dict())
            # Retrieve user input from html form on index page
            error = ""
            if urls.check_url(user_input['URL'], 1) is False:  # Check if input is a URL
                error = 'URL has whitespace'
                # Error for invalid input
            if urls.check_url(user_input['URL'], 2) is False:  # Check if URL uses https
                error = 'HTTPS links only'
                # Error for non-https link
            if len(error) != 0:
                print(f"URL check failed, URL: {user_input['URL']} | Failure error: {error}")
                resp = make_response(render_template('index.html', error_reason=error))
                return resp
            path = urls.generate_path(str(user_input))
            # Generate URN for shortened URL
            while cursor.execute(COLLISION_QUERY, (path,)) == 1:
                # Check for collisions with existing URNs
                path += 1  # Increment path value until there is no longer a collision
            try:
                cursor.execute(INSERT_QUERY, (path, user_input['URL'], str(datetime.now())))
                # Insert new URN and matching original URL into DB
                connection.commit()  # Commit the new entry
            except sqlite3.IntegrityError:  # SQLite error handling
                cursor.execute(URL_QUERY, [user_input['URL']])
                link = str(cursor.fetchone()[0])
                # Obtain existing URN and URL
                resp = make_response(render_template('index.html',
                                       error_reason="Already shortened",
                                       existing_url="http://127.0.0.1/" + link))
                return resp
                # Return existing URL and URN
            except sqlite3.Error as error_msg:  # Catch all for any other SQLite error
                print(f'SQLite error: {" ".join(error_msg.args)}')
                print(f"SQLite error. Input: {user_input['URL']} | Generated URN: {path}")
                # Print error information to console
                resp = make_response(render_template('500.html', code=500))
                return resp
                # Return 500 code to front end, render error page
            print(f"URL generated for: {user_input['URL']} | URL subdirectory: {path}")
            # Print new URL and URN to console
            resp = make_response(render_template('index.html',
                                shorten_message="Shortened URL",
                                extension="http://127.0.0.1/" + str(path)))
            return resp
            # Render link page with URL
        case _:
            resp = make_response(render_template('500.html', code=500))
            return resp
            # Catch all 500 error to handle unexpected errors, render error page to front end


@app.route('/<arg>', methods=['GET'])  # Handle any GET requests for URNs
def redirect_url(arg):
    """Redirect logic for any GET requests to any URI on top of base URL"""
    path = str(arg)
    if urls.check_url(path, 3) is False:  # Run check to see if URN is valid
        resp = make_response(render_template('404.html', code=404))
        return resp
        # Return 404 not found if URL is invalid
    cursor.execute(PATH_QUERY, (path,))
    # Execute query to obtain original URL that matches provided URN
    try:
        link = str(cursor.fetchone()[0])  # Fetch the original URL
        resp = make_response(redirect(link, code=302))
        return resp
        # Return 302 response to client, with original URL as redirect
    except TypeError:
        resp = make_response(render_template('404.html', code=404))
        return resp
        # Catch all 404 error handler for unknown URNs


@app.after_request
def add_security_headers(resp):
    """Add any headers to all responses generated"""
    resp.headers['Content-Security-Policy']='default-src \'self\''
    return resp
