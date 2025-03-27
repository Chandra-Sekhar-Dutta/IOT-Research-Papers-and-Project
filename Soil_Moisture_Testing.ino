#define MOISTURE_PIN A0  

void setup() {
  Serial.begin(9600);  
}

void loop() {
  int moistureValue = analogRead(MOISTURE_PIN);  
  int correctedValue = 1023 - moistureValue; // Inverting the values

  Serial.print("Corrected Moisture Level: ");
  Serial.println(correctedValue);  

  // Status Interpretation
  if (correctedValue < 300) {
    Serial.println("Status: Dry Soil 🌵");
  } else if (correctedValue < 700) {
    Serial.println("Status: Moist Soil 🌱");
  } else {
    Serial.println("Status: Wet Soil 💧");
  }

  Serial.println("------------------------");
  delay(1000);
}
