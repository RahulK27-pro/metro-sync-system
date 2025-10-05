from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint that provides API information."""
    return jsonify({
        'message': 'Metro Sync System API',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'routes': '/routes',
            'passengers': '/passengers',
            'cards': '/cards',
            'stations': '/stations',
            'trips': '/api/trips',
            'transactions': '/api/transactions',
            'fare_rules': '/api/fare-rules'
        }
    })

# Database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'project.db')

def get_db_connection() -> sqlite3.Connection:
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def execute_query(query: str, params: tuple = (), fetch_one: bool = False) -> Union[Dict, List[Dict], int, None]:
    """Execute a database query and return the results."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
            conn.commit()
            if query.strip().upper().startswith('INSERT'):
                return cursor.lastrowid
            return cursor.rowcount
        
        result = cursor.fetchone() if fetch_one else cursor.fetchall()
        return [dict(row) for row in result] if result and not fetch_one else (dict(result) if result else None)
        
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

# ==============================================================================
# == Card Operations
# ==============================================================================

@app.route('/cards', methods=['GET'])
def get_cards():
    """Get all cards with passenger and card type details."""
    try:
        query = """
            SELECT c.*, p.FirstName, p.LastName, p.Email, ct.TypeName, ct.BaseFareMultiplier
            FROM Card c
            LEFT JOIN Passenger p ON c.PassengerID = p.PassengerID
            LEFT JOIN CardType ct ON c.CardTypeID = ct.CardTypeID
            ORDER BY c.CardID
        """
        cards = execute_query(query)
        if cards is None:
            return jsonify([])
        return jsonify(cards if isinstance(cards, list) else [cards])
    except Exception as e:
        logger.error(f"Error fetching cards: {e}", exc_info=True)
        return jsonify({"error": f"Failed to fetch cards: {str(e)}"}), 500

@app.route('/api/cards', methods=['POST'])
def create_card():
    """Create a new metro card."""
    try:
        data = request.get_json()
        required_fields = ['cardNumber', 'balance', 'passengerId', 'cardTypeId']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        card_data = {
            'CardNumber': data['cardNumber'],
            'Balance': float(data['balance']),
            'IssueDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Status': data.get('status', 'Active'),
            'PassengerID': int(data['passengerId']),
            'CardTypeID': int(data['cardTypeId'])
        }
        
        query = """
        INSERT INTO Card (CardNumber, Balance, IssueDate, Status, PassengerID, CardTypeID)
        VALUES (:CardNumber, :Balance, :IssueDate, :Status, :PassengerID, :CardTypeID)
        """
        
        card_id = execute_query(query, tuple(card_data.values()))
        return jsonify({"id": card_id, "message": "Card created successfully"}), 201
        
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return jsonify({"error": "Invalid input data"}), 400
    except sqlite3.IntegrityError as e:
        logger.error(f"Database integrity error: {e}")
        return jsonify({"error": "Card with this number already exists"}), 409
    except Exception as e:
        logger.error(f"Error creating card: {e}")
        return jsonify({"error": "Failed to create card"}), 500

# ==============================================================================
# == Passenger Operations
# ==============================================================================

@app.route('/passengers', methods=['GET'])
def get_passengers():
    """Get all passengers with their card count."""
    try:
        query = """
        SELECT p.*, COUNT(c.CardID) as card_count
        FROM Passenger p
        LEFT JOIN Card c ON p.PassengerID = c.PassengerID
        GROUP BY p.PassengerID
        """
        passengers = execute_query(query)
        return jsonify(passengers or [])
    except Exception as e:
        logger.error(f"Error fetching passengers: {e}")
        return jsonify({"error": "Failed to fetch passengers"}), 500

