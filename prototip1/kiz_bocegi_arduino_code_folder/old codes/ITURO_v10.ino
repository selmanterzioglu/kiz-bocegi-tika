///////////////////////
// DEVELOPER OPTIMOTORS_ONS //
///////////////////////
#define IS_PRINT false  // true / false
#define PRINT_DELAY_TIME 100

#define IS_TEST false  // true / false
#define TEST_ANALOG_PIN A1
#define TEST_DELAY_TIME 1000

#define T_SHAPE_NUMBER 4
#define MOTOR_SPEED_MOTORS_LEFT 40
#define MOTOR_SPEED_MOTORS_RIGHT 40

#define LINE_HISTORY_LIMIT 255

#define FADING_TIME 10
#define FADING_FREQUENCY 5
#define FADING_DELAY 20


////////////////////////
// PIN CMOTORS_ONFIGURATIMOTORS_ONS //
////////////////////////
// Line Follow Pins
#define LINE_SENSOR_MOTORS_LEFT_2_PIN A2
#define LINE_SENSOR_MOTORS_LEFT_1_PIN A3
#define LINE_SENSOR_MOTORS_RIGHT_1_PIN A5
#define LINE_SENSOR_MOTORS_RIGHT_2_PIN A4

// Raspberry Pi Communication Pins
#define RPI_RECEIVER_PIN 8 // arduıno send pin
#define RPI_TRANSMITTER_PIN 9 // arduinoReceivePIN

// Motor Driver Pins
#define MOTORS_LEFT_MOTOR_ENABLE_PIN 6
#define MOTORS_RIGHT_MOTOR_ENABLE_PIN 5
#define MOTORS_LEFT_MOTOR_MOTORS_FORWARD_PIN 4
#define MOTORS_LEFT_MOTOR_MOTORS_BACKWARD_PIN 7
#define MOTORS_RIGHT_MOTOR_MOTORS_FORWARD_PIN 2
#define MOTORS_RIGHT_MOTOR_MOTORS_BACKWARD_PIN 3


////////////////////
// ENUM VARIABLES //
////////////////////
enum motors {
  MOTORS_FORWARD,
  MOTORS_BACKWARD,
  MOTORS_REVERSE,
  MOTORS_LEFT,
  MOTORS_RIGHT,
  MOTORS_OFF,
  MOTORS_ON,
  MOTORS_STOP,
  MOTORS_RUN,
  MOTORS_RESET
};

enum line_position {
  LINE_MID,
  LINE_LEFT,
  LINE_RIGHT,
  LINE_T_SHAPE
};

enum p_flag {
  PRINT_MOTORS,
  PRINT_RPI,
  PRINT_T_SHAPE,
  PRINT_LINE_SENSOR,
  PRINT_LINE_INFORMATION
};


//////////////////////
// SHARED VARIABLES //
//////////////////////
typedef struct type_shared_container_struct{

  // Line Sensor Outputs
  int sensor_output_right_2;
  int sensor_output_right_1;
  int sensor_output_left_2;
  int sensor_output_left_1;

  // T Shape Counter
  uint8_t shape_t_counter;
  line_position current_line_position;
  line_position history_of_last_line[LINE_HISTORY_LIMIT];
  int last_line_index;

  // RPI Communication Outputs
  int rpi_transmitter_output;
  int rpi_receiver_output;

  // Motors Information
  int motor_speed_left;
  int motor_speed_right;
  motors last_motors_status;


} t_shared_container;

t_shared_container g_shared;


////////////////////////
// BUILT-IN FUNCTIMOTORS_ONS //
////////////////////////
void setup(){
  line_sensors_pin_configurations();
  rpi_pin_configurations();
  motors_pin_configurations();

  #if IS_PRINT
    Serial.begin( 9600 );
    delay(1000);
  #endif

  #if IS_TEST
    test_pin_configuration(TEST_ANALOG_PIN);
  #endif
}

