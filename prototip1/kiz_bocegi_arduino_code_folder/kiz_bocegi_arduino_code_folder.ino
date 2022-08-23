/*
  Asagidaki kodlar'da zamaninda yuksek tecrubeleriyle bize desteklerini esirgemeyen Sn. M. Said Bilgehan'in buyuk  katkileri bulunmaktadir. 
  Bu katki, emek ve destekleri sebebiyle 
  Sn. Bilgehan anisina aracimizin gomulu kodlarinda ismini saygiyla aniyor ve yasatiyoruz...
  gitlab.com/msaidbilgehan
*/

/*
  For motors control, using this tutorial:
  https://www.makerguides.com/l298n-stepper-motor-arduino-tutorial/

*/

///////////////////////
//      LIBRARY      //
///////////////////////
#include <AccelStepper.h>

///////////////////////
// DEVELOPER MODE    //
///////////////////////

#define IS_PRINT true
#define PRINT_DELAY_TIME 100

///////////////////////
// PIN CONFIGURATIONS//
///////////////////////

// Motor Pins
#define MotorInterfaceType 4 // for l298n : "4" 

// Backend distance sensor
#define TRIG_PIN_BACKEND 5
#define ECHO_PIN_BACKEND 4  

// Frontend distance sensor
#define TRIG_PIN_FRONT 6 
#define ECHO_PIN_FRONT 7

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
  MOTORS,
  DISTANCE_FRONT,
  DISTANCE_BACKEND
};

enum sensors{
  DISTANCE_SENSORS_FRONT,
  DISTANCE_SENSORS_BACKEND
};

//////////////////////
// SHARED VARIABLES //
//////////////////////

typedef struct kiz_bocegi_code_shared{

  long time_wave_front;   // front wave time value
  long distance_front;    // front distance value

  long time_wave_backend; // backend wave time value
  long distance_backend;  // backend distance value

  // int a1, a2;

  int stop_distance_backend_sensor;
  int stop_distance_frontend_sensor;

  AccelStepper stepper_motors;


} kiz_bocegi;

kiz_bocegi g_shared;

void distance_sensors_configurations(){
  pinMode(TRIG_PIN_FRONT, OUTPUT);
  pinMode(TRIG_PIN_BACKEND, OUTPUT);
  pinMode(ECHO_PIN_FRONT, INPUT);
  pinMode(ECHO_PIN_BACKEND, INPUT);
}

void motor_configurations(){
  g_shared.stepper_motors = AccelStepper(MotorInterfaceType, 4, 5, 6, 7);
}

void setup(){

  distance_sensors_configurations();
  motor_configurations();

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

    break;
  case MOTORS_BACKWARD:

    break;

  case MOTORS_STOP:

    break;

  default:
    #if IS_PRINT
        Serial.print("Wrong Flag for motors_status(): " + String(flag) + "\n");
    #endif
    break;
  }
}

int get_distance(sensors flag)
{
  // This function is get distance value from distance sensors

  int trig_pin, echo_pin;
  long *time_wave, *distance;

  switch (flag)
  {
    case DISTANCE_SENSORS_FRONT:
      trig_pin = TRIG_PIN_FRONT;
      echo_pin = ECHO_PIN_FRONT;
      time_wave = &g_shared.time_wave_front;
      distance = &g_shared.distance_front;
      break;
    case DISTANCE_SENSORS_BACKEND:
      trig_pin = TRIG_PIN_FRONT;
      echo_pin = ECHO_PIN_FRONT;
      time_wave = &g_shared.time_wave_backend;
      distance = &g_shared.distance_backend;
      break;
  }

  digitalWrite(trig_pin, LOW); 
  delayMicroseconds(0.01);
  digitalWrite(trig_pin, HIGH); 
  delayMicroseconds(0.02);
  digitalWrite(trig_pin, LOW); 
  *time_wave = pulseIn(echo_pin, HIGH);
  *distance = *time_wave /29.1/2;

}

void print_info(print_flags flag){
  // This function print all info variables to serial monitor. 
  // You must choose which variable write to serial monitor using print_flags .
  #if IS_PRINT

    switch(flag){
      case MOTORS:
        Serial.print("INFO MOTORS:\n");
        break;

      case DISTANCE_FRONT:
        Serial.println("Uzaklik On: " + String(g_shared.distance_front)); 
        break;

      case DISTANCE_BACKEND:
        Serial.println("Uzaklik Arka: " + String(g_shared.distance_backend)); 
        break;
        
    }
    delay(PRINT_DELAY_TIME);

  #endif

}

void print_info_all(){
  //  if IS_PRINT is true, this function writes all variables to serial monitor.

    #if IS_PRINT
      print_info(MOTORS);
      print_info(DISTANCE_FRONT);
      print_info(DISTANCE_BACKEND);
    #endif
}

void threasold_distance_sensors(sensors flag){
  // if distance value is greater than 200, we set distance value to 200.
  
  switch (flag)
  {
  case DISTANCE_SENSORS_FRONT:
    if(g_shared.distance_front > 200)
      g_shared.distance_front = 200;
    break;
  
  case DISTANCE_SENSORS_BACKEND:
    if(g_shared.distance_backend > 200)  
      g_shared.distance_backend = 200;
    break;
  
  default:
    #if IS_PRINT
        Serial.print("Wrong Flag for set_pin_distance(): " + String(flag) + "\n");
    #endif
    break;
  }

}

void test_code_go_without_sensors(){
  
  
}

void loop() {
  
  test_code_go_without_sensors();
  
  // scenario();
}

void set_sensor_stop_distance(int frontend_distance, int backend_distance){
  g_shared.stop_distance_backend_sensor  = backend_distance;
  g_shared.stop_distance_frontend_sensor = frontend_distance;
}

int get_frontend_distance(){
  return g_shared.distance_front;
}
int get_backend_distance(){
  return g_shared.distance_backend;
}

void scenario(){
  //  below lines are functions which calculate distance using distance_sensors and print info to serial monitor.
  
  threasold_distance_sensors(DISTANCE_SENSORS_FRONT);
  threasold_distance_sensors(DISTANCE_SENSORS_BACKEND);

  if (Serial.find("forward")){
    String data = Serial.readString();
    motors_status(MOTORS_FORWARD);
  }
  else if (Serial.find("backward")){
    String data = Serial.readString();
    motors_status(MOTORS_BACKWARD);
  }

}
