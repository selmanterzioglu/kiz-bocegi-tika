
#define IS_PRINT true

#define input_pin_1 2
#define input_pin_2 3


int input_pin_1_read, input_pin_2_read;

void setup() {
  #if IS_PRINT
    Serial.begin(9600);
    delay(1000);
  #endif

  pinMode(input_pin_1, INPUT);
  pinMode(input_pin_2, INPUT);
  
}
 
void loop() {
  input_pin_1_read = digitalRead(input_pin_1); // Reading status of Arduino digital Pin
  input_pin_2_read = digitalRead(input_pin_2); // Reading status of Arduino digital Pin

  
  Serial.println("input_pin_1_read: " + String(input_pin_1_read));
  Serial.println("input_pin_2_read: " + String(input_pin_2_read));
   
}
