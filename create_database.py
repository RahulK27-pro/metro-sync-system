import sqlite3
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_connection(db_file: str) -> Optional[sqlite3.Connection]:
    """
    Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(db_file)), exist_ok=True)
        
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        logger.info(f"Successfully connected to SQLite database at: {os.path.abspath(db_file)}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database {db_file}: {e}", exc_info=True)
        return None

def create_tables_if_not_exist(conn: sqlite3.Connection) -> None:
    """
    Create database tables if they don't exist
    :param conn: Connection object
    :return: None
    """
    if not conn:
        logger.error("No database connection provided")
        return
        
    tables = {
        'CardType': """
        CREATE TABLE IF NOT EXISTS CardType (
            CardTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
            TypeName TEXT NOT NULL UNIQUE,
            BaseFareMultiplier REAL NOT NULL DEFAULT 1.00,
            Description TEXT
        )""",
        
        'Passenger': """
        CREATE TABLE IF NOT EXISTS Passenger (
            PassengerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            PhoneNumber TEXT UNIQUE,
            RegistrationDate TEXT NOT NULL
        )""",
        
        'Station': """
        CREATE TABLE IF NOT EXISTS Station (
            StationID INTEGER PRIMARY KEY AUTOINCREMENT,
            StationName TEXT NOT NULL UNIQUE,
            LineColor TEXT
        )""",
        
        'Card': """
        CREATE TABLE IF NOT EXISTS Card (
            CardID INTEGER PRIMARY KEY AUTOINCREMENT,
            CardNumber TEXT NOT NULL UNIQUE,
            Balance REAL NOT NULL DEFAULT 0.00,
            IssueDate TEXT NOT NULL,
            Status TEXT NOT NULL CHECK (Status IN ('Active', 'Inactive', 'Blocked')),
            PassengerID INTEGER,
            CardTypeID INTEGER,
            FOREIGN KEY (PassengerID) REFERENCES Passenger(PassengerID),
            FOREIGN KEY (CardTypeID) REFERENCES CardType(CardTypeID)
        )""",
        
        'Transaction': """
        CREATE TABLE IF NOT EXISTS [Transaction] (
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            TransactionType TEXT NOT NULL,
            Amount REAL NOT NULL,
            TransactionDate TEXT NOT NULL,
            CardID INTEGER,
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        )""",
        
        'FareRule': """
        CREATE TABLE IF NOT EXISTS FareRule (
            FareRuleID INTEGER PRIMARY KEY AUTOINCREMENT,
            StartStationID INTEGER NOT NULL,
            EndStationID INTEGER NOT NULL,
            FareType TEXT,
            FareAmount REAL NOT NULL,
            FOREIGN KEY (StartStationID) REFERENCES Station(StationID),
            FOREIGN KEY (EndStationID) REFERENCES Station(StationID),
            UNIQUE (StartStationID, EndStationID, FareType)
        )""",
        
        'Trip': """
        CREATE TABLE IF NOT EXISTS Trip (
            TripID INTEGER PRIMARY KEY AUTOINCREMENT,
            EntryTime TEXT NOT NULL,
            ExitTime TEXT,
            FareAmount REAL,
            CardID INTEGER NOT NULL,
            EntryStationID INTEGER NOT NULL,
            ExitStationID INTEGER,
            FOREIGN KEY (CardID) REFERENCES Card(CardID),
            FOREIGN KEY (EntryStationID) REFERENCES Station(StationID),
            FOREIGN KEY (ExitStationID) REFERENCES Station(StationID)
        )"""
    }
    
    try:
        cursor = conn.cursor()
        
        # Create tables
        for table_name, create_sql in tables.items():
            try:
                cursor.execute(create_sql)
                logger.info(f"Created/Verified table: {table_name}")
            except sqlite3.Error as e:
                logger.error(f"Error creating table {table_name}: {e}")
                raise
        
        # Insert default card types if they don't exist
        default_card_types = [
            ('Regular', 1.0, 'Standard fare card'),
            ('Student', 0.5, 'Discounted fare for students'),
            ('Senior', 0.7, 'Discounted fare for senior citizens'),
            ('Monthly', 0.9, 'Monthly subscription card')
        ]
        
        cursor.execute("SELECT COUNT(*) FROM CardType")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO CardType (TypeName, BaseFareMultiplier, Description)
                VALUES (?, ?, ?)
                """,
                default_card_types
            )
            logger.info("Inserted default card types")
        
        # Insert some default stations if they don't exist
        default_stations = [
            ('Central Station', 'Blue'),
            ('Downtown', 'Blue'),
            ('University', 'Red'),
            ('City Park', 'Green'),
            ('Terminal', 'Red')
        ]
        
        cursor.execute("SELECT COUNT(*) FROM Station")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO Station (StationName, LineColor)
                VALUES (?, ?)
                """,
                default_stations
            )
            logger.info("Inserted default stations")
        
        conn.commit()
        logger.info("Database schema initialized successfully")
        
    except sqlite3.Error as e:
        logger.error(f"Error initializing database schema: {e}")
        conn.rollback()
        raise

def insert_sample_data(conn: sqlite3.Connection) -> None:
    """
    Insert sample data into the database
    :param conn: Connection object
    :return: None
    """
    if not conn:
        return
        
    try:
        cursor = conn.cursor()
        
        # Check if we already have passengers
        cursor.execute("SELECT COUNT(*) FROM Passenger")
        if cursor.fetchone()[0] > 0:
            logger.info("Sample data already exists, skipping...")
            return
            
        # Insert sample passengers
        sample_passengers = [
            ('John', 'Doe', 'john.doe@example.com', '1234567890'),
            ('Jane', 'Smith', 'jane.smith@example.com', '9876543210'),
            ('Alice', 'Johnson', 'alice.j@example.com', '5551234567')
        ]
        
        cursor.executemany(
            """
            INSERT INTO Passenger (FirstName, LastName, Email, PhoneNumber, RegistrationDate)
            VALUES (?, ?, ?, ?, datetime('now'))
            """,
            sample_passengers
        )
        
        # Get the inserted passenger IDs
        cursor.execute("SELECT PassengerID, Email FROM Passenger")
        passengers = {row['Email']: row['PassengerID'] for row in cursor.fetchall()}
        
        # Insert sample cards
        cursor.execute("SELECT CardTypeID, TypeName FROM CardType")
        card_types = {row['TypeName']: row['CardTypeID'] for row in cursor.fetchall()}
        
        sample_cards = [
            ('CARD001', 100.0, 'Active', passengers['john.doe@example.com'], card_types['Regular']),
            ('CARD002', 50.0, 'Active', passengers['jane.smith@example.com'], card_types['Student']),
            ('CARD003', 200.0, 'Active', passengers['alice.j@example.com'], card_types['Monthly'])
        ]
        
        cursor.executemany(
            """
            INSERT INTO Card (CardNumber, Balance, Status, PassengerID, CardTypeID, IssueDate)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
            sample_cards
        )
        
        conn.commit()
        logger.info("Sample data inserted successfully")
        
    except sqlite3.Error as e:
        logger.error(f"Error inserting sample data: {e}")
        conn.rollback()
        raise

if __name__ == "__main__":
    # Initialize the database
    db_file = os.path.join(os.path.dirname(__file__), "project.db")
    conn = create_connection(db_file)
    
    if conn:
        try:
            create_tables_if_not_exist(conn)
            insert_sample_data(conn)
            logger.info("Database initialization completed successfully!")
        except Exception as e:
            logger.error(f"Error during database initialization: {e}")
        finally:
            conn.close()
    else:
        logger.error("Failed to create database connection")
