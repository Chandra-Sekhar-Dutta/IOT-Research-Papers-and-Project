import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def connect_to_database():
    """Establish connection to MySQL database"""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Chandra2011#",
            database="sensor_data"
        )
        print("✅ Connected to MySQL database")
        return db
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        return None

def fetch_recent_data(db, hours=24):
    """Fetch recent data from the database"""
    try:
        cursor = db.cursor()
        query = """
            SELECT moisture_value, timestamp 
            FROM moisture_log 
            WHERE timestamp > %s
            ORDER BY timestamp ASC
        """
        time_threshold = datetime.now() - timedelta(hours=hours)
        cursor.execute(query, (time_threshold,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"❌ Failed to fetch data: {err}")
        return None

def plot_data(data):
    """Create and display the plot"""
    if not data:
        print("⚠️ No data available to plot")
        return

    timestamps = [row[1] for row in data]
    values = [row[0] for row in data]

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, values, 'b-', marker='o', markersize=4, label="Moisture Level")
    
    # Formatting
    plt.title("Soil Moisture Monitoring")
    plt.xlabel("Time")
    plt.ylabel("Moisture Value")
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format x-axis to show time properly
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=45)
    
    # Add some padding
    plt.tight_layout()
    plt.legend()
    plt.show()

def main():
    db = connect_to_database()
    if not db:
        return

    try:
        data = fetch_recent_data(db)
        if data:
            plot_data(data)
        else:
            print("⚠️ No data found in the specified time range")
    except Exception as err:
        print(f"❌ Unexpected error: {err}")
    finally:
        db.close()
        print("🔌 Disconnected from MySQL database")

if __name__ == "__main__":
    main()