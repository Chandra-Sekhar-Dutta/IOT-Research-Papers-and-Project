const int relayPin = 8;      // Relay control pin
const int moisturePin = A0;  // Moisture sensor analog pin

// Settings (adjust based on your needs)
const int dryThreshold = 500;   // Below this = needs water
const int wateringTime = 3000;  // Water for 3 seconds (adjust)
const int checkInterval = 5000; // Wait 5 sec between checks (avoid rapid switching)

bool pumpRunning = false;
unsigned long lastCheckTime = 0;

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);  // Start with pump OFF
  Serial.begin(9600);
  Serial.println("Moisture-activated pump control ready");
}  

void loop() {
  unsigned long currentTime = millis();

  // Only check moisture at intervals (not every loop)
  if (currentTime - lastCheckTime >= checkInterval) {
    lastCheckTime = currentTime;

    int moistureValue = analogRead(moisturePin);
    Serial.print("Moisture: ");
    Serial.print(moistureValue);

    // If soil is dry and pump isn't already running
    if (moistureValue > dryThreshold && !pumpRunning) {
      pumpRunning = true;
      digitalWrite(relayPin, LOW);  // Turn pump ON
      Serial.println(" - Soil too dry, PUMP ON");
      
      delay(wateringTime);  // Water for set time
      
      digitalWrite(relayPin, HIGH);  // Turn pump OFF
      pumpRunning = false;
      Serial.println("Pump OFF after watering");
    }
    else {
      Serial.println(" - Soil moist enough");
    }
  }
}
