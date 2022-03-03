///////////////////////
// DEVELOPER MODE    //
///////////////////////

#define IS_PRINT false
#define PRINT_DELAY_TIME 100

///////////////////////
// PIN CONFIGURATIONS//
///////////////////////

// Motor Pins
#define dirPin 10
#define stepPin 9

////////////////////
// ENUM VARIABLES //
////////////////////
enum motors {
  MOTORS_FORWARD,
  MOTORS_BACKWARD,
  MOTORS_REVERSE,
  MOTORS_OFF,
  MOTORS_ON,
  MOTORS_STOP,
  MOTORS_RUN,
  MOTORS_RESET
};

enum print_flags{
  PRINT_MOTORS,
  PRINT_RPI,
  PRINT_DISTANCE_SENSORS_FRONT,
  PRINT_DISTANCE_SENSORS_BACKEND
};

enum sensors{
  DISTANCE_SENSORS_FRONT,
  DISTANCE_SENSORS_BACKEND
};

//////////////////////
// SHARED VARIABLES //
//////////////////////

typedef struct kiz_bocegi_code_shared{

  int motor_front_left_speed;
  int motor_front_right_speed;

  int motor_backend_left_speed;
  int motor_backend_right_speed;

  int a1;
  int a2;

  int trigPinOn = 4;  //
  int echoPinOn = 5;  //  >  On sensor
  long sureOn;        //
  long uzaklikOn;     //

  int trigPinArka = 7;  //
  int echoPinArka = 6;  //  >  Arka sensor
  long sureArka;        //
  long uzaklikArka;     //

} kiz_bocegi;

kiz_bocegi g_shared;

void distance_sensors_configurations(){
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(g_shared.trigPinOn, OUTPUT);
  pinMode(g_shared.trigPinArka, OUTPUT);
  pinMode(g_shared.echoPinOn, INPUT);
  pinMode(g_shared.echoPinArka, INPUT);
}

void set_default_sensors_parameters(){
  g_shared.a1 = 0;
  g_shared.a2 = 0;
}

void setup() {

  set_default_sensors_parameters();
  distance_sensors_configurations();

  #if IS_PRINT
    Serial.begin(9600);
    delay(1000);
  #endif
  
}

void motors_status(motors flag){
  // This function is update motors_status.  and then set motor_pins low or high value using  digitalWrite function.

  switch (flag)
  {
  case MOTORS_FORWARD:
    digitalWrite(dirPin, LOW);
    for (int i = 0;; i++) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(3000);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(3000);
    }
    break;
  case MOTORS_BACKWARD:
    digitalWrite(dirPin, HIGH);
    for (int i = 0;; i++) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(3000);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(3000);
    }
    break;
  case MOTORS_REVERSE:

    break;
  case MOTORS_OFF:

    break;
  case MOTORS_ON:

    break;
  case MOTORS_STOP:

    break;
  case MOTORS_RUN:

    break;
  case MOTORS_RESET:

    break;
  default:
    #if IS_PRINT
        Serial.println("Wrong Flag for motors_status(): " + String(flag));
    #endif
    break;
  }
}

int get_distance_sensors_frontEnd(){
  digitalWrite(g_shared.trigPinOn, LOW);         //İlk basta trig pinimizi low durumunda baslatiyoruz
  delayMicroseconds(0.01);                   //5 mikrosaniye bekletiyoruz
  digitalWrite(g_shared.trigPinOn, HIGH);        //Daha sonra pinimizi, ses dalgasi göndermesi icin calistiriyoruz
  delayMicroseconds(0.02);                  //10 mikrosaniye bekletiyoruz
  digitalWrite(g_shared.trigPinOn, LOW);         //Trig pinimizi pasif duruma getiriyoruz
  g_shared.sureOn = pulseIn(g_shared.echoPinOn, HIGH);  //Gonderilen dalganin geri donmesindeki sureyi olcuyor
  g_shared.uzaklikOn = g_shared.sureOn /29.1/2;         //Olctugu sureyi uzakliga ceviriyoruz

  return  g_shared.uzaklikOn;
}