@app.route('/api/passengers', methods=['POST'])
def create_passenger():
    """Create a new passenger."""
    try:
        data = request.get_json()
        required_fields = ['firstName', 'lastName', 'email']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        passenger_data = {
            'FirstName': data['firstName'].strip(),
            'LastName': data['lastName'].strip(),
            'Email': data['email'].strip().lower(),
            'PhoneNumber': data.get('phoneNumber', '').strip(),
            'RegistrationDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        query = """
        INSERT INTO Passenger (FirstName, LastName, Email, PhoneNumber, RegistrationDate)
        VALUES (:FirstName, :LastName, :Email, :PhoneNumber, :RegistrationDate)
        """
        
        passenger_id = execute_query(query, tuple(passenger_data.values()))
        return jsonify({"id": passenger_id, "message": "Passenger created successfully"}), 201
        
    except sqlite3.IntegrityError as e:
        logger.error(f"Database integrity error: {e}")
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        logger.error(f"Error creating passenger: {e}")
        return jsonify({"error": "Failed to create passenger"}), 500

# ==============================================================================
# == Trip Operations
# ==============================================================================

@app.route('/trips', methods=['GET'])
def get_trips():
    """Get all trips with related information."""
    try:
        query = """
        SELECT 
            t.TripID, t.EntryTime, t.ExitTime, t.FareAmount,
            c.CardNumber, p.PassengerID, p.FirstName, p.LastName,
            es.StationID as EntryStationID, es.StationName as EntryStation,
            xs.StationID as ExitStationID, xs.StationName as ExitStation
        FROM Trip t
        JOIN Card c ON t.CardID = c.CardID
        JOIN Passenger p ON c.PassengerID = p.PassengerID
        LEFT JOIN Station es ON t.EntryStationID = es.StationID
        LEFT JOIN Station xs ON t.ExitStationID = xs.StationID
        ORDER BY t.EntryTime DESC
        """
        trips = execute_query(query)
        return jsonify(trips or [])
    except Exception as e:
        logger.error(f"Error fetching trips: {e}")
        return jsonify({"error": "Failed to fetch trips"}), 500

@app.route('/trips', methods=['POST'])
def create_trip():
    """Create a new trip entry."""
    try:
        data = request.get_json()
        required_fields = ['cardId', 'entryStationId']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        trip_data = {
            'EntryTime': data.get('entryTime', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'ExitTime': data.get('exitTime'),
            'FareAmount': float(data.get('fareAmount', 0.0)),
            'CardID': int(data['cardId']),
            'EntryStationID': int(data['entryStationId']),
            'ExitStationID': int(data['exitStationId']) if data.get('exitStationId') else None
        }
        
        query = """
        INSERT INTO Trip (EntryTime, ExitTime, FareAmount, CardID, EntryStationID, ExitStationID)
        VALUES (:EntryTime, :ExitTime, :FareAmount, :CardID, :EntryStationID, :ExitStationID)
        """
        
        trip_id = execute_query(query, tuple(trip_data.values()))
        return jsonify({"id": trip_id, "message": "Trip recorded successfully"}), 201
        
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return jsonify({"error": "Invalid input data"}), 400
    except Exception as e:
        logger.error(f"Error creating trip: {e}")
        return jsonify({"error": "Failed to record trip"}), 500

# ==============================================================================
# == Station Operations
# ==============================================================================

@app.route('/stations', methods=['GET'])
def get_stations():
    """Get all stations."""
    try:
        stations = execute_query("SELECT * FROM Station ORDER BY StationName")
        return jsonify(stations or [])
    except Exception as e:
        logger.error(f"Error fetching stations: {e}")
        return jsonify({"error": "Failed to fetch stations"}), 500

# ==============================================================================
# == Card Type Operations
# ==============================================================================

@app.route('/card-types', methods=['GET'])
def get_card_types():
    """Get all card types."""
    try:
        card_types = execute_query("SELECT * FROM CardType ORDER BY TypeName")
        return jsonify(card_types or [])
    except Exception as e:
        logger.error(f"Error fetching card types: {e}")
        return jsonify({"error": "Failed to fetch card types"}), 500

# ==============================================================================
# == Transaction Operations
# ==============================================================================

@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions with card and passenger details."""
    try:
        query = """
        SELECT t.*, c.CardNumber, p.FirstName, p.LastName
        FROM [Transaction] t
        JOIN Card c ON t.CardID = c.CardID
        JOIN Passenger p ON c.PassengerID = p.PassengerID
        ORDER BY t.TransactionDate DESC
        """
        transactions = execute_query(query)
        return jsonify(transactions or [])
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        return jsonify({"error": "Failed to fetch transactions"}), 500

# ==============================================================================
# == Fare Rule Operations
# ==============================================================================

@app.route('/fare-rules', methods=['GET'])
def get_fare_rules():
    """Get all fare rules with station details."""
    try:
        query = """
        SELECT 
            fr.*, 
            s1.StationName as StartStationName,
            s2.StationName as EndStationName
        FROM FareRule fr
        JOIN Station s1 ON fr.StartStationID = s1.StationID
        JOIN Station s2 ON fr.EndStationID = s2.StationID
        ORDER BY s1.StationName, s2.StationName
        """
        fare_rules = execute_query(query)
        return jsonify(fare_rules or [])
    except Exception as e:
        logger.error(f"Error fetching fare rules: {e}")
        return jsonify({"error": "Failed to fetch fare rules"}), 500

# ==============================================================================
# == Health Check Endpoint
# ==============================================================================

@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])  # Support both /api/health and /health
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        conn = get_db_connection()
        if conn:
            conn.execute('SELECT 1')
            conn.close()
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': 'Could not connect to database'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# ==============================================================================
# == Error Handlers
# ==============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ==============================================================================
# == Main Application Entry Point
# ==============================================================================

# Add a route to list all available routes
@app.route('/routes', methods=['GET'])
def list_routes():
    """List all available routes for debugging."""
    routes = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        routes.append({
            'endpoint': rule.endpoint,
            'methods': methods,
            'rule': str(rule)
        })
    return jsonify(routes)

def initialize_database():
    """Initialize the database and return the database file path."""
    try:
        # Add the parent directory to Python path
        project_root = str(Path(__file__).parent.parent)
        sys.path.append(project_root)
        logger.info(f"Added to path: {project_root}")
        
        # Set the database file path
        db_file = os.path.join(project_root, 'project.db')
        logger.info(f"Database file path: {db_file}")
        
        # Import after adding to path
        from create_database import create_connection, create_tables_if_not_exist, insert_sample_data
        
        # Create connection and initialize database
        conn = create_connection(db_file)
        if conn:
            logger.info("Successfully connected to database")
            create_tables_if_not_exist(conn)
            insert_sample_data(conn)  # Insert sample data
            conn.close()
            logger.info("Database initialization completed")
            return db_file
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
    return None

# Initialize the database before starting the app
db_file = initialize_database()

# Print all registered routes when the app starts
with app.app_context():
    print("\n=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
    print("=======================\n")

if __name__ == '__main__':
    # Start the Flask application
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
