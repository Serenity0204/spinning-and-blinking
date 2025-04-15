const unsigned int LED{17};
// add these
const unsigned int MTR_HI{13};
const unsigned int MTR_LO{14};

void setup() {
    pinMode(LED, OUTPUT);
    // and these+
    pinMode(MTR_HI, OUTPUT);
    pinMode(MTR_LO, OUTPUT);
}

void loop() {
    digitalWrite(LED, HIGH); // turn the LED on
    delay(100); // wait 1 second
    digitalWrite(LED, LOW); // turn the LED off
    delay(100); // wait 1 second

    for(int i = 0; i <= 255; ++i)
    {
        analogWrite(MTR_HI, i);
        analogWrite(MTR_LO, 0);
        delay(10);
    }

    for(int i = 255; i >= 0; --i)
    {
        analogWrite(MTR_HI, i);
        analogWrite(MTR_LO, 0);
        delay(10);
    }

 
    for(int i = 0; i <= 255; ++i)
    {
        analogWrite(MTR_HI, 0);
        analogWrite(MTR_LO, i);
        delay(10);
    }   

    for(int i = 255; i >= 0; --i)
    {
        analogWrite(MTR_HI, 0);
        analogWrite(MTR_LO, i);
        delay(10);
    }
}