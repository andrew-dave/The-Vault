#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define RST_PIN 9
#define SERVO_PIN 3
int pos=2;
MFRC522 mfrc522(RST_PIN);   // Create MFRC522 instance.
Servo servo;
void rotateServo();

void setup() {
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  servo.attach(SERVO_PIN); // Attach servo to pin 7
  Serial.println("Approximate your card to the reader...");
  Serial.println();
  servo.write(pos);

 
}

void loop() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  //Show UID on serial monitor
  Serial.print("UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Message : ");
  content.toUpperCase();
  if (content.substring(1) == "C3 D1 DA A1") //change here the UID of the card/cards that you want to give access
  {
    Serial.println("Authorized access for Devika");
    Serial.println();
    // Send data to Raspberry Pi
    Serial.println(content);
  }
  else if(content.substring(1) == "13 0E 40 0F")
  {
    Serial.println("Authorized access for Andrew");
    Serial.println();
    // Send data to Raspberry Pi
    Serial.println(content);   
  }
  else {
    Serial.println(" Access denied");
    delay(3000);
  }
  
 // Wait for signal from Raspberry Pi to rotate servo
  while (!Serial.available()); // Wait until data is available
  char signal = Serial.read(); // Read the signal
  if (signal == 'R') { // Assuming 'R' is the signal to rotate the servo
    rotateServo();
  }
}

void rotateServo() {

for (pos = 2; pos <= 180; pos += 1) {
servo.write(pos);
delay(15); 
}
delay(5000);
for (pos = 180; pos >= 2; pos -= 1) { // goes from 180 degrees to 0 degrees
servo.write(pos); 
delay(15); 
}
}// Stop rotating the servo