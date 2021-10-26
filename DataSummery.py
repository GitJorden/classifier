import os

import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas
import seaborn

import plotSubjectGraph

seaborn.set_palette('husl')
import matplotlib.pyplot as pyplot
import matplotlib.patches as mpatches
import scipy.io
import Preprocess
import re
from openpyxl import Workbook
def dataSummery(subjectsData):
    dataFrame = pandas.DataFrame(index=['ASD', 'No Diagnose', 'LANG', 'SensoryMotoric', 'error'],
                                 columns=['dataListed',
                                          'coordinate_6', 'coordinate_10', 'coordinate_11', 'coordinate_AVG',
                                          'time_6', 'time_10', 'time_11', 'time_AVG',
                                          'meanDiameter_6', 'meanDiameter_10', 'meanDiameter_11', 'meanDiameter_AVG',
                                          'volume_6', 'volume_10', 'volume_11', 'volume_AVG',
                                          'focus_6', 'focus_10', 'focus_11', 'focus_AVG',
                                          'diameterFocus_6', 'diameterFocus_10',
                                          'diameterFocus_11', 'diameterFocus_AVG',
                                          'diameterNotFocus_6', 'diameterNotFocus_10',
                                          'diameterNotFocus_11', 'diameterNotFocus_AVG',
                                          'volumeByArea_6', 'volumeByArea_10', 'volumeByArea_11', 'volumeByArea_AVG',
                                          'timeByArea_6', 'timeByArea_10', 'timeByArea_11', 'timeByArea_AVG',
                                          'meanDiameterByArea_6', 'meanDiameterByArea_10',
                                          'meanDiameterByArea_11', 'meanDiameterByArea_AVG'])

    dataFrame.at['ASD', 'dataListed'] = []
    dataFrame.at['No Diagnose', 'dataListed'] = []
    dataFrame.at['LANG', 'dataListed'] = []
    dataFrame.at['SensoryMotoric', 'dataListed'] = []
    dataFrame.at['error', 'dataListed'] = []

    for subject in subjectsData:
        if subject['diagnose'] == 'ASD':
            dataFrame.at['ASD', 'dataListed'].append(subject)
        elif subject['diagnose'] == 'No Diagnose':
            dataFrame.at['No Diagnose', 'dataListed'].append(subject)
        elif subject['diagnose'] == 'LANG':
            dataFrame.at['LANG', 'dataListed'].append(subject)
        elif subject['diagnose'] == 'SensoryMotoric':
            dataFrame.at['SensoryMotoric', 'dataListed'].append(subject)
        else:
            dataFrame.at['error', 'dataListed'].append(subject)

    for index, row in dataFrame.iterrows():
        v = row['dataListed']
        # row['time_6'], row['time_10'], row['time_11'], \
        # row['time_AVG'] = RunAOITimesAnalysisByDiagnose(row['dataListed'])
        row['coordinate_6'], row['coordinate_10'], row['coordinate_11'], row['coordinate_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'coordinate', True, sortAOIsDataByTime)
        row['time_6'], row['time_10'], row['time_11'], row['time_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'time', True, sortAOIsDataByTime)
        row['meanDiameter_6'], row['meanDiameter_10'], row['meanDiameter_11'], row['meanDiameter_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'meanDiameter', True, sortAOIsDataByMeanDiameter)
        row['volume_6'], row['volume_10'], row['volume_11'], row['volume_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'volume', True, sortAOIsDataByVolume)
        row['focus_6'], row['focus_10'], row['focus_11'], row['focus_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'focus', False, sortAOIsDataByFocus)
        row['diameterFocus_6'], row['diameterFocus_10'], row['diameterFocus_11'], row['diameterFocus_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'diameterFocus', True, sortAOIsDataByDiameterFocus)
        row['diameterNotFocus_6'], row['diameterNotFocus_10'], row['diameterNotFocus_11'], row['diameterNotFocus_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'diameterNotFocus', True,
                                                sortAOIsDataByDiameterNotFocus)

        row['volumeByArea_6'], row['volumeByArea_10'], row['volumeByArea_11'], row['volumeByArea_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'volumeByArea', True, sortAOIsDataByVolumeByArea)
        row['timeByArea_6'], row['timeByArea_10'], row['timeByArea_11'], row['timeByArea_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'timeByArea', True, sortAOIsDataByTimeByArea)
        row['meanDiameterByArea_6'], row['meanDiameterByArea_10'],\
        row['meanDiameterByArea_11'], row['meanDiameterByArea_AVG']\
            = RunMeanDiameterAnalysisByDiagnose(row['dataListed'], 'meanDiameterByArea', True,
                                                sortAOIsDataByMeanDiameterByArea)

    dataFrame = dataFrame.drop(['dataListed'], axis=1)
    plotSubjectGraph.plotDataSummery(dataFrame)
    outCSVName = 'data_summery.xlsx'
    dataFrame.to_excel(outCSVName)
    return 0


def analyzeSubjectsData(fileName,
                        TETTime, CursorX, CursorY,
                        XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye, DiameterPupilLeftEye,
                        XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye,
                        DiameterPupilRightEye,
                        meanDiameter, TrialProc, AOI,
                        noDiagnostic, ASD, LANG, SensoryMotoric):
    if TrialProc.size == 0:
        return

    temp = re.findall(r'\d+', fileName)
    subjectNum = list(map(int, temp))[0]
    subjectProcedure = list(map(int, temp))[1]

    if subjectNum in ASD:
        diagnose = "ASD"
    elif subjectNum in LANG:
        diagnose = "LANG"
    elif subjectNum in SensoryMotoric:
        diagnose = "SensoryMotoric"
    elif subjectNum in noDiagnostic:
        diagnose = "No Diagnose"
    else:
        diagnose = "error"

    numberOfTrials, trialStartIndexes, trialEndIndexes = plotSubjectGraph.GetNumberAndListOfTrials(TrialProc)

    AOITimesPerTrial = GetAOITimesPerTrial(numberOfTrials, TrialProc, trialStartIndexes, trialEndIndexes, TETTime, AOI,
                                           meanDiameter, CursorX, CursorY)

    subjectData = {'subject': subjectNum,
                   'diagnose': diagnose,
                   'AOITimesPerTrial': AOITimesPerTrial}
    return subjectData


def GetAOISpan(trialStartIndex, trialEndIndex, TETTime, AOI):
    TETTimeStarts = TETTime[trialStartIndex:trialEndIndex - 1, :1]
    TETTimeEnds = TETTime[trialStartIndex + 1:trialEndIndex, :1]

    AOIStarts = AOI[trialStartIndex:trialEndIndex - 1, :1]

    TETTime = TETTime[trialStartIndex:trialEndIndex, :1]

    AOITimes = [{'aoi': 0, 'time': 0},
                {'aoi': 1, 'time': 0},
                {'aoi': 2, 'time': 0},
                {'aoi': 3, 'time': 0},
                {'aoi': 4, 'time': 0},
                {'aoi': 5, 'time': 0}]

    for i in range(trialEndIndex - trialStartIndex - 1):
        if AOIStarts[i][0] == 0:
            AOITimes[0]['time'] = AOITimes[0]['time'] + (TETTimeEnds[i][0] - TETTimeStarts[i][0])
        if AOIStarts[i][0] == 1:
            val = AOITimes[1]['time']
            valT = TETTimeEnds[i][0] - TETTimeStarts[i][0]
            AOITimes[1]['time'] = AOITimes[1]['time'] + (TETTimeEnds[i][0] - TETTimeStarts[i][0])
        if AOIStarts[i][0] == 2:
            AOITimes[2]['time'] = AOITimes[2]['time'] + (TETTimeEnds[i][0] - TETTimeStarts[i][0])
        if AOIStarts[i][0] == 3:
            AOITimes[3]['time'] = AOITimes[3]['time'] + (TETTimeEnds[i][0] - TETTimeStarts[i][0])
        if AOIStarts[i][0] == 4:
            AOITimes[4]['time'] = AOITimes[4]['time'] + (TETTimeEnds[i][0] - TETTimeStarts[i][0])
        if AOIStarts[i][0] == 5:
            AOITimes[5]['time'] = AOITimes[5]['time'] + (TETTimeEnds[i][0] - TETTimeStarts[i][0])

    AOITimes.sort(reverse=True, key=sortAOITimes)
    return AOITimes


def sortAOITimes(e):
    return e['time']


def GetAOITimesPerTrial(numberOfTrials, TrialProc, trialStartIndexes, trialEndIndexes, TETTime, AOI,
                        MeanDiameter, CursorX, CursorY):
    AOIDataPerTrial = []
    for i in range(numberOfTrials):
        currentTrial = TrialProc[trialStartIndexes[i]]
        # AOIData = GetAOISpan(trialStartIndexes[i], trialEndIndexes[i], TETTime, AOI)
        AOIData = GetAOIVolumeMeanDiameterCursor(trialStartIndexes[i], trialEndIndexes[i], TETTime, AOI,
                                                 MeanDiameter, CursorX, CursorY)
        AOIDataPerTrial.append(AOIData)

    return AOIDataPerTrial

def GetAOIVolumeMeanDiameterCursor(trialStartIndex, trialEndIndex, TETTime, AOI, MeanDiameter, CursorX, CursorY):
    TETTimeStarts = TETTime[trialStartIndex:trialEndIndex - 1, :1]
    TETTimeEnds = TETTime[trialStartIndex + 1:trialEndIndex, :1]

    AOI = AOI[trialStartIndex:trialEndIndex - 1, :1]
    MeanDiameter = MeanDiameter[trialStartIndex:trialEndIndex - 1, :1]
    CursorX = CursorX[trialStartIndex:trialEndIndex - 1, :1]
    CursorY = CursorY[trialStartIndex:trialEndIndex - 1, :1]

    TETTime = TETTime[trialStartIndex:trialEndIndex, :1]

    AOIsData = [{'aoi': 0, 'coordinate': [0, 0], 'time': 0, 'meanDiameter': 0, 'volume': 0, 'focus': 0,
                 'diameterFocus': 0, 'diameterNotFocus': 0,
                 'volumeByArea': 0, 'timeByArea': 0, 'meanDiameterByArea': 0},
                {'aoi': 1, 'coordinate': [0, 0], 'time': 0, 'meanDiameter': 0, 'volume': 0, 'focus': 0,
                 'diameterFocus': 0, 'diameterNotFocus': 0,
                 'volumeByArea': 0, 'timeByArea': 0, 'meanDiameterByArea': 0},
                {'aoi': 2, 'coordinate': [0, 0], 'time': 0, 'meanDiameter': 0, 'volume': 0, 'focus': 0,
                 'diameterFocus': 0, 'diameterNotFocus': 0,
                 'volumeByArea': 0, 'timeByArea': 0, 'meanDiameterByArea': 0},
                {'aoi': 3, 'coordinate': [0, 0], 'time': 0, 'meanDiameter': 0, 'volume': 0, 'focus': 0,
                 'diameterFocus': 0, 'diameterNotFocus': 0,
                 'volumeByArea': 0, 'timeByArea': 0, 'meanDiameterByArea': 0},
                {'aoi': 4, 'coordinate': [0, 0], 'time': 0, 'meanDiameter': 0, 'volume': 0, 'focus': 0,
                 'diameterFocus': 0, 'diameterNotFocus': 0,
                 'volumeByArea': 0, 'timeByArea': 0, 'meanDiameterByArea': 0},
                {'aoi': 5, 'coordinate': [0, 0], 'time': 0, 'meanDiameter': 0, 'volume': 0, 'focus': 0,
                 'diameterFocus': 0, 'diameterNotFocus': 0,
                 'volumeByArea': 0, 'timeByArea': 0, 'meanDiameterByArea': 0}]

    for i in range(trialEndIndex - trialStartIndex - 1):
        if AOI[i][0] == 0:
            focus = False
            AOIsData[0] = InsertAOIDataByVideo(0, AOIsData[0], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                               MeanDiameter[i][0], focus, CursorX[i][0], CursorY[i][0])
        if AOI[i][0] == 1:
            focus = CursorX[i][0] < (1024 * (4 / 10)) and CursorY[i][0] < (768 * (4 / 10))
            AOIsData[1] = InsertAOIDataByVideo(1, AOIsData[1], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                               MeanDiameter[i][0], focus, CursorX[i][0], CursorY[i][0])
        if AOI[i][0] == 2:
            focus = CursorX[i][0] > (1024 * (6 / 10)) and CursorY[i][0] < (768 * (4 / 10))
            AOIsData[2] = InsertAOIDataByVideo(2, AOIsData[2], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                               MeanDiameter[i][0], focus, CursorX[i][0], CursorY[i][0])
        if AOI[i][0] == 3:
            focus = CursorX[i][0] < (1024 * (4 / 10)) and CursorY[i][0] > (768 * (6 / 10))
            AOIsData[3] = InsertAOIDataByVideo(3, AOIsData[3], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                               MeanDiameter[i][0], focus, CursorX[i][0], CursorY[i][0])
        if AOI[i][0] == 4:
            focus = CursorX[i][0] > (1024 * (6 / 10)) and CursorY[i][0] > (768 * (6 / 10))
            AOIsData[4] = InsertAOIDataByVideo(4, AOIsData[4], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                               MeanDiameter[i][0], focus, CursorX[i][0], CursorY[i][0])
        if AOI[i][0] == 5:
            focus = False
            AOIsData[5] = InsertAOIDataByVideo(5, AOIsData[5], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                               MeanDiameter[i][0], focus, CursorX[i][0], CursorY[i][0])

        if CursorX[i][0] < (1024 * (4 / 10)) and CursorY[i][0] < (768 * (4 / 10)):
            AOIsData[1] = InsertAOIDataByArea(AOIsData[1], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                              MeanDiameter[i][0])
        if CursorX[i][0] > (1024 * (6 / 10)) and CursorY[i][0] < (768 * (4 / 10)):
            AOIsData[2] = InsertAOIDataByArea(AOIsData[2], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                              MeanDiameter[i][0])
        if CursorX[i][0] < (1024 * (4 / 10)) and CursorY[i][0] > (768 * (6 / 10)):
            AOIsData[3] = InsertAOIDataByArea(AOIsData[3], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                              MeanDiameter[i][0])
        if CursorX[i][0] > (1024 * (6 / 10)) and CursorY[i][0] > (768 * (6 / 10)):
            AOIsData[4] = InsertAOIDataByArea(AOIsData[4], (TETTimeEnds[i][0] - TETTimeStarts[i][0]),
                                              MeanDiameter[i][0])
    for i in range(len(AOIsData)):
        AOIsData[i] = CalculateAOIDataByVideo(AOIsData[i])
        AOIsData[i] = CalculateAOIDataByArea(AOIsData[i])
    return AOIsData


def sortAOIsDataByCoordinate(e):
    return e['coordinate']


def sortAOIsDataByTime(e):
    return e['time']


def sortAOIsDataByMeanDiameter(e):
    return e['meanDiameter']

def sortAOIsDataByVolume(e):
    return e['volume']

def sortAOIsDataByFocus(e):
    return e['focus']

def sortAOIsDataByDiameterFocus(e):
    return e['diameterFocus']

def sortAOIsDataByDiameterNotFocus(e):
    return e['diameterNotFocus']

def sortAOIsDataByVolumeByArea(e):
    return e['volumeByArea']

def sortAOIsDataByTimeByArea(e):
    return e['timeByArea']

def sortAOIsDataByMeanDiameterByArea(e):
    return e['meanDiameterByArea']

def InsertAOIDataByVideo(AOINumber, AOIData, time, meanDiameter, focus, x, y):
    AOIData['coordinate'][0] += x
    AOIData['coordinate'][1] += y
    AOIData['volume'] += 1
    AOIData['meanDiameter'] += meanDiameter
    AOIData['time'] += time
    if AOINumber != 5 or AOINumber != 0:
        if focus:
            AOIData['focus'] += 1
            AOIData['diameterFocus'] += meanDiameter
        else:
            AOIData['diameterNotFocus'] += meanDiameter
    else:
        AOIData['focus'] += 1
    return AOIData

def InsertAOIDataByArea(AOIData, time, meanDiameter):
    AOIData['volumeByArea'] += 1
    AOIData['meanDiameterByArea'] += meanDiameter
    AOIData['timeByArea'] += time
    return AOIData


def CalculateAOIDataByVideo(AOIData):
    volume = AOIData['volume']
    if volume == 0:
        return AOIData

    AOIData['coordinate'][0] = AOIData['coordinate'][0] / volume
    AOIData['coordinate'][1] = AOIData['coordinate'][1] / volume

    AOIData['meanDiameter'] = AOIData['meanDiameter'] / volume

    AOIData['focus'] = AOIData['focus'] / volume
    if (volume * AOIData['focus']) != 0:
        AOIData['diameterFocus'] = AOIData['diameterFocus'] / (volume * AOIData['focus'])
    if (volume * (1 - AOIData['focus'])) != 0:
        AOIData['diameterNotFocus'] = AOIData['diameterNotFocus'] / (volume * (1 - AOIData['focus']))
    return AOIData

def CalculateAOIDataByArea(AOIData):
    if AOIData['volumeByArea'] != 0:
        AOIData['meanDiameterByArea'] = AOIData['meanDiameterByArea'] / AOIData['volumeByArea']
    return AOIData

def RunAOITimesAnalysisByDiagnose(subjectsData):
    trialsData = GetTrialData(subjectsData)
    AOIDescendingList = []
    timesByAOI = []

    for i in range(len(trialsData)):
        trial = trialsData[i]
        aoiScore = [0, 0, 0, 0, 0, 0]
        aoiTrialList = []
        timeByAOI = []
        for j in range(len(trial)):
            for k in range(len(trial[j])):
                if trial[j][k]['time'] == 0:
                    continue
                aoiScore[trial[j][k]['aoi']] += trial[j][k]['time']
                # aoiScore[trial[j][k]['aoi']] += (5 - k)
        for j in range(len(aoiScore)):
            timeByAOI.append(aoiScore[j] / len(trial))
        for j in range(len(aoiScore)):
            index = aoiScore.index(max(aoiScore))
            aoiTrialList.append(index)
            aoiScore[index] = -1

        AOIDescendingList.append(aoiTrialList)
        timesByAOI.append(timeByAOI)

    return AOIDescendingList[0], AOIDescendingList[1], AOIDescendingList[2], timesByAOI

def GetTrialData(subjectsData):
    trialsData = [[], [], []]
    for subject in subjectsData:
        diagnose = subject['diagnose']
        for i in range(len(subject['AOITimesPerTrial'])):
            if len(subject['AOITimesPerTrial']) > 3:
                print(subject)
                continue
            val = subject['AOITimesPerTrial'][i]
            trialsData[i].append(val)

    return trialsData

def GetAOIScoreByParameter(trialsData, parm, reverse, keyFunc):
    AOIList = []
    averagesByAOI = []
    for i in range(len(trialsData)):
        trial = trialsData[i]
        aoiScore = [0, 0, 0, 0, 0, 0]
        AOIEntries = [0, 0, 0, 0, 0, 0]
        aoiTrialList = []
        averageByAOI = []
        for j in range(len(trial)):
            trialJ = trial[j]
            AOIsData = trialJ[:]
            AOIsData.sort(reverse=reverse, key=keyFunc)
            for k in range(len(AOIsData)):
                if AOIsData[k][parm] == 0:
                    continue
                h = AOIsData[k]['aoi']
                t = AOIsData[k][parm]
                aoiScore[AOIsData[k]['aoi']] += AOIsData[k][parm]
                AOIEntries[AOIsData[k]['aoi']] += 1
        for j in range(len(aoiScore)):
            if j == 0 or j == 5:
                continue
            if AOIEntries[j] == 0:
                averageByAOI.append(0)
                continue
            averageByAOI.append(aoiScore[j] / AOIEntries[j])
        aoiScore[0] = -1
        aoiScore[5] = -1
        for j in range(len(aoiScore)):
            index = aoiScore.index(max(aoiScore))
            aoiTrialList.append(index)
            aoiScore[index] = -1

        AOIList.append(aoiTrialList)
        averagesByAOI.append(averageByAOI)

    return AOIList[0], AOIList[1], AOIList[2], averagesByAOI

def RunMeanDiameterAnalysisByDiagnose(subjectsData, parm, reverse, keyFunc):
    trialsData = GetTrialData(subjectsData)
    if parm == 'coordinate':
        return GetCoordinateAOIScoreByParameter(trialsData, parm, reverse, keyFunc)
    return GetAOIScoreByParameter(trialsData, parm, reverse, keyFunc)

def GetCoordinateAOIScoreByParameter(trialsData, parm, reverse, keyFunc):
    AOIList = []
    averagesByAOI = []
    for i in range(len(trialsData)):
        trial = trialsData[i]
        aoiScore = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        AOIEntries = [0, 0, 0, 0, 0, 0]
        aoiTrialList = []
        averageByAOI = []
        for j in range(len(trial)):
            trialJ = trial[j]
            AOIsData = trialJ[:]
            AOIsData.sort(reverse=reverse, key=keyFunc)
            for k in range(len(AOIsData)):
                if AOIsData[k][parm][0] == 0 and AOIsData[k][parm][1] == 0:
                    continue
                aoiScore[AOIsData[k]['aoi']][0] += AOIsData[k][parm][0]
                aoiScore[AOIsData[k]['aoi']][1] += AOIsData[k][parm][1]
                AOIEntries[AOIsData[k]['aoi']] += 1
        for j in range(len(aoiScore)):
            if j == 0 or j == 5:
                continue
            if AOIEntries[j] == 0:
                averageByAOI.append([0, 0])
                continue
            x_avg = aoiScore[j][0] / AOIEntries[j]
            y_avg = aoiScore[j][1] / AOIEntries[j]
            averageByAOI.append([x_avg, y_avg])
        aoiScore[0] = [-1, -1]
        aoiScore[5] = [-1, -1]
        for j in range(len(aoiScore)):
            index = aoiScore.index(max(aoiScore))
            aoiTrialList.append(index)
            aoiScore[index] = [-1, -1]

        AOIList.append(aoiTrialList)
        averagesByAOI.append(averageByAOI)

    return AOIList[0], AOIList[1], AOIList[2], averagesByAOI