# Gonio-stepper_Control-command
Raspberry control command script for incidence, emergence and sample plate steppers of a laboratory goniometer.

The control command is divided in two parts: The server part that should be installed on a Raspberry Pi 3/3B board, and the client part that will be installed on the controller computer. The computer and the Raspberry board are connected in USB (serial communication drived by a CP2102 converter ship).

The server part, on the Raspberry, consists in the two scripts "stepper.py" and "steppers-benchmark.py". To turn on the reception of command from the controller computer, please run the script "steppers-benchmark.py".

The client part is the last script "test_send-cmd.py". You can start sending commands by running this script on the computer, after connecting the Raspberry board to the computer and launching first the server part script. The commands interpreted by the server are detailed in the manual "Gonio-Stepper_manual.pdf"

The following figure shows the connection between the different components of the goniometer system:
![Gonio-stepper-diagram](https://user-images.githubusercontent.com/57091666/160671639-dbafd581-07c7-494e-8eab-a2a3594918a5.png)
The microstep driver ships TB660000 are well suited for stepper motors NEMA17, that provide a rather good torque to move the goniometer arms. 
