#include <cvzone.h>

SerialData arduino(1, 1); //(numOfValsRec,digitsPerValRec)
int occupancy[1];
int threshold = 800;

// RGB format
int LEDs[6] = {6, 7, 8, 9, 10}; // led1, led2

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < 6; i++) {
    pinMode(LEDs[i], OUTPUT);
  }
  arduino.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  int LightIntensity = analogRead(A0); // 0-1023
  if (LightIntensity < threshold) { // Dim
      arduino.Get(occupancy); // Get occupancy status
      if (occupancy[0] == 1){ // Have people
        for (int i = 0; i < 6; i++) {
          digitalWrite(LEDs[i], 1); // Lights ON
        }
      } else { // No People
          for (int i = 0; i < 6; i++) {
            digitalWrite(LEDs[i], 0); //Lights OFF
          }
        }
  } else { // Bright
      for (int i = 0; i < 6; i++) {
          digitalWrite(LEDs[i], 0); // Lights OFF
      }
  }
}
