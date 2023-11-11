import cv2
from cv2 import VideoCapture
import numpy as np
from pygrabber.dshow_graph import FilterGraph
import PySimpleGUI as sg
import random


def main():
    scores = gen_random_scores()
    previousThrow = 0

    #pins are numbered followed by cooordinates [x1, x2, y1, y2] should be 6x6 squares
    pinData = {}
    pinData[7] = [14, 20, 38, 44]
    pinData[4] = [28, 34, 38, 44]
    pinData[2] = [48, 54, 38, 44]
    pinData[1] = [75, 81, 38, 44]
    pinData[8] = [41, 47, 38, 44]
    pinData[5] = [60, 66, 38, 44]
    pinData[3] = [83, 89, 38, 44]
    pinData[9] = [69, 75, 38, 44]
    pinData[6] = [89, 95, 38, 44]
    pinData[10] = [94, 100, 38, 44]

    scores = play_frame(0, 1, 2, scores, pinData)
    print(scores)

    # pins = get_current_pin_count(pinData)
    # sg.theme('DarkAmber')
    # toprow = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    # rows = [[str(scores[0]) + '  |  ' + str(scores[1]), str(scores[3]) + '  |  ' + str(scores[4]), str(scores[6]) + '  |  ' + str(scores[7]), str(scores[9]) + '  |  ' + str(scores[10]), str(scores[12]) + '  |  ' + str(scores[13]), str(scores[15]) + '  |  ' + str(scores[16]), str(scores[18]) + '  |  ' + str(scores[19]), str(scores[21]) + '  |  ' + str(scores[22]), str(scores[24]) + '  |  ' + str(scores[25]), str(scores[27]) + '  |  ' + str(scores[28]) + '  |  ' + str(scores[29])],
    #         [str(scores[2]) + "      ", str(scores[5]) + "      ", str(scores[8]) + "      ", str(scores[11]) + "      ", str(scores[14]) + "      ", str(scores[17]) + "      ", str(scores[20]) + "      ", str(scores[23]) + "      ", str(scores[26]) + "      ", str(scores[30]) + "            "]]
    # tbl = sg.Table(key='-TABLE-', values=rows, headings=toprow, expand_x=True, expand_y=True, justification='center')
    # layout = [[sg.Text("Total pins up: " + str(pins), key='-TOTALPINS-')],
    #         [tbl],
    #         [sg.Image('viewbounding.png', key='-BOUNDINGIMG-')],
    #         [sg.Button("Score"), sg.Button("Update"), sg.Button("Cancel")]]
    #
    # window = sg.Window('pysimple test', layout, size=(1920,1080), resizable=True, element_justification='center')
    # while True:
    #     event, value = window.read()
    #     if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
    #         break
    #     elif event == 'Update':
    #         scores = gen_random_scores()
    #         pins = get_current_pin_count(pinData)
    #         previousThrow = score_throw(previousThrow, pinData)
    #         rows = [[str(scores[0]) + '  |  ' + str(scores[1]), str(scores[3]) + '  |  ' + str(scores[4]),
    #                  str(scores[6]) + '  |  ' + str(scores[7]), str(scores[9]) + '  |  ' + str(scores[10]),
    #                  str(scores[12]) + '  |  ' + str(scores[13]), str(scores[15]) + '  |  ' + str(scores[16]),
    #                  str(scores[18]) + '  |  ' + str(scores[19]), str(scores[21]) + '  |  ' + str(scores[22]),
    #                  str(scores[24]) + '  |  ' + str(scores[25]),
    #                  str(scores[27]) + '  |  ' + str(scores[28]) + '  |  ' + str(scores[29])],
    #                 [str(scores[2]) + "      ", str(scores[5]) + "      ", str(scores[8]) + "      ",
    #                  str(scores[11]) + "      ", str(scores[14]) + "      ", str(scores[17]) + "      ",
    #                  str(scores[20]) + "      ", str(scores[23]) + "      ", str(scores[26]) + "      ",
    #                  str(scores[30]) + "            "]]
    #         window['-TABLE-'].update(values=rows)
    #         window['-BOUNDINGIMG-'].update("viewbounding.png")
    #         window['-TOTALPINS-'].update("Total pins up: " + str(pins))
    #         window.refresh()
    #         print("updating score")
    #         continue
    #     elif event == 'Score':
    #         print("Scoring")
    #         previousThrow = score_throw(previousThrow, pinData)
    #         continue

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def play_frame(throw1, throw2, scoreNum, scores, pinData):
    throw = throw1
    while throw <= throw2:
        if throw is throw1:
            scores[throw] = 10 - get_current_pin_count(pinData)
        # scores[throw] = get_current_pin_count(pinData)
        if throw is throw2:
            secondFrame = scores[throw1] - get_current_pin_count(pinData)
            score = scores[throw1] + secondFrame
            scores[scoreNum] = score
        input("Enter when ready for next frame")
        throw += 1
    return scores


