#include "Keyboard.h"

//declaring button pins
const int buttonPin = 2;
const int Vy = A1;

int previousButtonState = HIGH;

void setup() {
  //declare the buttons as input_pullup
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(Vy, INPUT);
  Keyboard.begin();
  Serial.begin(9600);
}

void loop() {
  //checking the state of the button
  int buttonState = digitalRead(buttonPin);
  Serial.println(String(analogRead(Vy)));


  if (analogRead(Vy) > 700) {
    Keyboard.press(100);
    delay(50);
    Keyboard.release(100);
  }
  else if (analogRead(Vy) < 200) {
    Keyboard.press(97);
    delay(50);
    Keyboard.release(97);

  }

//När knappen går från inte ner tryckt till ner tryckt så skrivs "d" ut
  if (buttonState == LOW && previousButtonState == HIGH) {
    // and it's currently pressed:
    Keyboard.press(101);
    delay(50);
  }


//När knappen går från ner tryckt till inte ner tryckt så skrivs "eeedaddaaa" ut
  if (buttonState == HIGH && previousButtonState == LOW) {
    // and it's currently released:
    Keyboard.release(101);
    delay(50);
  }

  previousButtonState = buttonState;

}
