#include <Servo.h>

Servo barrier;

void setup() {
  Serial.begin(9600);
  barrier.attach(9);
  barrier.write(0);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "OPEN") {
      barrier.write(90);
      delay(10000);
      barrier.write(0);
    }
  }
}