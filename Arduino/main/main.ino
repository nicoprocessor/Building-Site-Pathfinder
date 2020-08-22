#include <SoftwareSerial.h>
#define KEY 10
#define BTLED 7

// SoftwareSerial mySerial(52, 53);
SoftwareSerial mySerial(2, 3); // RX, TX

void setup()
{
    pinMode(KEY, OUTPUT);    // wakeup
    pinMode(BTLED, OUTPUT);  // something has been received (feedback LED)
    digitalWrite(KEY, HIGH); // activate key

    Serial.begin(38400);
    Serial.println("Waiting for AT commands!");
    // SoftwareSerial "COM port"
    mySerial.begin(38400);
}

void loop()
{
    if (mySerial.available())
    {
        digitalWrite(BTLED, HIGH);
        while (mySerial.available())
        {
            // read and append characters read from BT
            command += (char)mySerial.read();
        }

        // send user input
        if (Serial.available())
        {
            delay(10);
            mySerial.write(Serial.read());
        }
    }
}

// void loop() // run over and over
// {
//     if (mySerial.available())
//         Serial.write(mySerial.read());
//     if (Serial.available())
//         mySerial.write(Serial.read());
// }