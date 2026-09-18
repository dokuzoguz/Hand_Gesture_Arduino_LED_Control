#include <Arduino.h>
#define THUMB 2
#define INDEX 3
#define MIDDLE 4
#define RING 5
#define PINKY 6

unsigned long LastDataTime = 0;
const unsigned long Treshold = 100;

void setup() {
  pinMode(THUMB , OUTPUT);
  pinMode(INDEX , OUTPUT);
  pinMode(MIDDLE , OUTPUT);
  pinMode(RING , OUTPUT);
  pinMode(PINKY , OUTPUT);
  Serial.begin(115200);
}

int MyArray[5] = {0};

void loop() {
  if(Serial.available()>0){
    LastDataTime = millis();

    String message = Serial.readStringUntil('\n');
    message.trim();
    for(int i=0; i<message.length(); i++){
      if(message[i]=='1'){
        MyArray[i] = 1;
      }else{
        MyArray[i] = 0;
      }
    }

    digitalWrite(THUMB , MyArray[0]);
    digitalWrite(INDEX , MyArray[1]);
    digitalWrite(MIDDLE , MyArray[2]);
    digitalWrite(RING , MyArray[3]);
    digitalWrite(PINKY , MyArray[4]);

  }
  
  if ((millis() - LastDataTime) > Treshold) {

    digitalWrite(THUMB , 0);
    digitalWrite(INDEX , 0);
    digitalWrite(MIDDLE , 0);
    digitalWrite(RING , 0);
    digitalWrite(PINKY , 0);

  }
}