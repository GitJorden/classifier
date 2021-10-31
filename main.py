import os

import DataSummery
import plotSubjectGraph
import Preprocess
import pandas
import numpy

noDiagnostic = [1, 2, 102, 103, 107, 110, 112, 113, 114, 115, 116, 119, 120, 121, 122, 124, 130,
                132, 133, 134, 135, 139, 141, 142, 146, 147, 160, 170, 171, 172, 175, 176, 182, 185, 186,
                44, 45, 5, 51, 57, 59, 60, 61, 62, 64, 66, 68, 75, 77, 78, 8, 84, 87, 905, 923]
ASD = [166, 180, 181, 52, 93, 94, 95]
LANG = [126, 127, 131, 136, 148, 153, 50, 53, 63, 73, 80, 83, 910]
SensoryMotoric = [104, 108, 111, 140, 143, 47, 58, 65, 81, 86]

#####################################################################
#                   Step - 01 - Preprocess The Data                 #
#####################################################################
#
# files_in_preprocess = os.listdir('in_preprocess')
# for file in files_in_preprocess:
#     print(file)
#     dataFrame = Preprocess.preprocess(file)

##################################################################
#                   Step - 01 - Process The Data                 #
##################################################################
#

# files_out_preprocess = os.listdir('out_preprocess')
#
# for file in files_out_preprocess:
#     print(file)
#     dataFrame = pandas.read_csv('out_preprocess\\' + file, sep='\t')
#     TETTime, CursorX, CursorY,\
#     XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye,\
#     DiameterPupilLeftEye, DistanceLeftEye, ValidityLeftEye,\
#     XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye,\
#     DiameterPupilRightEye, DistanceRightEye, ValidityRightEye,\
#     TrialId, TrialProc, AOI = Preprocess.GetDataColumns(dataFrame)
#     plotSubjectGraph.plotFileData(file,
#                                   TETTime, CursorX, CursorY,
#                                   XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye,
#                                   DiameterPupilLeftEye,
#                                   XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye,
#                                   DiameterPupilRightEye,
#                                   (DiameterPupilLeftEye + DiameterPupilRightEye) / 2, TrialProc, AOI,
#                                   noDiagnostic, ASD, LANG, SensoryMotoric)


#######################################################################
#                   Step - 01 - Process file for test                 #
#######################################################################

# dataFrame = Preprocess.preprocess('tobii_YARDEN-24-1.csv')

# dataFrame = pandas.read_csv('out_preprocess\\' + '180-1-explore-out.csv', sep='\t')
#
# TETTime, CursorX, CursorY,\
# XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye,\
# DiameterPupilLeftEye, DistanceLeftEye, ValidityLeftEye,\
# XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye,\
# DiameterPupilRightEye, DistanceRightEye, ValidityRightEye,\
# TrialId, TrialProc, AOI = Preprocess.GetDataColumns(dataFrame)
#
# plotSubjectGraph.plotFileData('180-1-explore-out.csv',
#                               TETTime, CursorX, CursorY,
#                               XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye,
#                               DiameterPupilLeftEye,
#                               XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye,
#                               DiameterPupilRightEye,
#                               (DiameterPupilLeftEye + DiameterPupilRightEye)/2, TrialProc, AOI,
#                               noDiagnostic, ASD, LANG, SensoryMotoric)

##################################################################
#                   Step - 03 - Get data summery                 #
##################################################################
#
# files_out_preprocess = os.listdir('out_preprocess')
# subjectsData = []
# for file in files_out_preprocess:
#     print(file)
#     dataFrame = pandas.read_csv('out_preprocess\\' + file, sep='\t')
#     TETTime, CursorX, CursorY,\
#     XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye,\
#     DiameterPupilLeftEye, DistanceLeftEye, ValidityLeftEye,\
#     XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye,\
#     DiameterPupilRightEye, DistanceRightEye, ValidityRightEye,\
#     TrialId, TrialProc, AOI = Preprocess.GetDataColumns(dataFrame)
#
#     subjectData = DataSummery.analyzeSubjectsData(file,
#                                     TETTime, CursorX, CursorY,
#                                     XGazePosLeftEye, YGazePosLeftEye, XCameraPosLeftEye, YCameraPosLeftEye,
#                                     DiameterPupilLeftEye,
#                                     XGazePosRightEye, YGazePosRightEye, XCameraPosRightEye, YCameraPosRightEye,
#                                     DiameterPupilRightEye,
#                                     (DiameterPupilLeftEye + DiameterPupilRightEye) / 2, TrialProc, AOI,
#                                     noDiagnostic, ASD, LANG, SensoryMotoric)
#     if subjectData is not None:
#         subjectsData.append(subjectData)
#
# DataSummery.dataSummery(subjectsData)


dataFrame = pandas.read_excel('exploreMoviesAll-81-1.xls')
print("finish")
