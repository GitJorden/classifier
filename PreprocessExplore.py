import numpy
import numpy as np
import pandas

import scipy.io
import re

def Process(file):
    fileToread = 'in_preprocess\\' + file
    dataFrame = pandas.read_csv(fileToread)

    dataFrame.TETTime = dataFrame['TETTime'] - dataFrame['TETTime'].iloc[0]

    dataFrame = dataFrame.drop(['Subject'], axis=1)
    dataFrame = dataFrame.drop(['Session'], axis=1)
    dataFrame = dataFrame.drop(['ID'], axis=1)

    dataFrame = dataFrame.drop(['RTTime'], axis=1)
    dataFrame = dataFrame.drop(['TimestampSec'], axis=1)
    dataFrame = dataFrame.drop(['TimestampMicrosec'], axis=1)

    dataFrame = dataFrame.drop(['LeftMovieU'], axis=1)
    dataFrame = dataFrame.drop(['RightMovieU'], axis=1)
    dataFrame = dataFrame.drop(['LeftMovieD'], axis=1)
    dataFrame = dataFrame.drop(['RightMovieD'], axis=1)
    dataFrame = dataFrame.drop(['AOIStimulus'], axis=1)

    dataFrame = dataFrame.drop(['CRESP'], axis=1)
    dataFrame = dataFrame.drop(['RESP'], axis=1)
    dataFrame = dataFrame.drop(['ACC'], axis=1)
    dataFrame = dataFrame.drop(['RT'], axis=1)
    dataFrame = dataFrame.drop(['UserDefined_1'], axis=1)

    for index, row in dataFrame.iterrows():
        temp = re.findall(r'\d+', row['TrialProc'])
        trialProcNum = list(map(int, temp))
        if not trialProcNum:
            dataFrame['TrialProc'][index] = 0
        else:
            dataFrame['TrialProc'][index] = list(map(int, temp)).pop()

        if pandas.isna(row['AOI']):
            dataFrame['AOI'][index] = 0
        elif row['AOI'] == '1':
            dataFrame['AOI'][index] = 1
        elif row['AOI'] == '2':
            dataFrame['AOI'][index] = 2
        elif row['AOI'] == '3':
            dataFrame['AOI'][index] = 3
        elif row['AOI'] == '4':
            dataFrame['AOI'][index] = 4
        elif row['AOI'] == 'else':
            dataFrame['AOI'][index] = 1

        insertRightEyeData = False
        insertLeftEyeData = False

        if row['CursorX'] == -1 or row['CursorY'] == -1:
            dataFrame = dataFrame.drop(index)
            continue

        if row['XGazePosLeftEye'] == -1 or row['YGazePosLeftEye'] == -1:
            if row['ValidityRightEye'] < 2:
                insertRightEyeData = True
            else:
                dataFrame = dataFrame.drop(index)
                continue
        if row['XCameraPosLeftEye'] == -1 or row['YCameraPosLeftEye'] == -1:
            if row['ValidityRightEye'] < 2:
                insertRightEyeData = True
            else:
                dataFrame = dataFrame.drop(index)
                continue
        if row['DiameterPupilLeftEye'] == -1 or row['DistanceLeftEye'] == -1 or row['ValidityLeftEye'] > 1:
            if row['ValidityRightEye'] < 2:
                insertRightEyeData = True
            else:
                dataFrame = dataFrame.drop(index)
                continue

        if row['XGazePosRightEye'] == -1 or row['YGazePosRightEye'] == -1:
            if row['ValidityLeftEye'] < 2:
                insertLeftEyeData = True
            else:
                dataFrame = dataFrame.drop(index)
                continue
        if row['XCameraPosRightEye'] == -1 or row['YCameraPosRightEye'] == -1:
            if row['ValidityLeftEye'] < 2:
                insertLeftEyeData = True
            else:
                dataFrame = dataFrame.drop(index)
                continue
        if row['DiameterPupilRightEye'] == -1 or row['DistanceRightEye'] == -1 or row['ValidityRightEye'] > 1:
            if row['ValidityLeftEye'] < 2:
                insertLeftEyeData = True
            else:
                dataFrame = dataFrame.drop(index)
                continue

        if insertRightEyeData:
            dataFrame = InsertRightEyeData(dataFrame, index)
        elif insertLeftEyeData:
            dataFrame = InsertLeftEyeData(dataFrame, index)

    dataFrame.reset_index(drop=True)

    temp = re.findall(r'\d+', file)
    subjectNum = list(map(int, temp))[0]
    subjectProcedure = list(map(int, temp))[1]
    outCSVName = 'out_preprocess\\%d-%d-explore-out.csv' % (subjectNum, subjectProcedure)
    dataFrame.to_csv(outCSVName, sep='\t', index=False, encoding='utf-8')
    return dataFrame

def InsertRightEyeData(dataFrame, index):
    dataFrame['XGazePosLeftEye'][index] = dataFrame['XGazePosRightEye'][index]
    dataFrame['YGazePosLeftEye'][index] = dataFrame['YGazePosRightEye'][index]
    dataFrame['XCameraPosLeftEye'][index] = dataFrame['XCameraPosRightEye'][index]
    dataFrame['YCameraPosLeftEye'][index] = dataFrame['YCameraPosRightEye'][index]
    dataFrame['DiameterPupilLeftEye'][index] = dataFrame['DiameterPupilRightEye'][index]
    dataFrame['DistanceLeftEye'][index] = dataFrame['DistanceRightEye'][index]
    dataFrame['ValidityLeftEye'][index] = dataFrame['ValidityRightEye'][index]

    return dataFrame

