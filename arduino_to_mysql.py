import serial
import mysql.connector
import time
import re
from datetime import datetime

# Configuration
SERIAL_PORT = 'COM19'  # Update this to your Arduino's port
BAUD_RATE = 9600
MAX_ATTEMPTS = 3
READING_INTERVAL = 2  # seconds

def connect_to_database():
    """Establish connection to MySQL database"""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Chandra2011#",
            database="sensor_data",
            autocommit=True
        )
        print("✅ Connected to MySQL database")
        return db
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        return None

def parse_moisture_data(data):
    """Extract moisture value from serial data"""
    try:
        # Look for patterns like "Moisture: 450" or "450 - Soil"
        match = re.search(r'Moisture:\s*(\d+)|(\d+)\s*-\s*Soil', data)
        if match:
            return int(match.group(1) if match.group(1) else match.group(2))
    except (ValueError, AttributeError):
        pass
    return None

def insert_reading(db, value):
    """Insert reading into database if it's new"""
    try:
        cursor = db.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Check if similar value exists within last minute
        cursor.execute("""
            SELECT COUNT(*) FROM moisture_log 
            WHERE ABS(moisture_value - %s) < 10 
            AND timestamp > NOW() - INTERVAL 1 MINUTE
        """, (value,))
        
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO moisture_log (moisture_value, timestamp)
                VALUES (%s, %s)
            """, (value, timestamp))
            print(f"✅ Inserted new reading: {value} at {timestamp}")
        else:
            print(f"🔄 Similar reading recently recorded, skipping: {value}")
            
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")

def main():
    # Initialize connections
    db = connect_to_database()
    if not db:
        return

    arduino = None
    attempts = 0
    
    while attempts < MAX_ATTEMPTS:
        try:
            arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)  # Allow Arduino to initialize
            print(f"✅ Connected to Arduino on {SERIAL_PORT}")
            break
        except serial.SerialException as err:
            attempts += 1
            print(f"⚠️ Attempt {attempts}/{MAX_ATTEMPTS}: {err}")
            time.sleep(2)
    
    if not arduino:
        print("❌ Failed to connect to Arduino")
        db.close()
        return

    try:
        while True:
            try:
                data = arduino.readline().decode('utf-8').strip()
                if not data:
                    continue
                    
                print(f"📡 Raw data: {data}")
                moisture_value = parse_moisture_data(data)
                
                if moisture_value is not None:
                    insert_reading(db, moisture_value)
                else:
                    print(f"⚠️ Could not parse moisture value from: {data}")
                
                time.sleep(READING_INTERVAL)
                
            except UnicodeDecodeError:
                print("⚠️ Received malformed data from Arduino")
            except Exception as err:
                print(f"⚠️ Unexpected error: {err}")
                time.sleep(5)  # Wait before retrying
                
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    finally:
        if arduino:
            arduino.close()
        if db:
            db.close()
        print("🔌 Disconnected from Arduino and MySQL")

if __name__ == "__main__":
    main()