#!/usr/bin/env python3
import FaBo9Axis_MPU9250
import bluetooth
import time

"""
This file runs on the Server Raspberry Pi at startup.
It creates a Bluetooth Socket that can accept incoming connections.
Once a connection is made, it will send the IMU data as a string over the
Bluetooth connection

"""

def main():

    #Connect to the IMU Sensor
    mpu9250 = FaBo9Axis_MPU9250.MPU9250()

    # Accept incoming client connections and send IMU Data
    # Reopen a connection if there is an error
    while True:
        try:
            server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            port = 2
            server_sock.bind(("",port))
            server_sock.listen(1)

            client_sock,address = server_sock.accept()
            print("Accepted connection from ",address)

            # Set Send Rate
            dataRate = 50 # Hz
            dataInterval = 1000/dataRate

            prevTime = time.time()*1000
            curTime = time.time()*1000

            try:
                while True:
                    curTime = time.time()*1000
                    if (curTime - prevTime > dataInterval):
                        accel = mpu9250.readAccel()
                        gyro = mpu9250.readGyro()
                        mag = mpu9250.readMagnet()

                        megaStringAcc = str(accel['x']) + "_" + str(accel['y']) + "_" + str(accel['z']) + "_"
                        megaStringAng = str(gyro['x']) + "_" + str(gyro['y']) + "_" + str(gyro['z']) + "_"
                        megaStringMag = str(mag['x']) + "_" + str(mag['y']) + "_" + str(mag['z']) + "_"
                        timeString = str(time.time()*1000)

                        superDuperMegaString = megaStringAcc + megaStringAng + megaStringMag + timeString

                        client_sock.send(superDuperMegaString.encode())
                        prevTime = curTime

            except KeyboardInterrupt:
                pass

            client_sock.close()
            server_sock.close()
        except KeyboardInterrupt:
            print('endedbyUser')
            break
        except:
            print('BluetoothError')

if __name__ == '__main__':
    main()
