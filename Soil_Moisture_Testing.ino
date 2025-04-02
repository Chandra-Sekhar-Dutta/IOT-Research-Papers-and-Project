// Define the pins
const int relayPin = 8;      // Relay control pin
const int moisturePin = A0;  // Moisture sensor analog pin

// Moisture threshold (adjust based on your sensor readings)
const int dryThreshold = 500;  // Below this value = needs water

void setup() {
  // Initialize the relay pin as an output
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);  // Start with pump off
  
  // Initialize serial communication
  Serial.begin(9600);
  Serial.println("Moisture-activated pump control ready");
}

void loop() {
  // Read moisture level (0-1023)
  int moistureValue = analogRead(moisturePin);
  
  Serial.print("Moisture: ");
  Serial.print(moistureValue);
  
  // Check if soil is too dry
  if (moistureValue > dryThreshold) {
    digitalWrite(relayPin, LOW);  // Turn pump ON
    Serial.println(" - Soil too dry, PUMP ON");
    delay(1000);  // Water for 1 second (adjust as needed)
    
    // Turn pump off after watering
    digitalWrite(relayPin, HIGH);
    Serial.println("Pump OFF after watering");
  }
  else {
    digitalWrite(relayPin, HIGH);  // Ensure pump is OFF
    Serial.println(" - Soil moist enough");
  }
  
  delay(1000);  // Wait 1 second between checks
}
