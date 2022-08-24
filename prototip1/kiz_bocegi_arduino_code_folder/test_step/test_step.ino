// Include the AccelStepper library:
#include <AccelStepper.h>

// Define the AccelStepper interface type:
#define MotorInterfaceType 4

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(MotorInterfaceType, 4, 5, 6, 7);

void setup() {
  // Set the maximum speed in steps per second:
  stepper.setMaxSpeed(1000);
}

void loop() {
  // Set the speed of the motor in steps per second:
  stepper.setSpeed(500);
  // Step the motor with constant speed as set by setSpeed():
  stepper.runSpeed();
}