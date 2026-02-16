"""Statistics tracking and management module for link clicks and analytics"""

import logging
from datetime import datetime
from os import environ
from re import search

from dotenv import load_dotenv
from libsql import connect

load_dotenv()

url = environ["ENDPOINT"]
auth_token = environ["TOKEN"]

def _create_connection():
    """Creates and returns a new database connection."""
    conn = connect("urls.db", sync_url=url, auth_token=auth_token)
    conn.sync()
    return conn

def record_click(hashsum: str, user_agent: str = None, referrer: str = None, ip_address: str = None):
    """Record a click event for a shortened link"""
    conn = _create_connection()
    try:
        click_time = datetime.utcnow().isoformat()
        conn.execute(
            """INSERT INTO click_stats(hashsum, click_time, user_agent, referrer, ip_address) 
               VALUES (?, ?, ?, ?, ?)""",
            (hashsum, click_time, user_agent, referrer, ip_address),
        )
        conn.commit()
        return True, None
    except Exception as e:
        logging.error("Error recording click: %s", e)
        return False, str(e)
    finally:
        if conn:
            conn.close()

def get_click_stats(hashsum: str):
    """Get all click statistics for a given shortened link"""
    conn = _create_connection()
    try:
        result_set = conn.execute(
            "SELECT COUNT(*) as total_clicks FROM click_stats WHERE hashsum = ?",
            (hashsum,),
        )
        row = result_set.fetchone()
        total_clicks = row[0] if row else 0
        
        # Get unique visitors (by IP address)
        unique_result = conn.execute(
            "SELECT COUNT(DISTINCT ip_address) as unique_visitors FROM click_stats WHERE hashsum = ?",
            (hashsum,),
        )
        unique_row = unique_result.fetchone()
        unique_visitors = unique_row[0] if unique_row else 0
        
        return {
            "total_clicks": total_clicks,
            "unique_visitors": unique_visitors,
            "hashsum": hashsum
        }
    except Exception as e:
        logging.error("Error getting click stats: %s", e)
        return None
    finally:
        if conn:
            conn.close()

def get_click_history(hashsum: str, limit: int = 100):
    """Get recent click history for a given shortened link"""
    conn = _create_connection()
    try:
        result_set = conn.execute(
            """SELECT click_time, referrer, user_agent 
               FROM click_stats WHERE hashsum = ? 
               ORDER BY click_time DESC LIMIT ?""",
            (hashsum, limit),
        )
        clicks = result_set.fetchall()
        return [
            {
                "click_time": click[0],
                "referrer": click[1],
                "user_agent": click[2]
            } for click in clicks
        ]
    except Exception as e:
        logging.error("Error getting click history: %s", e)
        return []
    finally:
        if conn:
            conn.close()

def get_daily_stats(hashsum: str):
    """Get click statistics aggregated by day"""
    conn = _create_connection()
    try:
        result_set = conn.execute(
            """SELECT DATE(click_time) as day, COUNT(*) as clicks 
               FROM click_stats WHERE hashsum = ? 
               GROUP BY DATE(click_time) 
               ORDER BY day DESC""",
            (hashsum,),
        )
        rows = result_set.fetchall()
        return [{"day": row[0], "clicks": row[1]} for row in rows]
    except Exception as e:
        logging.error("Error getting daily stats: %s", e)
        return []
    finally:
        if conn:
            conn.close()