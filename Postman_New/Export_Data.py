#!/usr/bin/python3

import openpyxl
import config


def export(wb, sensorNames, sensorData, timestampBegin, timestampEnd, sampleRateDes, filePath='./defaultFileName'):
    '''
    main method of Export_Data module

    takes in 
    - sensorNames: a list [] of the sensors to be exported and
    - sensorData: a list of lists [[sensor1Data],[sensor2Data],[sensor3Data]] of all data falling between the given timestamps
    - timeStampBegin: timestamp of session start
    - timeStampEnd: timestamp of session end
    - sampleRateDes: desired sample rate of the outputted data
    - filePath: path/name of Excel file to save exported data to

    executes procedure
    - calls processData
    - generate timestamp array for y axis label
    - open new Excel Workbook and Sheet to write to
    - place header (x axis label) row with sensor id's
    - uses a loop structure to place data in Excel sheet
    - create fileName with .xlsx
    - save notebook

    no return value
    '''

    #####################################
    # doing Excel stuff with fake data

    dummyNames = ['a', 'b', 'c', 'd', 'e']
    dummyList = [[] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            dummyList[i][j] = str(10*i + j)

    processedData = dummyList
    #####################################

    # processedData = processData(sensorData)

    wb = openpyxl.Workbook()
    ws = wb.active

    # build headers list
    headers = sensorNames
    # insert time heading on left side of row
    headers.insert(0, 'Timestamp')

    printData = processedData


    for row in zip(processedData):
        ws.append(row)

    wb.save("defaultOutput.xlsx")


def processData(sensorNames, sensorData, timeStampBegin, timeStampEnd, sampleRateDes):
    '''
    takes in 
    - sensorNames: a list [] of the sensors to be exported and
    - sensorData: a list of lists [[sensor1Data],[sensor2Data],[sensor3Data]] of all data falling between the given timestamps
    - timeStampBegin: timestamp of session start
    - timeStampEnd: timestamp of session end
    - sampleRateDes: desired sample rate of the outputted data

    executes procedure
    - calls getSampleRates
    - find data lower frequency than sampleRateDes and interpolate it
    - find data higher frequency than sampleRateDes and decimate it
    - after modifying each data set, put it into a corresponding list in the processedData data structure



    returns processedData: a list of lists [[sensor1Data],[sensor2Data],[sensor3Data]] of all data falling between the given timestamps,
                            but processed


    '''
    sampleRates = getSampleRates(sensorNames)

    # generates empty list of lists to store new (processed) data in
    processedData = [[] for _ in range(len(sensorNames))]

    for sensorIdx in sensorData:
        currSampleRate = sampleRates[sensorIdx]

        if currSampleRate < sampleRateDes:
            processedData[sensorIdx] = interpolateData(
                sensorData[sensorIdx], sampleRateDes, currSampleRate)
        elif currSampleRate > sampleRateDes:
            processedData[sensorIdx] = decimateData(
                sensorData[sensorIdx], sampleRateDes, currSampleRate)

    return processedData


def getSampleRates(sensorNames):
    '''

    '''
    rates = []
    return rates


def interpolateData(data, sampleRateDes, currSampleRate):
    '''

    '''
    outputData = []
    return outputData


def decimateData(data, sampleRateDes, currSampleRate):
    '''

    '''

    outputData = []
    return outputData