int get_distance_sensors_backEnd(){
  digitalWrite(g_shared.trigPinArka, LOW);         //İlk basta trig pinimizi low durumunda baslatiyoruz
  delayMicroseconds(0.01);                   //5 mikrosaniye bekletiyoruz
  digitalWrite(g_shared.trigPinArka, HIGH);        //Daha sonra pinimizi, ses dalgasi göndermesi icin calistiriyoruz
  delayMicroseconds(0.02);                  //10 mikrosaniye bekletiyoruz
  digitalWrite(g_shared.trigPinArka, LOW);         //Trig pinimizi pasif duruma getiriyoruz
  g_shared.sureArka = pulseIn(g_shared.echoPinArka, HIGH);  //Gonderilen dalganin geri donmesindeki sureyi olcuyor
  g_shared.uzaklikArka = g_shared.sureArka /29.1/2;         //Olctugu sureyi uzakliga ceviriyoruz
  
  return g_shared.uzaklikArka;
}

void print_info(print_flags flag){

  switch(flag){
    case PRINT_MOTORS:
      Serial.println("INFO MOTORS:");
      break;

    case PRINT_RPI:
      Serial.println("INFO PRINT_RPI:");
      break;
      
    case PRINT_DISTANCE_SENSORS_FRONT:
      Serial.print("Uzaklik On "); 
      Serial.print(g_shared.uzaklikOn);
      Serial.print(" cm *** \n");
      break;

    case PRINT_DISTANCE_SENSORS_BACKEND:
      Serial.print("Uzaklik Arka "); 
      Serial.print(g_shared.uzaklikArka);              //Olctugumuz uzakligi seri port ekranina yazdiriyoruz
      Serial.print(" cm *** \n");
      break;
      
  }
  delay(PRINT_DELAY_TIME);

}

void print_info_all(){
    #if IS_PRINT
      print_info(PRINT_MOTORS);
      print_info(PRINT_RPI);
      print_info(PRINT_DISTANCE_SENSORS);
    #endif
}

void set_pin_distance(sensors flag){
  switch (flag)
  {
  case DISTANCE_SENSORS_FRONT:
    if(g_shared.uzaklikOn > 100)                   //200 cm ve üzeri tum uzakliklari 200 cm olarak sabitliyoruz
    g_shared.uzaklikOn = 100;
    break;
  
  case DISTANCE_SENSORS_BACKEND:
    if(g_shared.uzaklikArka > 100)                   //200 cm ve üzeri tum uzakliklari 200 cm olarak sabitliyoruz
    g_shared.uzaklikArka = 100;
    break;
  
  default:
    #if IS_PRINT
        Serial.println("Wrong Flag for set_pin_distance(): " + String(flag));
    #endif
    break;
  }

}

void loop() {
  scenario();
}

void scenario(){
  get_distance_sensors_frontEnd();
  set_pin_distance(DISTANCE_SENSORS_FRONT);

  print_info(PRINT_DISTANCE_SENSORS_FRONT);
  
  get_distance_sensors_backEnd();
  set_pin_distance(DISTANCE_SENSORS_BACKEND);

  print_info(PRINT_DISTANCE_SENSORS_BACKEND);

  
  if(((g_shared.uzaklikOn > 0)&&(g_shared.uzaklikOn <= 5))&&((g_shared.uzaklikArka == 0)||(g_shared.uzaklikArka > 5))){
    motors_status(MOTORS_BACKWARD);
  }
  else if(((g_shared.uzaklikArka > 0)&&(g_shared.uzaklikArka <= 5))&&((g_shared.uzaklikOn == 0)||(g_shared.uzaklikOn > 5))){
    motors_status(MOTORS_FORWARD);
  }
  // deleted else line here. because it was an unnecessary.
  
  if(g_shared.a1 > 0){
    motors_status(MOTORS_BACKWARD);
  }
  else if(g_shared.a2 > 0){
    motors_status(MOTORS_FORWARD);
  }
  
}
