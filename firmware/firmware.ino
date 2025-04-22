const unsigned int LED{17};
// add these
const char S_OK { 0xaa };
const char S_ERR { 0xff };
// add these
const unsigned int MTR_HI{13};
const unsigned int MTR_LO{14};
int global_state = 0;

void setup() {
    Serial.begin(9600);
    Serial.onEvent(ARDUINO_HW_CDC_RX_EVENT, on_receive);
    pinMode(LED, OUTPUT);
    // and these+
    pinMode(MTR_HI, OUTPUT);
    pinMode(MTR_LO, OUTPUT);
}

void on_receive(void* event_handler_arg, esp_event_base_t event_base, int32_t event_id, void* event_data) {
    // read one byte
    char state { Serial.read() };

    // guard byte is valid LED state
    if (!(state == LOW || state == HIGH)) {
        // invalid byte received
        // report error
        Serial.write(S_ERR);
        return;
    }

    // update LED with valid state
    if(state) global_state = 1;
    else global_state = 0;
    
    digitalWrite(LED, state);
    Serial.write(S_OK);
}

void turn_on_spin()
{
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

void loop() {
    if(global_state == 1) turn_on_spin();
    // Serial.println("Hello, World!");
    // delay(1000);
    // digitalWrite(LED, HIGH); // turn the LED on
    // delay(100); // wait 1 second
    // digitalWrite(LED, LOW); // turn the LED off
    // delay(100); // wait 1 second

}