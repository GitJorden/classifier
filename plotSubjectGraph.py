import os

# from basic_units import cm, inch
import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas
import seaborn
seaborn.set_palette('husl')
import matplotlib.pyplot as pyplot
import matplotlib.patches as mpatches
import scipy.io
import Preprocess
import re

def plotFileData(fileName,
                 TETTime, CursorX, CursorY,
                 XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye, DiameterPupilLeftEye,
                 XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye, DiameterPupilRightEye,
                 meanDiameter, TrialProc, AOI,
                 noDiagnostic, ASD, LANG, SensoryMotoric):
    if TrialProc.size == 0:
        return

    temp = re.findall(r'\d+', fileName)
    subjectNum = list(map(int, temp))[0]
    subjectProcedure = list(map(int, temp))[1]
    diagnose = ""

    if subjectNum in ASD:
        diagnose = "ASD"
    elif subjectNum in LANG:
        diagnose = "LANG"
    elif subjectNum in SensoryMotoric:
        diagnose = "SensoryMotoric"
    elif subjectNum in noDiagnostic:
        diagnose = "No diagnose"
    else:
        diagnose = "error"

    numberOfTrials, trialStartIndexes, trialEndIndexes = GetNumberAndListOfTrials(TrialProc)

    for i in range(numberOfTrials):
        currentTrial = TrialProc[trialStartIndexes[i]]

        fig, ax = pyplot.subplots(dpi = 250)
        PlotMeanDiameterAOI(fig, ax,
                            subjectNum, subjectProcedure, trialStartIndexes[i], trialEndIndexes[i], currentTrial,
                            TETTime, DiameterPupilLeftEye, DiameterPupilRightEye, AOI, diagnose, 'Mean')

    for i in range(numberOfTrials):
        currentTrial = TrialProc[trialStartIndexes[i]]

        fig, ax = pyplot.subplots(dpi = 250)
        PlotDiameterAOITrialproc(fig, ax,
                                 subjectNum, subjectProcedure, trialStartIndexes[i], trialEndIndexes[i], currentTrial,
                                 TETTime, DiameterPupilLeftEye, DiameterPupilRightEye, AOI, diagnose, 'Diameter')

    for i in range(numberOfTrials):
        currentTrial = TrialProc[trialStartIndexes[i]]

        fig, ax = pyplot.subplots(dpi = 250)
        ax.set_aspect('equal')
        plotCursorPerTrial(fig, ax,
                           subjectNum, subjectProcedure, trialStartIndexes[i], trialEndIndexes[i], currentTrial,
                           CursorX, CursorY, meanDiameter, AOI, diagnose, 'Cursor')

    for i in range(numberOfTrials):
        currentTrial = TrialProc[trialStartIndexes[i]]

        fig, ax = pyplot.subplots(dpi = 250)
        ax.set_aspect('equal')
        plotGazePerTrial(fig, ax,
                         subjectNum, subjectProcedure, trialStartIndexes[i], trialEndIndexes[i], currentTrial,
                         XGazePosLeftEye, YGazePosLeftEye, XGazePosRightEye, YGazePosRightEye, meanDiameter, AOI,
                         diagnose, 'Gaze')

    # for i in range(numberOfTrials):
    #     currentTrial = TrialProc[trialStartIndexes[i]]
    #
    #     fig, ax = pyplot.subplots(dpi = 150)
    #     ax.set_aspect('equal')
    #     plotCameraPerTrial(fig, ax,
    #                        subjectNum, subjectProcedure, trialStartIndexes[i], trialEndIndexes[i], currentTrial,
    #                        XCameraPosLeftEye, YCameraPosLeftEye, XCameraPosRightEye, YCameraPosRightEye,
    #                        meanDiameter, AOI, diagnose, 'Camera')


