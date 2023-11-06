import psycopg2

import logging


db_params = {
    'dbname': 'links',
    'user': 'postgresadmin',
    'password': 'admin123',
    'host': 'localhost', #change this to the container name of the postgres container
    'port': 5432
}

# DB table creation (use docker-development-youtube-series/storage/databases/postgresql/3-replication directory)
# docker run -it --rm --name postgres-1 --net postgres -e POSTGRES_USER=postgresadmin -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=links -e PGDATA="/data" -v ${PWD}/postgres-1/pgdata:/data -v ${PWD}/postgres-1/config:/config -v ${PWD}/postgres-1/archive:/mnt/server/archive -p 5000:5432 postgres:15.0 -c 'config_file=/config/postgresql.conf'
# (New terminal) docker exec -it postgres-1 bash
# psql --username=postgresadmin postgresdb
# CREATE TABLE links (path text, link text);

# App Container tesitng: 
# python3
# import db_mgmt
# db_mgmt.insert_link('path1', 'link1')

def insert_link(path, link):
    # Test data: INSERT INTO links (path, link) VALUES ('path2', 'link2');
    # Test output: SELECT * FROM links;
    # path  | link  
    #-------+-------
    # path1 | link1
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(**db_params)

    # Create a cursor object to interact with the database
        cursor = connection.cursor()

    # Define the SQL statement with placeholders for three values
        insert_query = "INSERT INTO links (path, link) VALUES (%s, %s);"

    # Values to insert
        values = (path, link)  # Replace with your actual values

    # Execute the INSERT statement with the specified values
        cursor.execute(insert_query, values)

    # Commit the transaction
        connection.commit()
        print("Data inserted successfully.")

    # Don't forget to close the cursor and connection when you're done
        cursor.close()
        connection.close()

        return True
    except (Exception, psycopg2.Error) as error:
        psql_error = ("PostgreSQL Error:", error)
        logging.warning(psql_error)
        return False



def check_link(path):
    #Test output: SELECT EXISTS(SELECT 1 FROM links WHERE link = 'link value');
    # exists 
    #--------
    # t (f if false)
    #(1 row)
    try:
        # Establish a connection to the database
        logging.warning("Checking for link collision")
        # NOTE TO SELF: THE DB AND THE APP ARE USING THE SAME PORT, SO THE APP CAN'T CONNECT TO THE DB
        connection = psycopg2.connect(**db_params)
        logging.warning("Connection established")

        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        logging.warning("Cursor created")

        # Define the SQL statement to check for a link collision
        collision_query = "SELECT EXISTS(SELECT 1 FROM links WHERE path = %s);"
        logging.warning("Collision query defined")

        # Execute the SELECT statement with the specified value
        cursor.execute(collision_query, (path,))
        logging.warning("Collision query executed")

        # Retrieve the results of the SELECT statement
        collision = cursor.fetchone()[0]
        logging.warning("Collision query results retrieved")

        # Commit the transaction
        connection.commit()
        logging.warning("Transaction committed")

        # Don't forget to close the cursor and connection when you're done
        cursor.close()
        logging.warning("Cursor closed")
        connection.close()
        logging.warning("Connection closed")

        logging.warning("Collision result")
        logging.warning(collision)
        return collision
    except (Exception, psycopg2.Error) as error:
        psql_error = ("PostgreSQL Error:", error)
        logging.warning(psql_error)



def get_link(path):
    # Test output: SELECT link FROM links WHERE path = 'path value';
    # link
    #-------
    #link1
    #(1 row)
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(**db_params)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Define the SQL statement to check for a link collision
        path_query = "SELECT link FROM links WHERE path = %s;"

        # Execute the SELECT statement with the specified value
        cursor.execute(path_query, (path,))

        # Retrieve the results of the SELECT statement
        link = cursor.fetchone()[0]

        # Commit the transaction
        connection.commit()

        # Don't forget to close the cursor and connection when you're done
        cursor.close()
        connection.close()

        return link
    except (Exception, psycopg2.Error) as error:
        psql_error = ("PostgreSQL Error:", error)
        logging.warning(psql_error)
        return False
