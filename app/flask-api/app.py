import os
import time
import logging
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
from flask import Flask, jsonify, request, Response
import mysql.connector
from mysql.connector import pooling, Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('flask-api')

app = Flask(__name__)

# Global Connection Pool reference
db_pool: Optional[pooling.MySQLConnectionPool] = None

def get_db_config() -> Dict[str, str]:
    """Extract database configuration from environment variables."""
    return {
        'host': os.environ.get('DB_HOST', 'mysql'),
        'user': os.environ.get('DB_USER', 'flaskuser'),
        'password': os.environ.get('DB_PASSWORD', 'flaskpass'),
        'database': os.environ.get('DB_NAME', 'flaskdb')
    }

def init_db_pool() -> pooling.MySQLConnectionPool:
    """Initialize MySQL connection pool with startup retry logic."""
    global db_pool
    if db_pool is not None:
        return db_pool

    config = get_db_config()
    max_retries = 30
    retry_delay = 2

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting database pool creation (attempt {attempt}/{max_retries})...")
            db_pool = pooling.MySQLConnectionPool(
                pool_name="flask_pool",
                pool_size=5,
                pool_reset_session=True,
                **config
            )
            logger.info("Database connection pool established successfully.")
            return db_pool
        except Error as err:
            logger.warning(f"Database connection attempt {attempt} failed: {err}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                logger.error("Exhausted database connection retries.")
                raise

def get_db_connection() -> PooledMySQLConnection:
    """Retrieve a database connection from the pool."""
    pool = init_db_pool()
    return pool.get_connection()

def init_db() -> None:
    """Initialize database schema if table does not exist."""
    conn: Optional[PooledMySQLConnection] = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        logger.info("Database schema verified.")
    except Error as err:
        logger.error(f"Error initializing database schema: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Initialize DB schema within app context on startup
with app.app_context():
    try:
        init_db()
    except Exception as e:
        logger.warning(f"Deferred DB initialization: {e}")

@app.errorhandler(Exception)
def handle_global_exception(error: Exception) -> Tuple[Response, int]:
    """Global exception handler returning clean JSON responses."""
    logger.exception(f"Unhandled exception: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health() -> Tuple[Response, int]:
    """Health check endpoint for readiness/liveness probes."""
    return jsonify({'status': 'healthy', 'service': 'flask-api'}), 200

@app.route('/api/items', methods=['GET'])
def get_items() -> Tuple[Response, int]:
    """Retrieve all items ordered by creation timestamp."""
    conn: Optional[PooledMySQLConnection] = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name, description, created_at FROM items ORDER BY created_at DESC')
        items: List[Dict[str, Any]] = cursor.fetchall()
        
        # Safely convert datetime objects to formatted strings
        for item in items:
            created_at = item.get('created_at')
            if isinstance(created_at, datetime):
                item['created_at'] = created_at.strftime('%Y-%m-%d %H:%M:%S')
            elif created_at is not None:
                item['created_at'] = str(created_at)
            else:
                item['created_at'] = ''

        return jsonify(items), 200
    except Error as err:
        logger.error(f"Database error in get_items: {err}")
        return jsonify({'error': 'Failed to retrieve items'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/items', methods=['POST'])
def create_item() -> Tuple[Response, int]:
    """Create a new item record."""
    data: Optional[Dict[str, Any]] = request.get_json(silent=True)
    if not data or 'name' not in data or not str(data['name']).strip():
        return jsonify({'error': 'Name is required'}), 400

    name: str = str(data['name']).strip()
    description: str = str(data.get('description', '')).strip()

    conn: Optional[PooledMySQLConnection] = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO items (name, description) VALUES (%s, %s)',
            (name, description)
        )
        conn.commit()
        item_id: int = cursor.lastrowid
        return jsonify({'id': item_id, 'name': name, 'description': description}), 201
    except Error as err:
        logger.error(f"Database error in create_item: {err}")
        return jsonify({'error': 'Failed to create item'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id: int) -> Tuple[Response, int]:
    """Delete an item record by ID."""
    conn: Optional[PooledMySQLConnection] = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
        conn.commit()
        affected: int = cursor.rowcount

        if affected == 0:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify({'message': 'Item deleted'}), 200
    except Error as err:
        logger.error(f"Database error in delete_item: {err}")
        return jsonify({'error': 'Failed to delete item'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