def InsertLeftEyeData(dataFrame, index):
    dataFrame['XGazePosRightEye'][index] = dataFrame['XGazePosLeftEye'][index]
    dataFrame['YGazePosRightEye'][index] = dataFrame['YGazePosLeftEye'][index]
    dataFrame['XCameraPosRightEye'][index] = dataFrame['XCameraPosLeftEye'][index]
    dataFrame['YCameraPosRightEye'][index] = dataFrame['YCameraPosLeftEye'][index]
    dataFrame['DiameterPupilRightEye'][index] = dataFrame['DiameterPupilLeftEye'][index]
    dataFrame['DistanceRightEye'][index] = dataFrame['DistanceLeftEye'][index]
    dataFrame['ValidityRightEye'][index] = dataFrame['ValidityLeftEye'][index]

    return dataFrame

def GetDataColumns(dataFrame):
    TETTime = dataFrame['TETTime']

    CursorX = dataFrame['CursorX']
    CursorY = dataFrame['CursorY']

    XGazePosLeftEye = dataFrame['XGazePosLeftEye']
    YGazePosLeftEye = dataFrame['YGazePosLeftEye']
    XCameraPosLeftEye = dataFrame['XCameraPosLeftEye']
    YCameraPosLeftEye = dataFrame['YCameraPosLeftEye']
    DiameterPupilLeftEye = dataFrame['DiameterPupilLeftEye']
    DistanceLeftEye = dataFrame['DistanceLeftEye']
    ValidityLeftEye = dataFrame['ValidityLeftEye']

    XGazePosRightEye = dataFrame['XGazePosRightEye']
    YGazePosRightEye = dataFrame['YGazePosRightEye']
    XCameraPosRightEye = dataFrame['XCameraPosRightEye']
    YCameraPosRightEye = dataFrame['YCameraPosRightEye']
    DiameterPupilRightEye = dataFrame['DiameterPupilRightEye']
    DistanceRightEye = dataFrame['DistanceRightEye']
    ValidityRightEye = dataFrame['ValidityRightEye']

    TrialId = dataFrame['TrialId']

    TrialProc = dataFrame['TrialProc']
    AOI = dataFrame['AOI']

    TETTime = numpy.array(TETTime)

    CursorX = numpy.array(CursorX)
    CursorY = numpy.array(CursorY)

    XGazePosLeftEye = numpy.array(XGazePosLeftEye)
    YGazePosLeftEye = numpy.array(YGazePosLeftEye)
    XCameraPosLeftEye = numpy.array(XCameraPosLeftEye)
    YCameraPosLeftEye = numpy.array(YCameraPosLeftEye)
    DiameterPupilLeftEye = numpy.array(DiameterPupilLeftEye)
    DistanceLeftEye = numpy.array(DistanceLeftEye)
    ValidityLeftEye = numpy.array(ValidityLeftEye)

    XGazePosRightEye = numpy.array(XGazePosRightEye)
    YGazePosRightEye = numpy.array(YGazePosRightEye)
    XCameraPosRightEye = numpy.array(XCameraPosRightEye)
    YCameraPosRightEye = numpy.array(YCameraPosRightEye)
    DiameterPupilRightEye = numpy.array(DiameterPupilRightEye)
    DistanceRightEye = numpy.array(DistanceRightEye)
    ValidityRightEye = numpy.array(ValidityRightEye)

    TrialId = numpy.array(TrialId)

    TrialProc = numpy.array(TrialProc)
    AOI = numpy.array(AOI)

    TETTime = TETTime.reshape(TETTime.size, 1)

    CursorX = CursorX.reshape(CursorX.size, 1)
    CursorY = CursorY.reshape(CursorY.size, 1)

    XGazePosLeftEye = XGazePosLeftEye.reshape(XGazePosLeftEye.size, 1)
    YGazePosLeftEye = YGazePosLeftEye.reshape(YGazePosLeftEye.size, 1)
    XCameraPosLeftEye = XCameraPosLeftEye.reshape(XCameraPosLeftEye.size, 1)
    YCameraPosLeftEye = YCameraPosLeftEye.reshape(YCameraPosLeftEye.size, 1)
    DiameterPupilLeftEye = DiameterPupilLeftEye.reshape(DiameterPupilLeftEye.size, 1)
    DistanceLeftEye = DistanceLeftEye.reshape(DistanceLeftEye.size, 1)
    ValidityLeftEye = ValidityLeftEye.reshape(ValidityLeftEye.size, 1)

    XGazePosRightEye = XGazePosRightEye.reshape(XGazePosRightEye.size, 1)
    YGazePosRightEye = YGazePosRightEye.reshape(YGazePosRightEye.size, 1)
    XCameraPosRightEye = XCameraPosRightEye.reshape(XCameraPosRightEye.size, 1)
    YCameraPosRightEye = YCameraPosRightEye.reshape(YCameraPosRightEye.size, 1)
    DiameterPupilRightEye = DiameterPupilRightEye.reshape(DiameterPupilRightEye.size, 1)
    DistanceRightEye = DistanceRightEye.reshape(DistanceRightEye.size, 1)
    ValidityRightEye = ValidityRightEye.reshape(ValidityRightEye.size, 1)

    TrialId = TrialId.reshape(TrialId.size, 1)

    TrialProc = TrialProc.reshape(TrialProc.size, 1)
    AOI = AOI.reshape(AOI.size, 1)

    return TETTime, \
           CursorX, CursorY, \
           XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye, \
           DiameterPupilLeftEye, DistanceLeftEye, ValidityLeftEye,\
           XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye, \
           DiameterPupilRightEye, DistanceRightEye,\
           ValidityRightEye, TrialId, TrialProc, AOI

