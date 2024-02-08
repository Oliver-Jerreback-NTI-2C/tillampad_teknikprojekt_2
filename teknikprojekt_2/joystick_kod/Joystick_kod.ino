/* File name: teknikprojekt_2.ino
 * Author: Oliver Jerrebäck
 * Date:2024-02-08
 * Description: En joystick som skriver ut bokstäver beroende på hur mycket man höjt den i Y-led.
 */


#include "Keyboard.h"

//deklarerar pinsen
const int buttonPin = 2;
const int Vy = A1;
//skapar variabeln previousbuttonstate
int previousButtonState = HIGH;


//deklarerar buttonpins som input_pullup men vy vilket är y axeln på joysticken som en input. Sen även "serial" för seriel monitorn och "keyboard" för att skriva ut bokstäver
void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(Vy, INPUT);
  Keyboard.begin();
  Serial.begin(9600);
}

//här loopar vi bara vad vi ska göra 
void loop() {
  //kollar state på knappen
  int buttonState = digitalRead(buttonPin);
  Serial.println(String(analogRead(Vy)));

 //ifall knappen har över 700 i serielmonitorn ska den skriva ut bokstaven som är på "100"(a) och sedan släppa så den inte oändligt skriver ut bokstaven
  if (analogRead(Vy) > 700) {
    Keyboard.press(100);
    delay(50);
    Keyboard.release(100);
  }
   //här gör vi samma sak fast under 200 så skriver man ut en annan bokstav (d)
  else if (analogRead(Vy) < 200) {
    Keyboard.press(97);
    delay(50);
    Keyboard.release(97);
  }

//När knappen går från inte ner tryckt till ner tryckt så skrivs "y" ut
  if (buttonState == LOW && previousButtonState == HIGH) {
    // and it's currently pressed:
    Keyboard.press(101);
    delay(50);
  }


//När knappen går från ner tryckt till inte ner tryckt så skrivs "y" ut
  if (buttonState == HIGH && previousButtonState == LOW) {
    // and it's currently released:
    Keyboard.release(101);
    delay(50);
  }

  previousButtonState = buttonState;

}
