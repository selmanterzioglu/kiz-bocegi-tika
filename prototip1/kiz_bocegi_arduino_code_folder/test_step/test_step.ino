// Include the Arduino Stepper Library
#include <Stepper.h>

// Number of steps per output rotation
const int stepsPerRevolution = 200;

// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 4, 5, 6, 7);


void setup()
{
    Serial.begin(9600);
	myStepper.setSpeed(100);
}

void loop() 
{
    myStepper.step(stepsPerRevolution);


}