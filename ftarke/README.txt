CS41 README
Weight Room Data Logger
Franklin Tarke
franklin.tarke@gmail
5307014779

Credits: Thanks to Wilson Ruotolo for helping with the hardware setup, debugging,
and design of the system

Project Description:
Create a data logger system that stores labeled IMU data into numpy files
that can be fed into a machine learning model.

Features:
1.	Server Side
  a.	Server Code runs on Pi Startup
  b.	Catches disconnect errors and doesn't crash
  c.	Read data from GPIO, Sends data over Bluetooth Socket
2.	Client Side
  a.	GUI that takes in user input for labeling/saving data
  b.	User input causes recording of data between time interval of button press
  c.	Data is saved to file with proper naming convention
  d.  Plot of data is shown to user for data visualization
3.	Feature Extraction and Machine Learning
  a.	Organize data to be put into a model
  b.	Create new features by manipulating data i.e. integration etc.


Python Files:
(Client)
  guiTesting_FT.py -- Main Program File that the user runs on their laptop
  clientActiveEditing_FT.py -- Contains a method for connecting to the server via
  a Bluetooth Socket
  ShowRepPlot.py -- Contains a method that plots the IMU data for visualization

  featureExtraction.py -- takes in user input for the name of a .npy file
  created by guiTesting_FT.py, creates a new .npy file that modifies the data
  to add new features (Velocity from integrated acceleration)

(Server)
serverFinal.py -- Main Program File that runs on raspberry pi boot

Python Libraries:
Everything was done using Python 3.8

(Client - Linux Laptop or another Raspberry Pi)
  PySimpleGUI
  numpy
  queue
  datetime
  pytz
  threading
  Pybluez -- Seems to only work on Linux systems. Ran into many errors when
  attempting to use on OSX.
  Follow these instructions: https://gist.github.com/lexruee/fa2e55aab4380cf266fb
  bluetooth (via Pybluez)
  matplotlib

(Server - Raspberry Pi)
  Pybluez -- Seems to only work on Linux systems. Ran into many errors when
  attempting to use on OSX.
  Follow these instructions: https://gist.github.com/lexruee/fa2e55aab4380cf266fb
  time
  FaBo9Axis_MPU9250 -- Library must be modified for compatibility with Python 3
  Remove or comment Python 2 print statements from the end of the library file.

Raspberry Pi Setup:
- To Run serverFinal.py on boot edit this File: sudo nano /etc/profile
  Add "sudo python /home/pi/serverFinal.py" to the end of the file.
- Once ssh'd into raspberry pi, may need to use bluetoothctl to turn on the
bluetooth module and trust the Bluetooth hardware address of the client, and vice versa.
use commands :"list" to see your device's Bluetooth hardware address, and
"trust <Hardware Address you want to communicate with>" to trust the other device.
- IMU -> Pi Wiring
  VCC -> Pin 1
  GND -> Pin 6
  SCL -> Pin 5
  SDA -> Pin 3
