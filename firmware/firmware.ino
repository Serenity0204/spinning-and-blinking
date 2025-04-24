const unsigned int LED{17};
// add these
const char S_OK{0xaa};
const char S_ERR{0xff};
// add these
const unsigned int MTR_HI{13};
const unsigned int MTR_LO{14};
int global_state = 0;
int global_rotation_speed = 125;
int global_direction = 1;

void setup()
{
    Serial.begin(9600);
    Serial.onEvent(ARDUINO_HW_CDC_RX_EVENT, on_receive);
    pinMode(LED, OUTPUT);
    // and these+
    pinMode(MTR_HI, OUTPUT);
    pinMode(MTR_LO, OUTPUT);
}

void on_receive(void* event_handler_arg, esp_event_base_t event_base, int32_t event_id, void* event_data)
{
    char state{Serial.read()};
    uint8_t rotation_speed = Serial.read(); // no need for extra temp
    uint8_t direction = Serial.read();

    if (!(state == LOW || state == HIGH))
    {
        // invalid byte received
        // report error
        Serial.write(S_ERR);
        return;
    }

    // update LED with valid state
    if (state)
        global_state = 1;
    else
        global_state = 0;
    global_rotation_speed = rotation_speed;
    global_direction = direction;
    digitalWrite(LED, state);
    Serial.write(S_OK);
}

void turn_off_spin()
{
    analogWrite(MTR_HI, 0);
    analogWrite(MTR_LO, 0);
}

void turn_on_spin(int value, int direction)
{
    if (direction)
    {
        analogWrite(MTR_HI, value);
        analogWrite(MTR_LO, 0);
    }
    else
    {
        analogWrite(MTR_LO, value);
        analogWrite(MTR_HI, 0);
    }
}

void loop()
{
    if (global_state == 1)
        turn_on_spin(global_rotation_speed, global_direction);
    else
        turn_off_spin();
}