void loop() {
  //test_fade();

  scenario();
}


//////////////////////
// CUSTOM FUNCTIMOTORS_ONS //
//////////////////////
void scenario() {

  motors_status(MOTORS_RESET);

  // TODO - Add base_state(); function
  for(g_shared.shape_t_counter = 0; g_shared.shape_t_counter < T_SHAPE_NUMBER; g_shared.shape_t_counter++){
    motors_speed_set(MOTOR_SPEED_MOTORS_LEFT, MOTOR_SPEED_MOTORS_RIGHT);
    motors_status(MOTORS_ON);

    #if IS_TEST
      test_pin_print(TEST_ANALOG_PIN, TEST_DELAY_TIME);
    #endif

    read_line_position();
    print_info_all();

    go_for_next_t_shape(true);

    send_to_rpi(HIGH);
    wait_for_rpi(2);

    send_to_rpi(LOW);
  }

  // TODO - Returning algorithm
  // Turn to left side

  motors_status(MOTORS_STOP);
  motors_reverse(MOTORS_LEFT);

  motors_speed_set(MOTOR_SPEED_MOTORS_LEFT, MOTOR_SPEED_MOTORS_RIGHT);
  motors_status(MOTORS_ON);

  read_line_position();
  while(g_shared.sensor_output_right_1 != 1){
    read_line_position();
    print_info_all();
  }
  motors_reverse(MOTORS_LEFT);
  
  //motors_fade(MOTORS_RUN, FADING_TIME, FADING_DELAY, FADING_FREQUENCY);

  for(; g_shared.shape_t_counter > 0; g_shared.shape_t_counter--){

    read_line_position();
    print_info_all();

    go_for_next_t_shape(false);
  }

  motors_fade(MOTORS_STOP, 30, FADING_DELAY, 10);
  motors_status(MOTORS_STOP);

  print_info_all();

  delay(50000);
  wait_for_rpi(2);

}


/*
void turn_back(){
    motors_status(TURN_BACK);

    g_shared.motor_speed_left = motor_speed_left;
    g_shared.motor_speed_right = motor_speed_right;

    analogWrite(MOTORS_LEFT_MOTOR_ENABLE_PIN, motor_speed_left);
    analogWrite(MOTORS_RIGHT_MOTOR_ENABLE_PIN, motor_speed_right);
}
*/

bool wait_for_t_shape(){
  /* A hook to read line which waits for t shape pattern */
  read_line_position();
  while(g_shared.current_line_position != LINE_T_SHAPE){
    read_line_position();
    print_info_all();

    line_correction();
  /*
   * TODOs - Controlling and actioning algorithm
   */

  }
  return true;
}


void go_for_next_t_shape(bool is_stop_active){

  wait_for_t_shape();

  if(is_stop_active)
    motors_fade(MOTORS_STOP, FADING_TIME, FADING_DELAY, FADING_FREQUENCY);

  #if IS_PRINT
    print_info(PRINT_MOTORS);
  #endif

}


void read_line_sensors(){
  /*
    Reads Sensor outputs and put them into shared area
  */

  g_shared.sensor_output_right_2  = digitalRead(LINE_SENSOR_MOTORS_RIGHT_2_PIN);
  g_shared.sensor_output_left_1   = digitalRead(LINE_SENSOR_MOTORS_LEFT_1_PIN);
  g_shared.sensor_output_left_2   = digitalRead(LINE_SENSOR_MOTORS_LEFT_2_PIN);
  g_shared.sensor_output_right_1  = digitalRead(LINE_SENSOR_MOTORS_RIGHT_1_PIN);

}