def PlotMeanDiameterAOI(fig, ax,
                        subjectNum, subjectProcedure, trialStartIndex, trialEndIndex, currentTrial,
                        TETTime, DiameterPupilLeftEye, DiameterPupilRightEye, AOI, diagnose, plotName):

    TETTimeStarts = TETTime[trialStartIndex:trialEndIndex - 1, :1]
    TETTimeEnds = TETTime[trialStartIndex + 1:trialEndIndex, :1]

    AOIStarts = AOI[trialStartIndex:trialEndIndex - 1, :1]

    TETTime = TETTime[trialStartIndex:trialEndIndex, :1]
    DiameterPupilLeftEye = DiameterPupilLeftEye[trialStartIndex:trialEndIndex, :1]
    DiameterPupilRightEye = DiameterPupilRightEye[trialStartIndex:trialEndIndex, :1]

    AOIColors = ["#ffffff", "#ffdd00", "#00ff44", "#00a6ff", "#8800ff", "#b3faff"]

    for i in range(trialEndIndex - trialStartIndex - 1):
        ax.axvspan(TETTimeStarts[i], TETTimeEnds[i], facecolor=AOIColors[AOIStarts[i][0]], zorder=0)

    ax.plot(TETTime, (DiameterPupilLeftEye + DiameterPupilRightEye) / 2, linewidth=0.1, c='black')

    AOIBlank = mpatches.Patch(color = '#ffffff', label = 'blanks AOI')
    AOI1 = mpatches.Patch(color = '#ffdd00', label = '1 AOI')
    AOI2 = mpatches.Patch(color = '#00ff44', label = '2 AOI')
    AOI3 = mpatches.Patch(color = '#00a6ff', label = '3 AOI')
    AOI4 = mpatches.Patch(color = '#8800ff', label = '4 AOI')
    AOIElse = mpatches.Patch(color = '#b3faff', label = 'else AOI')
    # ax.legend(handles = [AOIBlank, AOI1, AOI2, AOI3, AOI4, AOIElse], bbox_to_anchor = (1.05, 1), loc = 'upper left',
    #           borderaxespad = 0.)

    ax.legend(handles = [AOIBlank, AOI1, AOI2, AOI3, AOI4, AOIElse], bbox_to_anchor = (1.05, 1), loc = 'upper left')

    fig.subplots_adjust(hspace = 1)

    plotTitle = createTitle(diagnose, plotName, subjectNum, currentTrial, subjectProcedure)
    ax.set_title(plotTitle)

    savePath = createSavePath(plotName, diagnose, subjectNum, currentTrial, subjectProcedure)
    fig.tight_layout()
    plt.savefig(savePath)

def PlotDiameterAOITrialproc(fig, ax,
                             subjectNum, subjectProcedure, trialStartIndex, trialEndIndex, currentTrial,
                             TETTime, DiameterPupilLeftEye, DiameterPupilRightEye, AOI, diagnose, plotName):

    TETTimeStarts = TETTime[trialStartIndex:trialEndIndex - 1, :1]
    TETTimeEnds = TETTime[trialStartIndex + 1:trialEndIndex, :1]

    AOIStarts = AOI[trialStartIndex:trialEndIndex - 1, :1]

    TETTime = TETTime[trialStartIndex:trialEndIndex, :1]
    DiameterPupilLeftEye = DiameterPupilLeftEye[trialStartIndex:trialEndIndex, :1]
    DiameterPupilRightEye = DiameterPupilRightEye[trialStartIndex:trialEndIndex, :1]

    AOIColors = ["#ffffff", "#ffdd00", "#00ff44", "#00a6ff", "#8800ff", "#b3faff"]

    for i in range(trialEndIndex - trialStartIndex - 1):
        ax.axvspan(TETTimeStarts[i], TETTimeEnds[i], facecolor=AOIColors[AOIStarts[i][0]], zorder=0)

    ax.scatter(TETTime, DiameterPupilLeftEye, s=0.5, c='red', zorder=2)
    ax.scatter(TETTime, DiameterPupilRightEye, s=0.5, c='blue', zorder=2)

    AOIBlank = mpatches.Patch(color = '#ffffff', label = 'blanks AOI')
    AOI1 = mpatches.Patch(color = '#ffdd00', label = '1 AOI')
    AOI2 = mpatches.Patch(color = '#00ff44', label = '2 AOI')
    AOI3 = mpatches.Patch(color = '#00a6ff', label = '3 AOI')
    AOI4 = mpatches.Patch(color = '#8800ff', label = '4 AOI')
    AOIElse = mpatches.Patch(color = '#b3faff', label = 'else AOI')
    ax.legend(handles = [AOIBlank, AOI1, AOI2, AOI3, AOI4, AOIElse], bbox_to_anchor = (1.05, 1), loc = 'upper left',
              borderaxespad = 0.)

    fig.subplots_adjust(hspace = 1)

    plotTitle = createTitle(diagnose, plotName, subjectNum, currentTrial, subjectProcedure)
    ax.set_title(plotTitle)

    savePath = createSavePath(plotName, diagnose, subjectNum, currentTrial, subjectProcedure)
    fig.tight_layout()
    plt.savefig(savePath)

