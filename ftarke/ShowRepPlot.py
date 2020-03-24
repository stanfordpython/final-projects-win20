import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

"""
plotRep

Takes in a numpy array and plots the collected data for the user to visualize.
Three plots are made with 3 data streams each (Acclerometer, Gyroscope,
Magnetometer)

Arguments:
    repArray -- A numpy array that contains the 9 data streams and time

Returns:None

"""

def plotRep(repArray):

    style.use('fivethirtyeight')
    fig, (accPlot,angPlot,magPlot) = plt.subplots(nrows=1,ncols=3)

    print("repArray.shape: " + str(repArray.shape))

    try:
        plotArrayFloat = np.array([[float(x) for x in y] for y in repArray])

        time = plotArrayFloat[9,:]

        axData = plotArrayFloat[0,:]
        ayData = plotArrayFloat[1,:]
        azData = plotArrayFloat[2,:]

        gxData = plotArrayFloat[3,:]
        gyData = plotArrayFloat[4,:]
        gzData = plotArrayFloat[5,:]

        mxData = plotArrayFloat[6,:]
        myData = plotArrayFloat[7,:]
        mzData = plotArrayFloat[8,:]

        accPlot.clear()
        accPlot.plot(time, axData)
        accPlot.plot(time, ayData)
        accPlot.plot(time, azData)

        angPlot.clear()
        angPlot.plot(time, gxData)
        angPlot.plot(time, gyData)
        angPlot.plot(time, gzData)

        magPlot.clear()
        magPlot.plot(time, mxData)
        magPlot.plot(time, myData)
        magPlot.plot(time, mzData)

        accPlot.title.set_text('Accelerometer')
        angPlot.title.set_text('Gyroscope')
        magPlot.title.set_text('Magnetometer')

        plt.show()

        plt.close()

    except:
        print("Failed to Generate Plot")
