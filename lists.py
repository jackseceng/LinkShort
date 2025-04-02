import sqlite3

import urllib3

http = urllib3.PoolManager()
CON = sqlite3.connect("app/badsites.db")

cur = CON.cursor()
cur.execute("""CREATE TABLE [badsites] ([site] TEXT)""")


def add_sites(response):
    sites = ""
    for site in response.data.decode("utf-8"):
        if site == "\n":
            sites = sites.replace("\n", "")
            cur.execute("""INSERT INTO badsites VALUES (?)""", (sites,))
            sites = ""
        sites += site

    CON.commit()


if __name__ == "__main__":
    URL1 = "https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt"
    URL2 = "https://raw.githubusercontent.com/stamparm/blackbook/refs/heads/master/blackbook.txt"

    add_sites(http.request("GET", URL1))
    add_sites(http.request("GET", URL2))

    CON.close()