void read_line_position(){

  read_line_sensors();

  /*
    * This Pattern Set is used to focus MID
  */
  // T SHAPE PATTERN
  if(g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 1 )

      g_shared.current_line_position = LINE_T_SHAPE;

  // MID PATTERN
  if((g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_MID;


  // MOTORS_LEFT PATTERN
  if((g_shared.sensor_output_left_2 == 1 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ) ||
      (g_shared.sensor_output_left_2 == 1 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ) ||
      (g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_LEFT;


  // MOTORS_RIGHT PATTERN
  if((g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 1 ) ||
      (g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_RIGHT;

  /*
   * This Pattern Set is used to focus left 1 sensor
   * 
  // T SHAPE PATTERN
  if((g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 1) || 
    (g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 1))
      g_shared.current_line_position = LINE_T_SHAPE;

  // MID PATTERN
  if((g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_MID;


  // MOTORS_LEFT PATTERN
  if((g_shared.sensor_output_left_2 == 1 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ) ||
      (g_shared.sensor_output_left_2 == 1 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_LEFT;


  // MOTORS_RIGHT PATTERN
  if((g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 1 ) ||
      (g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_RIGHT;
  */
}


/*
void read_line_position(){
  /*
   * TODO - Sensors should be placed like left1 and left2 should be left of line, right1 and right2 should be right of line and none of them on the line.
   * /

  read_line_sensors();

  // T SHAPE PATTERN
  if(g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 1 )
      g_shared.current_line_position = LINE_T_SHAPE;


  // MID PATTERN
  if(g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 )
    g_shared.current_line_position = LINE_MID;

  * /

  read_line_sensors();


  // T SHAPE PATTERN
  if((g_shared.sensor_output_left_2 == 1 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 1 ) ||
      (g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 1 ) ||
      (g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 1 ))

      g_shared.current_line_position = LINE_T_SHAPE;

  // MID PATTERN
  if((g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ) ||
    (g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_MID;


  // MOTORS_LEFT PATTERN
  if((g_shared.sensor_output_left_2 == 1 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ) ||
      (g_shared.sensor_output_left_2 == 1 && g_shared.sensor_output_left_1 == 1 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_LEFT;


  // MOTORS_RIGHT PATTERN
  if((g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 0 && g_shared.sensor_output_right_2 == 1 ) ||
      (g_shared.sensor_output_left_2 == 0 && g_shared.sensor_output_left_1 == 0 && g_shared.sensor_output_right_1 == 1 && g_shared.sensor_output_right_2 == 0 ))
      g_shared.current_line_position = LINE_RIGHT;
}
*/


void line_correction(){
  //g_shared.history_of_last_line

  read_line_position();

  if(g_shared.current_line_position == LINE_RIGHT)
      motors_left(MOTOR_SPEED_MOTORS_LEFT + round(MOTOR_SPEED_MOTORS_LEFT % 25));
  else if(g_shared.current_line_position == LINE_LEFT)
      motors_right(MOTOR_SPEED_MOTORS_RIGHT + round(MOTOR_SPEED_MOTORS_RIGHT % 25));
  else{
    motors_speed_set(MOTOR_SPEED_MOTORS_LEFT, MOTOR_SPEED_MOTORS_RIGHT);
  }

  /*
  if(g_shared.current_line_position == LINE_RIGHT)
      motors_right(MOTOR_SPEED_MOTORS_RIGHT - round(MOTOR_SPEED_MOTORS_RIGHT % 25));
  else if(g_shared.current_line_position == LINE_LEFT)
      motors_left(MOTOR_SPEED_MOTORS_LEFT - round(MOTOR_SPEED_MOTORS_LEFT % 25));
  else{
    motors_speed_set(MOTOR_SPEED_MOTORS_LEFT, MOTOR_SPEED_MOTORS_RIGHT);
  }
  */
}


void read_rpi_pin(){
  g_shared.rpi_transmitter_output = digitalRead(RPI_TRANSMITTER_PIN);
  g_shared.rpi_receiver_output    = digitalRead(RPI_RECEIVER_PIN);
}


void write_rpi_pin(bool transmitter){
  g_shared.rpi_transmitter_output = transmitter;
  digitalWrite(RPI_TRANSMITTER_PIN, transmitter);
}


bool wait_for_rpi(int test_flag){
  /*
   * A hook for rpi receiver output which waits for HIGH (1) from pin
   */
  while(g_shared.rpi_receiver_output != HIGH){
    read_rpi_pin();
    #if IS_PRINT
      print_info(PRINT_RPI);
    #endif
    if(test_flag > 1){
      delay(1000);
      g_shared.rpi_receiver_output = HIGH;
    }
  }
  return true;
}


void send_to_rpi(bool flag){
  switch(flag){
    case false:
      write_rpi_pin(LOW);
      break;
    case true:
      write_rpi_pin(HIGH);
      break;
    default:

      #if IS_PRINT
        Serial.println("ERROR Wrong Flag for RPI Transmitter: " + String(flag));
      #endif
      // flag = flag;
      break;
  }
}


void motors_status(motors flag){
  switch(flag){
    case MOTORS_FORWARD:
      digitalWrite(MOTORS_LEFT_MOTOR_MOTORS_FORWARD_PIN, HIGH);
      digitalWrite(MOTORS_LEFT_MOTOR_MOTORS_BACKWARD_PIN, LOW);

      digitalWrite(MOTORS_RIGHT_MOTOR_MOTORS_FORWARD_PIN, HIGH);
      digitalWrite(MOTORS_RIGHT_MOTOR_MOTORS_BACKWARD_PIN, LOW);
      break;
    case MOTORS_BACKWARD:
      digitalWrite(MOTORS_LEFT_MOTOR_MOTORS_FORWARD_PIN, LOW);
      digitalWrite(MOTORS_LEFT_MOTOR_MOTORS_BACKWARD_PIN, HIGH);

      digitalWrite(MOTORS_RIGHT_MOTOR_MOTORS_FORWARD_PIN, LOW);
      digitalWrite(MOTORS_RIGHT_MOTOR_MOTORS_BACKWARD_PIN, HIGH);
      break;
    case MOTORS_OFF:
      motors_speed_set(LOW, LOW);
      //analogWrite(MOTORS_LEFT_MOTOR_ENABLE_PIN, LOW);
      //digitalWrite(MOTORS_LEFT_MOTOR_MOTORS_FORWARD_PIN, LOW);
      //digitalWrite(MOTORS_LEFT_MOTOR_MOTORS_BACKWARD_PIN, LOW);

      //analogWrite(MOTORS_RIGHT_MOTOR_ENABLE_PIN, LOW);
      //digitalWrite(MOTORS_RIGHT_MOTOR_MOTORS_FORWARD_PIN, LOW);
      //digitalWrite(MOTORS_RIGHT_MOTOR_MOTORS_BACKWARD_PIN, LOW);
      break;
    case MOTORS_ON:
      motors_speed_set(g_shared.motor_speed_left, g_shared.motor_speed_right);
      //analogWrite(MOTORS_LEFT_MOTOR_ENABLE_PIN, MOTOR_SPEED_MOTORS_LEFT);
      //analogWrite(MOTORS_RIGHT_MOTOR_ENABLE_PIN, MOTOR_SPEED_MOTORS_RIGHT);
      break;
    case MOTORS_REVERSE:
      motors_reverse(MOTORS_LEFT);
      motors_reverse(MOTORS_RIGHT);
      break;
    case MOTORS_RESET:
      motors_status(MOTORS_FORWARD);
      //motors_speed_set(0, 0);
      motors_status(MOTORS_OFF);
      break;
    case MOTORS_STOP:
      #if IS_PRINT
        Serial.println("Motors Stopped");
      #endif
      motors_status(MOTORS_OFF);
      break;
    case MOTORS_LEFT:
      #if IS_PRINT
        Serial.println("No need MOTORS_LEFT flag for motors_status(): " + String(flag));
      #endif
      break;
    case MOTORS_RIGHT:
      #if IS_PRINT
        Serial.println("No need MOTORS_RIGHT flag for motors_status(): " + String(flag));
      #endif
      break;
    default:
      #if IS_PRINT
        Serial.println("Wrong Flag for motors_status(): " + String(flag));
      #endif
      break;
  }

  g_shared.last_motors_status = flag;
}


void motors_speed_set(int motor_speed_left, int motor_speed_right){

  // Negative speed control
  if(motor_speed_left < 0)
    motor_speed_left = 0;
  if(motor_speed_right < 0)
    motor_speed_right = 0;

  // Shared Area Sync
  g_shared.motor_speed_left = motor_speed_left;
  g_shared.motor_speed_right = motor_speed_right;

  analogWrite(MOTORS_LEFT_MOTOR_ENABLE_PIN, motor_speed_left);
  analogWrite(MOTORS_RIGHT_MOTOR_ENABLE_PIN, motor_speed_right);
}


void motors_left(int motor_speed_left){

  // Shared Area Sync
  g_shared.motor_speed_left = motor_speed_left;
  
  analogWrite(MOTORS_LEFT_MOTOR_ENABLE_PIN, motor_speed_left);
}


void motors_right(int motor_speed_right){

  // Shared Area Sync
  g_shared.motor_speed_right = motor_speed_right;
  
  analogWrite(MOTORS_RIGHT_MOTOR_ENABLE_PIN, motor_speed_right);
}


void to_right(int motor_speed_left){
  motors_speed_set(motor_speed_left, motor_speed_left - motor_speed_left * 0.5);
  //motors_left(motor_speed_left);
  //motors_right(motor_speed_left - motor_speed_left * 0.5);
}


void to_left(int motor_speed_right){
  motors_speed_set(motor_speed_right - motor_speed_right * 0.5, motor_speed_right);
  //motors_left(motor_speed_right - motor_speed_right * 0.5 );
  //motors_right(motor_speed_right);
}


void motors_stop(int stop_after_delay_time){
  if (stop_after_delay_time > 0)
  {
    delay(stop_after_delay_time);
  }
  motors_status(MOTORS_OFF);
}


void motors_fade(motors motor_flag, int fading_time, int fading_delay, int fading_frequency){
  int delay_counter;

  if(motor_flag == MOTORS_STOP){
    fading_frequency = -fading_frequency;
  }
  // else it is positive, no need action

  int motor_speed_left;
  int motor_speed_right;

  // Fading loop
  for(delay_counter = 0; delay_counter < fading_time; delay_counter++){

    motor_speed_left = g_shared.motor_speed_left + fading_frequency;
    motor_speed_right = g_shared.motor_speed_right + fading_frequency;

    // 0 speed controls. If below than fading_frequency, make it 0 (fading_frequency - fading_frequency = 0)
    if(motor_speed_left < 0){
      motor_speed_left = 0;
    }
    if(motor_speed_right < 0){
      motor_speed_left = 0;
    }

    // 255 speed controls. If above than 255 - fading_frequency, make it 255 (g_shared.motors_speed + fading_frequency = (MAX)255 )
    if(motor_speed_left > 255){
      motor_speed_left = 255;
    }
    if(motor_speed_right > 255){
      motor_speed_right = 255;
    }

    motors_speed_set(motor_speed_left, motor_speed_right);
    delay(fading_delay);

    // If both equals 0 or 255, finish the fading
    if( (motor_speed_left == 0 && motor_speed_right == 0) || (motor_speed_left == 255 && motor_speed_right == 255))
      break;

    } // For Loop
}


void motors_reverse(motors revers_flag){
  /*
   * Reversing only 1 motor at a time
   */
  if(revers_flag == MOTORS_LEFT){
    digitalWrite(MOTORS_LEFT_MOTOR_MOTORS_FORWARD_PIN, (digitalRead(MOTORS_LEFT_MOTOR_MOTORS_FORWARD_PIN) ? LOW : HIGH) );
    digitalWrite(MOTORS_LEFT_MOTOR_MOTORS_BACKWARD_PIN, (digitalRead(MOTORS_LEFT_MOTOR_MOTORS_BACKWARD_PIN) ? LOW : HIGH) );
  }
  else if(revers_flag == MOTORS_RIGHT){
    digitalWrite(MOTORS_RIGHT_MOTOR_MOTORS_FORWARD_PIN, (digitalRead(MOTORS_RIGHT_MOTOR_MOTORS_FORWARD_PIN) ? LOW : HIGH) );
    digitalWrite(MOTORS_RIGHT_MOTOR_MOTORS_BACKWARD_PIN, (digitalRead(MOTORS_RIGHT_MOTOR_MOTORS_BACKWARD_PIN) ? LOW : HIGH) );
  }
}


void motors_go_back(int motor_speed_left, int motor_speed_right){

  g_shared.motor_speed_left = motor_speed_left;
  g_shared.motor_speed_right = motor_speed_right;

  motors_status(MOTORS_BACKWARD);
  motors_speed_set(motor_speed_left, motor_speed_right);
}

/*
void motors_return(motors revers_flag){
  /*
   * Reversing only 1 motor at a time
   * /

  g_shared.motor_speed_left = motor_speed_left;
  g_shared.motor_speed_right = motor_speed_right;

  motors_reverse(revers_flag);

  analogWrite(MOTORS_LEFT_MOTOR_ENABLE_PIN, motor_speed_left);
  analogWrite(MOTORS_RIGHT_MOTOR_ENABLE_PIN, motor_speed_right);
}
*/


void line_sensors_pin_configurations(){
  pinMode(LINE_SENSOR_MOTORS_LEFT_1_PIN, INPUT);
  pinMode(LINE_SENSOR_MOTORS_LEFT_2_PIN, INPUT);
  pinMode(LINE_SENSOR_MOTORS_RIGHT_1_PIN, INPUT);
  pinMode(LINE_SENSOR_MOTORS_RIGHT_2_PIN, INPUT);
}


void rpi_pin_configurations(){
  pinMode(RPI_RECEIVER_PIN, INPUT);
  pinMode(RPI_TRANSMITTER_PIN, OUTPUT);

  digitalWrite(RPI_RECEIVER_PIN, LOW);
  digitalWrite(RPI_TRANSMITTER_PIN, LOW);
}


void motors_pin_configurations(){
  pinMode(MOTORS_LEFT_MOTOR_MOTORS_FORWARD_PIN, OUTPUT);
  pinMode(MOTORS_LEFT_MOTOR_MOTORS_BACKWARD_PIN, OUTPUT);
  pinMode(MOTORS_RIGHT_MOTOR_MOTORS_FORWARD_PIN, OUTPUT);
  pinMode(MOTORS_RIGHT_MOTOR_MOTORS_BACKWARD_PIN, OUTPUT);

  motors_status(MOTORS_FORWARD);
  motors_status(MOTORS_OFF);
}


#if IS_PRINT
  void print_info(p_flag flag){
    switch(flag){
      case PRINT_MOTORS:
        Serial.println("INFO MOTORS\t| Speed - Left:" + String(g_shared.motor_speed_left) + " Right:" + String(g_shared.motor_speed_right) + " | Last Motors Status: " + get_last_motors_status() );
        break;
      case PRINT_RPI:
        Serial.println("INFO RPi\t| Receiver:" + String(g_shared.rpi_receiver_output) + " - Transmitter:" + String(g_shared.rpi_transmitter_output) );
        break;
      case PRINT_T_SHAPE:
        Serial.println("INFO VARIABLE\t| T Shape Counter:" + String(g_shared.shape_t_counter));
        break;
      case PRINT_LINE_SENSOR:
        Serial.println("INFO LINE SENSOR\t| Right2:" + String(g_shared.sensor_output_right_2) + " - Right1:" + String(g_shared.sensor_output_right_1) + " - Left1:" + String(g_shared.sensor_output_left_1) + " - Left2:" + String(g_shared.sensor_output_left_2) );
        break;
      case PRINT_LINE_INFORMATION:
        Serial.println("Current Line Position (" + String(g_shared.current_line_position) + "): " + get_current_line_position() );
        break;
    }
    delay(PRINT_DELAY_TIME);
  }


char * get_current_line_position(){
  switch(g_shared.current_line_position){
    case LINE_MID:
      return "LINE_MID";
    case LINE_LEFT:
      return "LINE_LEFT";
    case LINE_RIGHT:
      return "LINE_RIGHT";
    case LINE_T_SHAPE:
      return "LINE_T_SHAPE";
  }
}


char * get_last_motors_status(){
  switch(g_shared.last_motors_status){
    case MOTORS_FORWARD:
      return "MOTORS_FORWARD";
    case MOTORS_BACKWARD:
      return "MOTORS_BACKWARD";
    case MOTORS_LEFT:
      return "MOTORS_LEFT";
    case MOTORS_RIGHT:
      return "MOTORS_RIGHT";
    case MOTORS_ON:
      return "MOTORS_ON";
    case MOTORS_OFF:
      return "MOTORS_OFF";
    case MOTORS_STOP:
      return "MOTORS_STOP";
    case MOTORS_RUN:
      return "MOTORS_RUN";
    case MOTORS_RESET:
      return "MOTORS_RESET";
  }
}
#endif

void print_info_all(){

    #if IS_PRINT
      read_rpi_pin();
      read_line_position();

      print_info(PRINT_MOTORS);
      print_info(PRINT_RPI);
      print_info(PRINT_T_SHAPE);
      print_info(PRINT_LINE_SENSOR);
      print_info(PRINT_LINE_INFORMATION);
    #endif
}


#if IS_TEST
  void test_pin_configuration(int analog_pin){
    pinMode(analog_pin, INPUT);
  }

  int test_pin_read(int test_analog_pin){
    return analogRead(test_analog_pin);
  }

  int test_pin_print(int test_analog_pin, int delay_time){
    if(delay_time > 0)
      delay(delay_time);
    Serial.println("TEST PIN()" + String(test_analog_pin) + " OUTPUT:" + String(test_pin_read(test_analog_pin)));
  }

  void test_fade(){
    ///*
    //motors_status(MOTORS_ON);
    //motors_speed_set(MOTOR_SPEED_MOTORS_LEFT, MOTOR_SPEED_MOTORS_RIGHT);
    motors_status(MOTORS_OFF);

    int fading_time = 50;
    int fading_frequency = 5;
    int fading_delay = 200;

    while(1){
      // Fade Run TEST
      //motors_status(MOTORS_OFF);
      print_info(PRINT_MOTORS);

      //motors_status(MOTORS_ON);
      //print_info(PRINT_MOTORS);

      motors_fade(MOTORS_RUN, fading_time, fading_delay, fading_frequency);
      print_info(PRINT_MOTORS);

      //motors_status(MOTORS_OFF);
      delay(1500);

      // Fade Stop TEST
      //motors_status(MOTORS_ON);
      //motors_speed_set(255, 255);
      print_info(PRINT_MOTORS);

      //motors_status(MOTORS_ON);
      //print_info(PRINT_MOTORS);

      motors_fade(MOTORS_STOP, fading_time, fading_delay, fading_frequency);
      print_info(PRINT_MOTORS);

      //motors_status(MOTORS_OFF);
      delay(1500);
      /*
      motors_status(MOTORS_ON);
      motors_fade(MOTORS_STOP, fading_time, fading_delay, fading_frequency);
      print_info(PRINT_MOTORS);
      delay(1500);
      motors_status(MOTORS_OFF);
      */
    }


    //motors_status(MOTORS_OFF);

    //*/
  }
#endif