def plotCameraPerTrial(fig, ax, subjectNum, subjectProcedure, trialStartIndex, trialEndIndex, currentTrial,
                       XCameraPosLeftEye, YCameraPosLeftEye, XCameraPosRightEye, YCameraPosRightEye,
                       meanDiameter, AOI, diagnose, plotName):

    XCameraPosLeftEye = XCameraPosLeftEye[trialStartIndex:trialEndIndex, :1]
    YCameraPosLeftEye = YCameraPosLeftEye[trialStartIndex:trialEndIndex, :1]
    XCameraPosRightEye = XCameraPosRightEye[trialStartIndex:trialEndIndex, :1]
    YCameraPosRightEye = YCameraPosRightEye[trialStartIndex:trialEndIndex, :1]
    meanDiameter = meanDiameter[trialStartIndex:trialEndIndex, :1]
    AOI = AOI[trialStartIndex:trialEndIndex, :1]

    XCameraPosLeftEyes = []
    YCameraPosLeftEyes = []

    XCameraPosRightEyes = []
    YCameraPosRightEyes = []

    for i in range(4):
        aoi = i + 1
        XCameraPosLeftEyes.append(numpy.ma.masked_where(AOI != aoi, XCameraPosLeftEye))
        YCameraPosLeftEyes.append(numpy.ma.masked_where(AOI != aoi, YCameraPosLeftEye))
        XCameraPosRightEyes.append(numpy.ma.masked_where(AOI != aoi, XCameraPosRightEye))
        YCameraPosRightEyes.append(numpy.ma.masked_where(AOI != aoi, YCameraPosRightEye))

    symbols = ['^', 's', 'x', '1']
    for i in range(4):
        scatterLeft = ax.scatter(XCameraPosLeftEyes[i], YCameraPosLeftEyes[i], s=10, c=meanDiameter, cmap='viridis',
                                 zorder=2, marker=symbols[i])
        scatterRight = ax.scatter(XCameraPosRightEyes[i], YCameraPosRightEyes[i], s=10, c=meanDiameter, cmap='seismic',
                                  zorder=2, marker=symbols[i])

        # x = [XCameraPosLeftEyes[i], XCameraPosRightEyes[i]]
        # y = [YCameraPosLeftEyes[i], YCameraPosRightEyes[i]]
        #
        # for j in range(len(XCameraPosLeftEyes[i])):
        #     ax.plot([x[0][j], x[1][j]], [y[0][j], y[1][j]], linewidth=0.1, c='black')

    ax.set(xlim=(0, 1), ylim=(1, 0))

    fig.colorbar(scatterLeft, ax=ax, label='Left', fraction=0.02, pad=0.1, location='left')
    fig.colorbar(scatterRight, ax=ax, label='Right', fraction=0.02, pad=0.1, location='right')

    plotTitle = createTitle(diagnose, plotName, subjectNum, currentTrial, subjectProcedure)
    ax.set_title(plotTitle)

    savePath = createSavePath(plotName, diagnose, subjectNum, currentTrial, subjectProcedure)
    fig.tight_layout()
    plt.savefig(savePath)

