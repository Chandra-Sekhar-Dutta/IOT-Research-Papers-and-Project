# 🌱 IoT-Based Smart Irrigation System

## 📌 Project Overview  
This project implements an **IoT-based Smart Irrigation System** that automates plant watering using real-time soil moisture data. The system consists of an Arduino-based sensor module and a Python backend for data logging and visualization.

## 🎯 Key Features  
- **Real-time Soil Monitoring**: Measures moisture levels continuously.  
- **Automated Watering**: Activates pump when soil is too dry.  
- **Data Logging**: Stores sensor readings in a MySQL database.  
- **Visualization**: Generates time-series graphs of moisture levels.  

## 🏗️ System Architecture  
**Arduino (Sensor & Pump Control) → Python (Data Processing) → MySQL (Storage) → Matplotlib (Visualization)**  

## 📂 Project Files  

### Arduino Sketch  
- `Soil_Moisture_Testing.ino` - Controls moisture sensor and water pump  

### Python Scripts  
- `arduino_to_mysql.py` - Handles:  
  - Serial communication with Arduino  
  - Data parsing and validation  
  - MySQL database operations  
- `graph.py` - Provides:  
  - Data retrieval from MySQL  
  - Interactive moisture level visualization  

## 🛠️ Installation  

### Python Requirements  
Install dependencies via pip:  
```bash
pip install pyserial mysql-connector-python matplotlib
```

### Database Setup  
Create MySQL database:  
```sql
CREATE DATABASE sensor_data;
USE sensor_data;
CREATE TABLE moisture_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    moisture_value INT NOT NULL,
    timestamp DATETIME NOT NULL
);
```

## 🔌 Hardware Setup  
1. Connect soil moisture sensor to Arduino's **A0** pin.  
2. Connect relay module to **pin 8**.  
3. Connect Arduino via **USB** to a computer running Python scripts.  

## 🚀 Usage  

1. Upload the Arduino sketch.  
2. Run the data logger:  
   ```bash
   python arduino_to_mysql.py
   ```
3. Generate graphs:  
   ```bash
   python graph.py
   ```

## 📊 Data Flow  
**Arduino → Serial Port → Python (Parser) → MySQL → Matplotlib**  

## 🔮 Future Enhancements  
- Web-based dashboard using Flask/Django  
- Mobile notifications for dry soil conditions  
- Multi-sensor support (temperature/humidity)  

## 📜 License  
**MIT License** - Open source for educational and personal use.  

