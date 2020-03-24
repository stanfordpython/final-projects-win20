#!/usr/bin/env python3
import PySimpleGUI as sg
import numpy as np
import queue

from datetime import datetime
from pytz import timezone

from clientActiveEditing_FT import socketConfiguration
import threading

from ShowRepPlot import plotRep

#Defaut State
save = False


"""
eatData

While not in saving state, receives data from the bluetooth
socket and does nothing with it.

Arguments:
    sock -- the bluetooth socket between the server and client

Returns: None

"""
def eatData(sock):
    while boolmethod() == False:
        sock.recv(2048)

"""
boolmethod

Returns True if in Saving state and false otherwise

Arguments: None

Returns:
    save -- a boolean indicating if in the saving state
"""

def boolmethod():
    global save
    return save

"""
getTime

Creates a timestamp that is used in the file naming convention

Arguments: None

Returns:
    timestamp -- a string of formatted timestamp

"""
def getTime():
    pacific = timezone('US/Pacific')
    sa_time = datetime.now(pacific)
    timestamp = sa_time.strftime('%Y-%m-%d_%H_%M_%S')
    return timestamp

"""
saveRep

When in the saving state, recieves the data stream via the bluetooth socket
Parses the data and appends it to a numpy array. When the Saving state is
exited, it saves the array to a temporary storage location.

Arguments:
    sock -- the bluetooth socket between the server and client

Returns:
    storageArray -- The numpy array of data is added to a queue to be accessed
    later by the main thread

"""

def saveRep(sock, values, q):
#    plottingLength = 500
    storageArray = np.zeros([10,0])
    while boolmethod():
        curData = sock.recv(2048)
#        print('saving Rep to TempStorage')
        dataList = curData.decode('utf-8').split('_')
        dataVector = np.asarray(dataList)[0:10]
        dataVector = np.expand_dims(dataVector,axis=1)
        storageArray = np.append(storageArray, dataVector, axis=1)
    print('Rep Complete!')

    #Save the numpy array to a new labeled file.
    data = storageArray
    timestamp = getTime()
    filename = values[0] + '_' + values[1] + '_' + values[2] + '_' + timestamp
    np.save("saveFiles/" + filename, data)
    q.put(storageArray)

"""
main

Calls function to create bluetooth connection and starts a thread to
receive the data.
Defines and creates the GUI window.
Main while loop is the main GUI thread that handles user interaction.
If Start/Stop clicked, state changed to logging, thread starts to recieve and
store data.
If Start/Stop clicked again, state is changed to not logging, and the program
waits until the saved numpy data file has been saved. Restarts thread for
receiving data, and then plots the numpy array for user to visualize.

"""

def main():
    global save
    #Connect to server via bluetooth and start receiving data from the server
    sock = socketConfiguration()
    threading.Thread(target = eatData, args = (sock,) , daemon = True).start()

    #Definethe GUI color and Label Input Boxes
    sg.theme('DarkAmber')
    layout = [  [sg.Text('')],
                [sg.Text('Exercise:'), sg.InputText()],
                [sg.Text('Athlete:'), sg.InputText()],
                [sg.Text('Weight:'), sg.InputText()],
                [sg.Button('Start/Stop Rep')],
                [sg.Button('Exit')] ]

    # Create the GUI Window
    window = sg.Window('Data Logger for Individual Rep Labeling', layout)
    button, values = window.Read()

    # States
    logging = False

    # Main GUI Loop
    while True:
        event, values = window.read()

        # Handle Exit Button
        if event in (None, 'Exit'):	# if user closes window or clicks cancel
            break

        # Handle Start/Stop Button
        if not logging:
            if event in (None, 'Start/Stop Rep'):
                #Start Saving Data from socket
                try:
                    print('Starting Rep!')
                    save = True
                    logging = True
                    q = queue.Queue()
                    threading.Thread(target = saveRep, args = (sock, values, q,) , daemon = True).start()
                except:
                    print('Saving Data Failed')

        elif logging:

            if event in (None, 'Start/Stop Rep'):

                save = False
                logging = False
                q.join() # Wait until queue is filled before moving to next stage
                threading.Thread(target = eatData, args = (sock,) , daemon = True).start()
                data = q.get()
                plotRep(data)

    window.close()

if __name__ == '__main__':
    main()