def plotGazePerTrial(fig, ax, subjectNum, subjectProcedure, trialStartIndex, trialEndIndex, currentTrial,
                     XGazePosLeftEye, YGazePosLeftEye, XGazePosRightEye, YGazePosRightEye,
                     meanDiameter, AOI, diagnose, plotName):

    XGazePosLeftEye = XGazePosLeftEye[trialStartIndex:trialEndIndex, :1]
    YGazePosLeftEye = YGazePosLeftEye[trialStartIndex:trialEndIndex, :1]
    XGazePosRightEye = XGazePosRightEye[trialStartIndex:trialEndIndex, :1]
    YGazePosRightEye = YGazePosRightEye[trialStartIndex:trialEndIndex, :1]
    meanDiameter = meanDiameter[trialStartIndex:trialEndIndex, :1]
    AOI = AOI[trialStartIndex:trialEndIndex, :1]

    XGazePosLeftEyes = []
    YGazePosLeftEyes = []

    XGazePosRightEyes = []
    YGazePosRightEyes = []

    for i in range(4):
        aoi = i + 1
        XGazePosLeftEyes.append(numpy.ma.masked_where(AOI != aoi, XGazePosLeftEye))
        YGazePosLeftEyes.append(numpy.ma.masked_where(AOI != aoi, YGazePosLeftEye))
        XGazePosRightEyes.append(numpy.ma.masked_where(AOI != aoi, XGazePosRightEye))
        YGazePosRightEyes.append(numpy.ma.masked_where(AOI != aoi, YGazePosRightEye))

    symbols = ['^', 's', 'x', '1']
    for i in range(4):
        scatterLeft = ax.scatter(XGazePosLeftEyes[i], YGazePosLeftEyes[i], s=10, c=meanDiameter, cmap='viridis',
                                 zorder=2, marker=symbols[i])
        scatterRight = ax.scatter(XGazePosRightEyes[i], YGazePosRightEyes[i], s=10, c=meanDiameter, cmap='seismic',
                                  zorder=2, marker=symbols[i])

        # x = [XGazePosLeftEyes[i], XGazePosRightEyes[i]]
        # y = [YGazePosLeftEyes[i], YGazePosRightEyes[i]]
        #
        # for j in range(len(XGazePosLeftEyes[i])):
        #     ax.plot([x[0][j], x[1][j]], [y[0][j], y[1][j]], linewidth=0.1, c='black')

    ax.set(xlim=(0, 1), ylim=(1, 0))

    fig.colorbar(scatterLeft, ax=ax, label='Left', fraction=0.02, pad=0.1, location='left')
    fig.colorbar(scatterRight, ax=ax, label='Right', fraction=0.02, pad=0.1, location='right')

    plotTitle = createTitle(diagnose, plotName, subjectNum, currentTrial, subjectProcedure)
    ax.set_title(plotTitle)

    savePath = createSavePath(plotName, diagnose, subjectNum, currentTrial, subjectProcedure)
    fig.tight_layout()
    plt.savefig(savePath)

def plotCursorPerTrial(fig, ax, subjectNum, subjectProcedure, trialStartIndex, trialEndIndex, currentTrial,
                       CursorX, CursorY, meanDiameter, AOI, diagnose, plotName):

    CursorX = CursorX[trialStartIndex:trialEndIndex, :1]
    CursorY = CursorY[trialStartIndex:trialEndIndex, :1]
    meanDiameter = meanDiameter[trialStartIndex:trialEndIndex, :1]
    AOI = AOI[trialStartIndex:trialEndIndex, :1]

    CursorXs = []
    CursorYs = []

    for i in range(4):
        aoi = i + 1
        CursorXs.append(numpy.ma.masked_where(AOI != aoi, CursorX))
        CursorYs.append(numpy.ma.masked_where(AOI != aoi, CursorY))

    scatter = 0
    symbols = ['^', 's', 'x', '1']
    for i in range(4):
        scatter = ax.scatter(CursorXs[i], CursorYs[i], s=10, c=meanDiameter, cmap='seismic',
                             zorder=2, marker=symbols[i])

    fig.colorbar(scatter, ax=ax)
    ax.set(xlim=(0, 1024), ylim=(768, 0))

    plotTitle = createTitle(diagnose, plotName, subjectNum, currentTrial, subjectProcedure)
    ax.set_title(plotTitle)

    savePath = createSavePath(plotName, diagnose, subjectNum, currentTrial, subjectProcedure)
    fig.tight_layout()
    plt.savefig(savePath)