def score_throw(previousTotal, pinData):
    totalUp = get_current_pin_count(pinData)
    if previousTotal is None:
        hit = 10 - totalUp
    else:
        hit = 10 - totalUp
        hit + previousTotal

    print("Num pins hit: " + str(hit))
    return hit


def get_current_pin_count(pinData):
    cam_port = 1
    cam = VideoCapture(cam_port)
    result, image = cam.read()
    while not result:
        result, image = cam.read()
    # cv2.imshow("webcam", image)
    originalImage = image
    cv2.imwrite("original.png", originalImage)

    image = resize_image(originalImage)
    blackAndWhiteImage = convert_to_bw(image)
    cv2.imwrite("blackandwhite.png", blackAndWhiteImage)
    pins = countPins(blackAndWhiteImage, pinData)
    drawViews(image, pinData)
    return pins


def gen_random_scores():
    scores = []
    for i in range(31):
        scores.append(" ")
        # scores.append(random.randint(0, 9))
    return scores


def get_available_cameras():
    devices = FilterGraph().get_input_devices()
    available_cameras = {}

    for device_index, device_name in enumerate(devices):
        available_cameras[device_index] = device_name

    print(available_cameras)


def resize_image(inputImage):
    scale = 20
    width = int(inputImage.shape[1] * scale / 100)
    height = int(inputImage.shape[0] * scale / 100)
    dim = (width, height)
    return cv2.resize(inputImage, dim, interpolation=cv2.INTER_AREA)


def convert_to_bw(inputImage):
    grayImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    (thresh, outputImage) = cv2.threshold(grayImage, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return outputImage


def pin_up(inputImage, pinnumber, pinStartX, pinStartY, pinEndX, pinEndY):
    pin = inputImage[pinEndX:pinEndY, pinStartX:pinStartY]
    numWhitePixPin = np.sum(pin == 255)
    pinSize = pin.size
    pinProb = numWhitePixPin / pinSize
    # print("Pin ", pinnumber, " Percent White: {:.2f}%".format((numWhitePixPin / pinSize)*100))

    if pinProb > 0.5:
        pinStatus = True
    else:
        pinStatus = False

    # print(pinnumber, " status: ", pinStatus)

    return pinStatus


def drawViews(image, data):
    finalImage = image
    for pinNum in data:
        finalImage = cv2.rectangle(finalImage, (data[pinNum][0], data[pinNum][2]), (data[pinNum][1], data[pinNum][3]), (0, 0, 255), 1)
    finalImage = cv2.resize(finalImage, (1280, 720), interpolation=cv2.INTER_AREA)
    cv2.imwrite("viewbounding.png", finalImage)


def countPins(image, data):
    pinCounts = {}
    for pinNum in data:
        if pin_up(image, pinNum, data[pinNum][0], data[pinNum][1], data[pinNum][2], data[pinNum][3]):
            pinCounts[pinNum] = 1
        else:
            pinCounts[pinNum] = 0

    total = 0
    for pinNum in pinCounts:
        if pinCounts[pinNum] == 1:
            total = total + 1

    print("Total pins up: ", total)
    return total


def drawScoreCard(s):
    print("_______________________________________________________________________________________________" +
          "\n|   1    |   2    |   3    |   4    |   5    |   6    |   7    |   8    |   9    |     10     |" +
          "\n-----------------------------------------------------------------------------------------------" +
          "\n|    |   |    |   |    |   |    |   |    |   |    |   |    |   |    |   |    |   |    |   |   |" +
          "\n|        |        |        |        |        |        |        |        |        |            |" +
          "\n-----------------------------------------------------------------------------------------------")


main()
