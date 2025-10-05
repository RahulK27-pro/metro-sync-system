import sqlite3
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================================================================
# == Part 1: Database Connection & Table Creation
# ==============================================================================

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
        
        conn.commit()
        logger.info("Database schema initialized successfully")
        
    except sqlite3.Error as e:
        logger.error(f"Error initializing database schema: {e}")
        conn.rollback()
        raise
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
        );""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS [Transaction] (
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            TransactionType TEXT NOT NULL,
            Amount REAL NOT NULL,
            TransactionDate TEXT NOT NULL,
            CardID INTEGER,
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        );""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS FareRule (
            FareRuleID INTEGER PRIMARY KEY AUTOINCREMENT,
            StartStationID INTEGER NOT NULL,
            EndStationID INTEGER NOT NULL,
            FareType TEXT,
            FareAmount REAL NOT NULL,
            FOREIGN KEY (StartStationID) REFERENCES Station(StationID),
            FOREIGN KEY (EndStationID) REFERENCES Station(StationID),
            UNIQUE (StartStationID, EndStationID, FareType)
        );""")
        
        cursor.execute("""
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
        );""")
        
        conn.commit()
        print("Tables checked/created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

# ==============================================================================
# == Part 2: INSERT Queries for Sample Data
# ==============================================================================

def insert_sample_data(conn):
    """ Insert at least 5 sample data records into the main tables """
    try:
        cursor = conn.cursor()
        
        print("Inserting new data... (will ignore duplicates)")
        
        passengers = [
            ('Sanjay', 'Kumar', 'sanjay.k@email.com', '9876543210', '2025-01-15'),
            ('Priya', 'Sharma', 'priya.s@email.com', '8765432109', '2025-02-20'),
            ('Arun', 'Verma', 'arun.v@email.com', '7654321098', '2025-03-10'),
            ('Meera', 'Nair', 'meera.n@email.com', '6543210987', '2025-04-05'),
            ('Rohan', 'Singh', 'rohan.s@email.com', '5432109876', '2025-05-25')
        ]
        cursor.executemany("INSERT OR IGNORE INTO Passenger (FirstName, LastName, Email, PhoneNumber, RegistrationDate) VALUES (?, ?, ?, ?, ?);", passengers)
        
        stations = [
            ('Central Station', 'Blue'), ('Market Square', 'Blue'),
            ('University Stop', 'Red'), ('Tech Park', 'Red'),
            ('City Airport', 'Green')
        ]
        cursor.executemany("INSERT OR IGNORE INTO Station (StationName, LineColor) VALUES (?, ?);", stations)
        
        card_types = [
            ('Adult', 1.0, 'Standard adult card'), ('Student', 0.6, 'Discounted card for students'),
            ('Senior', 0.5, 'Discounted card for senior citizens')
        ]
        cursor.executemany("INSERT OR IGNORE INTO CardType (TypeName, BaseFareMultiplier, Description) VALUES (?, ?, ?);", card_types)

        cards = [
            ('SNJ1001', 500.00, '2025-01-15', 'Active', 1, 1),
            ('PRI2002', 250.50, '2025-02-20', 'Active', 2, 2),
            ('ARU3003', 1000.00, '2025-03-10', 'Active', 3, 1),
            ('MEE4004', 150.00, '2025-04-05', 'Blocked', 4, 3), 
            ('ROH5005', 300.00, '2025-05-25', 'Active', 5, 2)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Card (CardNumber, Balance, IssueDate, Status, PassengerID, CardTypeID) VALUES (?, ?, ?, ?, ?, ?);", cards)

        transactions = [
            ('Top-up', 500.00, '2025-09-01 10:00:00', 1),
            ('Top-up', 300.00, '2025-09-05 11:30:00', 2),
            ('Top-up', 1000.00, '2025-09-10 15:00:00', 3),
            ('Top-up', 200.00, '2025-09-15 09:00:00', 4),
            ('Top-up', 350.00, '2025-09-20 18:45:00', 5)
        ]
        cursor.executemany("INSERT OR IGNORE INTO [Transaction] (TransactionType, Amount, TransactionDate, CardID) VALUES (?, ?, ?, ?);", transactions)
        
        fare_rules = [
            (1, 2, 'Peak', 25.00), (1, 3, 'Peak', 40.00),
            (2, 3, 'Off-Peak', 30.00), (3, 4, 'Off-Peak', 20.00),
            (1, 5, 'Anytime', 100.00)
        ]
        cursor.executemany("INSERT OR IGNORE INTO FareRule (StartStationID, EndStationID, FareType, FareAmount) VALUES (?, ?, ?, ?);", fare_rules)

        trips = [
            ('2025-10-03 09:00:00', '2025-10-03 09:15:00', 18.00, 2, 2, 3),
            ('2025-10-03 18:00:00', '2025-10-03 18:30:00', 40.00, 1, 1, 3),
            ('2025-10-04 11:00:00', '2025-10-04 11:10:00', 20.00, 3, 3, 4),
            ('2025-10-04 12:00:00', None, None, 5, 1, None),
            ('2025-10-04 14:00:00', '2025-10-04 14:45:00', 100.00, 3, 1, 5)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Trip (EntryTime, ExitTime, FareAmount, CardID, EntryStationID, ExitStationID) VALUES (?, ?, ?, ?, ?, ?);", trips)

        conn.commit()
        print("Sample data insertion process completed.")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
        
# ==============================================================================
# == Part 3: DML Command Examples
# ==============================================================================

def perform_dml_commands(conn):
    """ Perform UPDATE, DELETE, and SELECT manipulations """
    print("\n--- Performing DML Commands ---")
    try:
        cursor = conn.cursor()

        print("\n1. UPDATE: Changing the status of Meera's card (CardID=4) to 'Active'.")
        cursor.execute("UPDATE Card SET Status = 'Active' WHERE CardID = 4;")
        conn.commit()
        print("   Update successful.")
        
        print("\n2. SELECT: Fetching card details for passenger 'Meera Nair' to verify the update.")
        cursor.execute("""
            SELECT p.FirstName, p.LastName, c.CardNumber, c.Status
            FROM Card c JOIN Passenger p ON c.PassengerID = p.PassengerID
            WHERE p.FirstName = 'Meera';
        """)
        result = cursor.fetchone()
        if result:
            print(f"   Result -> Name: {result[0]} {result[1]}, Card: {result[2]}, New Status: {result[3]}")

        print("\n3. DELETE: Deleting any fare rule that starts or ends at 'Tech Park' (StationID=4).")
        cursor.execute("DELETE FROM FareRule WHERE StartStationID = 4 OR EndStationID = 4;")
        rows_deleted = cursor.rowcount
        conn.commit()
        print(f"   Successfully deleted {rows_deleted} rule(s).")
        
        print("\n4. SELECT: Finding all passengers with a card balance below 300.")
        cursor.execute("""
            SELECT p.FirstName, p.LastName, c.Balance
            FROM Passenger p JOIN Card c ON p.PassengerID = c.PassengerID
            WHERE c.Balance < 300;
        """)
        low_balance_users = cursor.fetchall()
        print(f"   Found {len(low_balance_users)} user(s) with low balance:")
        for user in low_balance_users:
             print(f"   -> Name: {user[0]} {user[1]}, Balance: {user[2]:.2f}")

        # --- NEW DML COMMANDS START HERE ---

        # DML Command 5: A more complex UPDATE to complete a trip
        print("\n5. UPDATE: Completing Rohan's in-progress trip (TripID=4).")
        trip_id_to_complete = 4
        exit_station_id = 3 # University Stop
        fare = 24.00 # Assume fare is calculated (40.00 base * 0.6 student multiplier)
        card_id_for_trip = 5 # Rohan's CardID
        
        # First, update the trip record with exit info
        cursor.execute("""
            UPDATE Trip 
            SET ExitTime = ?, ExitStationID = ?, FareAmount = ? 
            WHERE TripID = ?;
        """, (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), exit_station_id, fare, trip_id_to_complete))
        
        # Second, deduct the fare from the card's balance
        cursor.execute("UPDATE Card SET Balance = Balance - ? WHERE CardID = ?;", (fare, card_id_for_trip))
        conn.commit()
        print(f"   Trip {trip_id_to_complete} completed. Deducted {fare:.2f} from Card {card_id_for_trip}.")

        # DML Command 6: SELECT with aggregation (GROUP BY and COUNT)
        print("\n6. SELECT (Aggregate): Counting the number of trips taken by each passenger.")
        cursor.execute("""
            SELECT p.FirstName, p.LastName, COUNT(t.TripID) as TripCount
            FROM Passenger p
            JOIN Card c ON p.PassengerID = c.PassengerID
            JOIN Trip t ON c.CardID = t.CardID
            GROUP BY p.PassengerID
            ORDER BY TripCount DESC;
        """)
        trip_counts = cursor.fetchall()
        print(f"   Found trip data for {len(trip_counts)} passenger(s):")
        for passenger in trip_counts:
            print(f"   -> Name: {passenger[0]} {passenger[1]}, Trips Taken: {passenger[2]}")

    except sqlite3.Error as e:
        print(f"An error occurred during DML operations: {e}")

# ==============================================================================
# == Main Execution Block
# ==============================================================================

if __name__ == "__main__":
    database_file = "project.db"
    
    connection = create_connection(database_file)
    
    if connection:
        create_tables_if_not_exist(connection)
        insert_sample_data(connection)
        perform_dml_commands(connection)
        connection.close()
        print("\nDatabase connection closed.")