def GetNumberAndListOfTrials(TrialProc):
    trialStartIndexes = [0]
    trialEndIndexes = []
    currentTrial = TrialProc[0]
    for i in range(TrialProc.size):
        if currentTrial != TrialProc[i]:
            trialStartIndexes.append(i)
            trialEndIndexes.append(i)
            currentTrial = TrialProc[i]

    trialEndIndexes.append(TrialProc.size)
    numberOfTrials = len(trialEndIndexes)
    return numberOfTrials, trialStartIndexes, trialEndIndexes

def createSavePath(plotName, diagnose, subjectNum, currentTrial, subjectProcedure):
    savePath = "plots\\subject_%d_%d-%s\\trial_%d" % (subjectNum, subjectProcedure, diagnose,
                                                      currentTrial)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    savePath = "plots\\subject_%d_%d-%s\\trial_%d\\%s_%d.png" % (subjectNum, subjectProcedure, diagnose,
                                                                 currentTrial,
                                                                 plotName, currentTrial)
    return savePath

def createTitle(diagnose, plotName, subjectNum, currentTrial, subjectProcedure):
    return '%s - %s: Subject - %d, Procedure - %d, Trial - %d'\
           % (diagnose, plotName, subjectNum, subjectProcedure, currentTrial)

def plotDataSummery(dataFrame):
    indexes = numpy.array(dataFrame.index)
    indexes = indexes.reshape(indexes.size, 1)
    plotDataSummeryAVG(dataFrame['time_AVG'], indexes, 'Time Span')
    plotDataSummeryAVG(dataFrame['meanDiameter_AVG'], indexes, 'Mean Diameter')
    plotDataSummeryAVG(dataFrame['volume_AVG'], indexes, 'Volume')
    plotDataSummeryAVG(dataFrame['volumeByArea_AVG'], indexes, 'Volume By Area')
    plotDataSummeryAVG(dataFrame['timeByArea_AVG'], indexes, 'Time Span By Area')
    plotDataSummeryAVG(dataFrame['meanDiameterByArea_AVG'], indexes, 'Mean Diameter By Area')
    plotDataSummeryAVG(dataFrame['focus_AVG'], indexes, 'Focus')
    plotDataSummeryAVG(dataFrame['diameterFocus_AVG'], indexes, 'Mean Diameter Focus')
    plotDataSummeryAVG(dataFrame['diameterNotFocus_AVG'], indexes, 'Mean Diameter Not Focus')


    return 0

def plotDataSummeryAVG(dataSeries, indexes, dataSeriesName):
    labels = ['AOI-1', 'AOI-2', 'AOI-3', 'AOI-4']
    trials = ['6', '10', '11']
    for i in range(3):
        fig, ax = plt.subplots()
        diagnostics = []
        for index in indexes:
            diagnostics.append(dataSeries[index][0][i])
        x = numpy.arange(len(labels))

        width = 0.1
        rects1 = ax.bar(x - 0.15, diagnostics[0], width, label=indexes[0][0])
        rects2 = ax.bar(x - 0.05, diagnostics[1], width, label=indexes[1][0])
        rects3 = ax.bar(x + 0.05, diagnostics[2], width, label=indexes[2][0])
        rects4 = ax.bar(x + 0.15, diagnostics[3], width, label=indexes[3][0])

        ax.set_ylabel(dataSeriesName)
        ax.set_title(dataSeriesName + ' - ' + trials[i])
        ax.set_xticks(x)
        ax.set_xticklabels(labels)

        # ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

        fig.tight_layout()

        savePath = "plots\\Summery"
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        savePath = "plots\\Summery\\%s_%s.png" % (dataSeriesName, trials[i])
        plt.savefig(savePath)
        # plt.show()

    return 0