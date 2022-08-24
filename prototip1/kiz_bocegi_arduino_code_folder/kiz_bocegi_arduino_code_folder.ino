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
#include <TimerOne.h>
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
#define ECHO_PIN_BACKEND 4  
#define TRIG_PIN_BACKEND 5

// Frontend distance sensor
#define ECHO_PIN_FRONT 6
#define TRIG_PIN_FRONT 7 

////////////////////
// ENUM VARIABLES //
////////////////////
enum motor_status {
  MOTORS_FORWARD,
  MOTORS_BACKWARD,
  MOTORS_STOP
};

enum sensors{
  DISTANCE_SENSORS_FRONT,
  DISTANCE_SENSORS_BACKEND
};

//////////////////////
// SHARED VARIABLES //
//////////////////////

typedef struct kiz_bocegi_code_shared{

  motor_status status;
  
  int route = 1;
  int lock_motor = 0;

  long time_wave_front;   // front wave time value
  long distance_front;    // front distance value

  long time_wave_backend; // backend wave time value
  long distance_backend;  // backend distance value
  
  int motor_speed = 500;  // default value is 500 for motors_speed

  int stop_distance_backend_sensor; // if backend  distance less equal than this value, motors stops 
  int stop_distance_frontend_sensor;// if frontend distance less equal than this value, motors stops

  volatile long ultrasonic_echo_start = 0;

  AccelStepper stepper_motors;

} kiz_bocegi;

kiz_bocegi g_shared;

void distance_sensors_configurations()
{
  pinMode(TRIG_PIN_FRONT, OUTPUT);
  pinMode(TRIG_PIN_BACKEND, OUTPUT);
  pinMode(ECHO_PIN_FRONT, INPUT);
  pinMode(ECHO_PIN_BACKEND, INPUT);

  set_sensor_stop_distance(9, 9);
}

void motor_configurations(){
  g_shared.stepper_motors = AccelStepper(MotorInterfaceType, 8, 9, 10, 11);
  g_shared.stepper_motors.setMaxSpeed(1000);
}

void set_speed(int speed)
{
  g_shared.motor_speed = speed;
}

void set_motor_status(motor_status flag)
{

  // This function is update motors_status. 
  // Then set motor_pins low or high value using  digitalWrite function.

  switch (flag)
  {
    case MOTORS_FORWARD:
        g_shared.stepper_motors.setSpeed(g_shared.motor_speed);
        g_shared.stepper_motors.runSpeed();
      break;
    case MOTORS_BACKWARD:
        g_shared.stepper_motors.setSpeed(-g_shared.motor_speed);
        g_shared.stepper_motors.runSpeed();
      break;

    case MOTORS_STOP:
        g_shared.stepper_motors.stop();
      break;
  }
}

int get_distance(sensors flag)
{
  // This function gets distance value from distance sensors.

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
      trig_pin = TRIG_PIN_BACKEND;
      echo_pin = ECHO_PIN_BACKEND;
      time_wave = &g_shared.time_wave_backend;
      distance = &g_shared.distance_backend;
      break;
  }

  digitalWrite(trig_pin, LOW); 
  delayMicroseconds(10);
  digitalWrite(trig_pin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trig_pin, LOW); 

  *time_wave = pulseIn(echo_pin, HIGH);
  *distance = *time_wave /29.1/2;

}

void threasold_distance_sensors(sensors flag)
{
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
  }
}

void set_sensor_stop_distance(int frontend_distance, int backend_distance)
{
  g_shared.stop_distance_backend_sensor  = backend_distance;
  g_shared.stop_distance_frontend_sensor = frontend_distance;
}

void check_distance_sensors(sensors sensor){
  get_distance(sensor);
  threasold_distance_sensors(sensor);
}

void read_serial(){
  String serial_message = "";

  if (Serial.available() > 0)
  {
      serial_message = Serial.readString();
      serial_message.trim();
  }

  if (serial_message == "motors_forward")
  {
    set_motor_status(MOTORS_FORWARD);
  }
  else if (serial_message == "motors_backward")
  {
    set_motor_status(MOTORS_BACKWARD);
  }
  else if (serial_message == "motors_stop")
  {
    set_motor_status(MOTORS_STOP);
  }
  else if (serial_message == "motors_unlock"){
    g_shared.lock_motor = 0;
  }
  else if (serial_message.indexOf("new_speed: ") != -1)
  {
      serial_message.remove(0, 11);
      int new_speed = serial_message.toInt();
      set_speed(new_speed);
  }

}

void test_code_go_without_sensors()
{
  set_speed(500);
  set_motor_status(MOTORS_FORWARD);
}

void interrupt ()
{
  /*
    https://gelecegiyazanlar.turkcell.com.tr/konu/egitim/arduino-401/zaman-kesmesi-timer-interrupt 
  */
  cli();
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1  = 0;
  OCR1A = 15624;
  TCCR1B |= (1 << WGM12);
  TCCR1B |= (1 << CS12) | (1 << CS10);
  TIMSK1 |= (1 << OCIE1A);

  sei();

}


void setup()
{
  distance_sensors_configurations();
  motor_configurations();
  // interrupt();

  #if IS_PRINT
    Serial.begin(9600);
    delay(1000);
  #endif
}

ISR(TIMER1_COMPA_vect)
{  
  Serial.print("[DEBUG] ");
  Serial.print(" route: " + String(g_shared.route));
  Serial.print(" lock: " + String(g_shared.lock_motor));
  Serial.print(" front: " + String(g_shared.distance_front));
  Serial.println(" backend: " + String(g_shared.distance_backend));

  if(g_shared.route == 1)
    check_distance_sensors(DISTANCE_SENSORS_FRONT);
  
  else if (g_shared.route == -1)
    check_distance_sensors(DISTANCE_SENSORS_BACKEND);

}

void test_print_distance()
{
  check_distance_sensors(DISTANCE_SENSORS_FRONT);
  check_distance_sensors(DISTANCE_SENSORS_BACKEND);

  Serial.print("[DEBUG] ");
  Serial.print(" front: " + String(g_shared.distance_front));
  Serial.println(" backend: " + String(g_shared.distance_backend));

}

void scenario()
{
  //  below lines are functions which calculate distance using distance_sensors and print info to serial monitor.
  

  read_serial();

  if (g_shared.route == 1)
  {
    if (g_shared.distance_front <= g_shared.stop_distance_frontend_sensor)
    {
      set_motor_status(MOTORS_STOP);
      g_shared.route = -1;
      g_shared.lock_motor = 1;

    }
    if (g_shared.lock_motor == 0)
      set_motor_status(MOTORS_FORWARD);
    
  }
  else if (g_shared.route == -1) 
  {
    if (g_shared.distance_backend <= g_shared.stop_distance_backend_sensor)
    {
      set_motor_status(MOTORS_STOP);
      g_shared.route = 1;
      g_shared.lock_motor = 1;
    }
    if (g_shared.lock_motor == 0)
      set_motor_status(MOTORS_BACKWARD);

  }
}

void loop()
{
  // test_print_distance();
  // test_code_go_without_sensors();
  
  scenario();
}

