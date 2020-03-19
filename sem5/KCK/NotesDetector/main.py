from copy import deepcopy

import cv2
import skimage.morphology as mp
import numpy as np
from PIL import Image
import os
import enum


class Notes(enum.Enum):
    TREBLE_CLEF = 'klucz wiolinowy'
    BASS_CLEF = 'klucz basowy'
    NOTE = 'nuta'
    HALF_NOTE = 'półnuta'
    QUARTER_NOTE = 'ćwierć nuta'
    EIGHTH_NOTE = 'ósemka'
    PAUSE = 'pauza'
    UNKNOWN = 'nieznana'


INPUT_LOCATION = 'input/'
OUTPUT_LOCATION = 'output/'

lineDeletingMasks = [
    [
        [0,     0,      0],
        [255,   255,    255],
        [255,   255,    255]
    ],
    [
        [255,   255,    255],
        [255,   255,    255],
        [0,     0,      0]
    ],
    [
        [0,     0,      0],
        [0,     0,      0],
        [255,   255,    255]
    ],
    [
        [255,   255,    255],
        [0,     0,      0],
        [0,     0,      0]
    ],
    [
        [0,     0,      0],
        [255,   255,    255],
        [0,     0,      0]
    ]
]


def changeAllInputsDefinitions(numberOfFiles, param):
    for i in range(1, numberOfFiles + 1):
        inputImage = Image.open(INPUT_LOCATION + i.__str__() + '.jpg')
        width, height = inputImage.size
        if (width > param) or (height > param):
            if (width > height):
                diff = width - param
                width = width - diff
                height = height * (width / (width + diff))
            else:
                diff = height - param
                height = height - diff
                width = width * (height / (height + diff))
            width = width.__int__()
            height = height.__int__()
            inputImage = inputImage.resize((width, height))
            inputImage.save(INPUT_LOCATION + i.__str__() + '.jpg')


def getImageSize(path):
    inputImage = Image.open(path)
    width, height = inputImage.size
    return width, height


def thresh(img, t):
    binary = (img > t) * 255
    binary = np.uint8(binary)
    return binary


def contrast(img, perc=0):
    MIN = np.percentile(img, perc)
    MAX = np.percentile(img, 100 - perc)
    norm = (img - MIN) / (MAX - MIN)
    img[norm[:, :] > 1] = 255
    img[norm[:, :] < 0] = 0

    return img


def negative(img):
    black = img[:, :] == 0
    white = img[:, :] == 255
    img[black] = 255
    img[white] = 0
    return img


def deleteNextToLines(lines, crtDist):
    mainLines = []
    for line in lines:
        for r, theta in line:
            mainLines.append([r, theta])
            for rad, angle in mainLines:
                if ((abs(r - rad) <= crtDist) and (r != rad)):
                    mainLines.remove([r, theta])
                    break
    return mainLines


def smartDeleteNextToLines(lines, startCrtDist):
    if (startCrtDist <= 0):
        print('ERROR: startCrtDist must be > 0')
        return 0
    param = startCrtDist - 1
    newLines = lines
    while (True):
        param += 1
        newLines = deleteNextToLines(lines, param)
        foundedLines = countLines(newLines)
        if (foundedLines == 20):
            break
    return newLines


def getStaves(lines):
    lines.sort(key=lambda x: x[0])
    groupedLines = []
    staves = len(lines) / 5
    for i in range(int(staves)):
        groupedLines.append([])
        for j in range(0 + (5 * i), 5 + (5 * i)):
            groupedLines[i].append(lines[j][0])
    return groupedLines


def countLines(lines):
    foundLines = 0
    for i in lines:
        foundLines += 1
    return foundLines


def makePictureWithDetectedLines(lines, mainImage, saveLocation, detectedLinesFileName):
    for r, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * r
        y0 = b * r
        x1 = int(x0 + 4000 * (-b))
        y1 = int(y0 + 4000 * (a))
        x2 = int(x0 - 4000 * (-b))
        y2 = int(y0 - 4000 * (a))
        cv2.line(mainImage, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imwrite(saveLocation + detectedLinesFileName, mainImage)


def lineDeleting(input, width, height, masks):
    binaryImage = deepcopy(input)
    for m in masks:
        for i in range(height):
            if ((i != 0) and (i != height - 1)):
                for j in range(width):
                    if ((j != 0) and (j != width - 1)):
                        if (binaryImage[i][j] == 255):
                            newI = deepcopy(i)
                            if m == lineDeletingMasks[3]:
                                newI += 1
                            elif m == lineDeletingMasks[2]:
                                newI -= 1
                            neighbourhood = [
                                [binaryImage[newI - 1][j - 1], binaryImage[newI - 1][j], binaryImage[newI - 1][j + 1]],
                                [binaryImage[newI][j - 1], binaryImage[newI][j], binaryImage[newI][j + 1]],
                                [binaryImage[newI + 1][j - 1], binaryImage[newI + 1][j], binaryImage[newI + 1][j + 1]],
                            ]
                            if (neighbourhood == m):
                                input[i][j] = 0
    return input


def findAllNeighbours(image, width, height, chosen, posX, posY):
    potencials = [
        [image[posX - 1][posY - 1], posX - 1,   posY - 1],
        [image[posX - 1][posY],     posX - 1,   posY],
        [image[posX - 1][posY + 1], posX - 1,   posY + 1],

        [image[posX][posY - 1],     posX,       posY - 1],
        [image[posX][posY],         posX,       posY],
        [image[posX][posY + 1],     posX,       posY + 1],

        [image[posX + 1][posY - 1], posX + 1,   posY - 1],
        [image[posX + 1][posY],     posX + 1,   posY],
        [image[posX + 1][posY + 1], posX + 1,   posY + 1]
    ]
    neighbours = []
    chosen[posX][posY] = True
    for potencial in potencials:
        if (not chosen[potencial[1]][potencial[2]]) and (potencial[0] == 255):
            newNeighbours = findAllNeighbours(image, width, height, chosen, potencial[1], potencial[2])
            if not (newNeighbours is None):
                for nb in newNeighbours:
                    neighbours.append(nb)
    neighbours.append([posX, posY])
    return neighbours


def getElementsFromImage(image, width, height):
    elements = []
    alreadyChosen = []
    for row in range(height):
        alreadyChosen.append([])
        for col in range(width):
            alreadyChosen[row].append(False)
    for row in range(height):
        for col in range(width):
            if (not alreadyChosen[row][col]) and (image[row][col] == 255):
                newElement = findAllNeighbours(image, width, height, alreadyChosen, row, col)
                elements.append(newElement)
    return elements


def deletePixelsOnEdges(image, width, height):
    for i in range(width):
        image[0][i] = 0
        image[height - 1][i] = 0
    for j in range(height):
        image[j][0] = 0
        image[j][width - 1] = 0
    return image


def deleteSmallElements(image, elements, crtSize):
    bigElements = []
    for elem in elements:
        if len(elem) < crtSize:
            for pix in elem:
                image[pix[0]][pix[1]] = 0
        else:
            bigElements.append(elem)
    return bigElements


def getAverageDistanceBetweenLines(staves):
    mainContainer = []
    for stave in staves:
        stave.sort()
        staveContainer = []
        for i in range(len(stave) - 1):
            staveContainer.append(abs(stave[i] - stave[i + 1]))
        staveAvg = np.average(staveContainer)
        mainContainer.append(staveAvg)
    return int(np.average(mainContainer))


def makeLowDefinitionImage(path, crtSize):
    inputImage = Image.open(path)
    width, height = inputImage.size
    percents = 100.0
    if (width > crtSize) or (height > crtSize):
        if (width > height):
            diff = width - crtSize
            percents = (width - diff) / width
            width = width - diff
            height = height * (width / (width + diff))
        else:
            diff = height - crtSize
            percents = (height - diff) / height
            height = height - diff
            width = width * (height / (height + diff))
        width = width.__int__()
        height = height.__int__()
        inputImage = inputImage.resize((width, height))
        inputImage.save(path)
    return percents


def scaleStaves(staves, newEdges, imgWidth, imgHeight):
    for stave in staves:
        for i in range(len(stave)):
            stave[i] = int(stave[i] * percentOfBasicImg)
    for stave in staves:
        for i in range(5):
            for j in range(imgWidth):
                newEdges[int(stave[i])][j] = 200


def divideImageToWorkSpaces(image, imgHeight, staves):
    imgCopy = deepcopy(image)
    dividedParts = []
    separatingHeights = []
    separatingHeights.append(0)
    for i in range(3):
        diff = abs(staves[i][4] - staves[i + 1][0])
        separatingHeights.append(staves[i][4] + int(diff / 2))
    separatingHeights.append(imgHeight)
    for j in range(len(separatingHeights) - 1):
        part = []
        for row in range(separatingHeights[j], separatingHeights[j + 1]):
            part.append(imgCopy[row][:])
        dividedParts.append(np.array(part))
    return dividedParts


def addAtribiutesToElements(elements):
    newElements = []
    for element in elements:
        xs = []
        ys = []
        for x, y in element:
            xs.append(x)
            ys.append(y)
        newElements.append(
            {
                'width': max(ys) - min(ys),
                'height': max(xs) - min(xs),
                'top': min(xs),
                'right': max(ys),
                'bottom': max(xs),
                'left': min(ys),
                'type': Notes.UNKNOWN,
                'pitch': '',
                'pos': 0,
                'size': len(element),
                'pixels': element
            }
        )
    newElements.sort(key=lambda i: i['left'])
    return newElements


def translateToPitch(i):
    if i == 0:
        return 'F'
    if i == 0.5:
        return 'E'
    if i == 1:
        return 'D'
    if i == 1.5:
        return 'C'
    if i == 2:
        return 'H'
    if i == 2.5:
        return 'A'
    if i == 3:
        return 'G'
    if i == 3.5:
        return 'F'
    if i == 4:
        return 'E'
    else:
        return 'still unknown'


def setPitch(elem, staves):
    copyStaves = deepcopy(staves)
    value = 0
    for stave in reversed(copyStaves):
        if elem['bottom'] >= (stave + 3):
            value = staves.index(stave)
            break
        elif elem['bottom'] >= (stave - 1):
            value = staves.index(stave) - 0.5
            break
    elem['pos'] = value
    elem['pitch'] = translateToPitch(value)


def findMiddlePosition(elem, staves):
    top = []
    bottom = []
    for stave in staves:
        top.append([abs(elem['top'] - stave), stave])
        bottom.append([abs(elem['bottom'] - stave), stave])
    topStave = min(top, key=lambda i: i[0])
    bottomStave = min(bottom, key=lambda i: i[0])
    topStave = staves.index(topStave[1])
    bottomStave = staves.index(bottomStave[1])
    return (topStave + bottomStave)/2


def calculateRatio(elem, vertical, horizontal):
    if vertical and horizontal:
        print("ERROR: can not calculate vertical and horizontal ratio in the same time.")
        return 0
    elif not vertical and not horizontal:
        print("ERROR: no parameters have been chosen for calculateRatio function.")
    elif vertical:
        perOne = 'left'
        perTwo = 'right'
        size = 'width'
    else:
        perOne = 'top'
        perTwo = 'bottom'
        size = 'height'
    perimeterOne = elem[perOne]
    perimeterTwo = elem[perTwo]
    mid = perimeterOne + int(elem[size]/2)
    firstSize = 0
    secondSize = 0
    up = 0
    if not mid == (elem[size]/2):
        up += 1
    for x, y in elem['pixels']:
        chosen = y
        if horizontal:
            chosen = x
        if (chosen >= perimeterOne) and (chosen <= mid):
            firstSize += 1
        elif (chosen > mid+up) and (chosen <= perimeterTwo):
            secondSize += 1
    return int((firstSize/secondSize)*100)
    

def isRatioBetween(ratio, variation):
    return (ratio >= (100-variation)) and (ratio <= (100+variation))


def cutElement(elem, which):
    mid = 0
    if (which == 'left') or (which == 'right'):
        mid = elem['left'] + int(elem['width']/2)
    elif (which == 'top') or (which == 'bottom'):
        mid = elem['top'] + int(elem['height']/2)
    e1 = []
    for x, y in elem['pixels']:
        if ((which == 'left') and (y <= mid)) or ((which == 'right') and (y > mid)) or ((which == 'top') and (x <= mid)) or ((which == 'bottom') and (x > mid)):
            e1.append([x, y])
    newElem = deepcopy(elem)
    newElem['pixels'] = e1
    newElem['size'] = len(e1)
    return newElem


def ratioOfBlackPixelsInMiddle(elem):
    mid = elem['left'] + int(elem['width']/2)
    countB = 0
    countW = 0
    for x in range(elem['top'], elem['bottom'] + 1):
        if elem['pixels'].count([x, mid]):
            countW += 1
        else:
            countB += 1
    return  int((countB/countW)*100)


def MAGIC_FUNCTION(elements, staves, avg):
    # deleting small first elements
    while elements[0]['size'] < elements[1]['size']:
        elements.remove(elements[0])

    # identifying first note
    firstNote = elements[0]
    if (firstNote['top'] < staves[0]) and (firstNote['bottom'] > staves[4]):
        firstNote['type'] = Notes.TREBLE_CLEF
    if (firstNote['type'] == Notes.UNKNOWN) and (firstNote['height'] < (avg*4)) and (firstNote['height'] > (avg*2.5)):
        firstNote['type'] = Notes.BASS_CLEF

    # identifying rest of notes
    for elem in elements:
        if elem['type'] == Notes.UNKNOWN:
            if elem['height'] <= (avg*1.6):
                elem['type'] = Notes.NOTE
                setPitch(elem, staves)
            elif (elem['height'] <= (avg*3)) and (elem['height'] >= (avg*1.8)):
                hor = calculateRatio(elem, False, True)
                topVer = calculateRatio(cutElement(elem, 'top'), True, False)
                bottomVer = calculateRatio(cutElement(elem, 'bottom'), True, False)
                if (topVer <= 40) and (bottomVer > 160):
                    elem['type'] = Notes.EIGHTH_NOTE
                    setPitch(elem, staves)
                elif hor < 90:
                    setPitch(elem, staves)
                    e = cutElement(elem, 'bottom')
                    e['top'] += int(e['height']/2)
                    ratio = ratioOfBlackPixelsInMiddle(e)
                    if ratio > 35:
                        elem['type'] = Notes.HALF_NOTE
                    else:
                        elem['type'] = Notes.QUARTER_NOTE
                elif findMiddlePosition(elem, staves) == 1.5:
                    elem['type'] = Notes.PAUSE
                    elem['pos'] = 1.5


# ================================================================================
# ============================== MAIN ============================================
# ================================================================================

if __name__ == '__main__':
    # -- resizing images to smaller definitions ------------------------------------
    nrOfImg = 4
    changeAllInputsDefinitions(nrOfImg, 800)

    for imgNr in range(1, nrOfImg+1):
        print("--------- IMAGE NO " + imgNr.__str__() + " --------------------------------------------------------")

        # -- reading and preparing image ----------------------------------------------
        directory = os.path.join("E:\\", "INFORMATYKA", "Python", "KCK",
                                 "PROJEKT_CzytnikNut", "output", imgNr.__str__())
        if not os.path.exists(directory):
            os.mkdir(directory)
        img = cv2.imread(INPUT_LOCATION + imgNr.__str__() + '.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = contrast(gray, 8)
        cv2.imwrite(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + '-1.jpg', gray)
        thresh_param = np.median(gray) - 30
        edges = thresh(gray, thresh_param)
        edges = negative(edges)
        cv2.imwrite(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + '-2.jpg', edges)

        # -- finding lines ------------------------------------------------------------
        imgWidth, imgHeight = getImageSize(INPUT_LOCATION + imgNr.__str__() + '.jpg')
        lineLengthParameter = int(imgWidth * 1/3)
        lines = cv2.HoughLines(edges, 1, 3*np.pi / 180, lineLengthParameter)
        lines = smartDeleteNextToLines(lines, 1)
        makePictureWithDetectedLines(lines, img, OUTPUT_LOCATION + imgNr.__str__() + '/', imgNr.__str__() + '-3.jpg')

        # -- grouping -----------------------------------------------------------------
        staves = getStaves(lines)
        avgDist = getAverageDistanceBetweenLines(staves)

        # -- deleting lines ------------------------------------------------------------
        edges = lineDeleting(edges, imgWidth, imgHeight, lineDeletingMasks[0:4])
        edges = lineDeleting(edges, imgWidth, imgHeight, [lineDeletingMasks[4]])
        edges = deletePixelsOnEdges(edges, imgWidth, imgHeight)

        cv2.imwrite(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + '-4.jpg', edges)
        elements = getElementsFromImage(edges, imgWidth, imgHeight)
        elements = deleteSmallElements(edges, elements, int(avgDist) * 2)
        cv2.imwrite(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + '-5.jpg', edges)

        # -- finding elements (notes) on picture ---------------------------------------
        edges = mp.dilation(edges)
        edges = mp.dilation(edges)
        edges = mp.dilation(edges)
        cv2.imwrite(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + '-6.jpg', edges)

        smallImagePath = OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + '-6.jpg'
        cv2.imwrite(smallImagePath, edges)
        percentOfBasicImg = makeLowDefinitionImage(smallImagePath, 400)

        img = cv2.imread(smallImagePath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = thresh(gray, thresh_param)
        imgWidth, imgHeight = getImageSize(smallImagePath)

        newEdges = deepcopy(edges)
        scaleStaves(staves, newEdges, imgWidth, imgHeight)
        cv2.imwrite(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + '-7.jpg', newEdges)

        workSpaces = divideImageToWorkSpaces(edges, imgHeight, staves)
        directory = os.path.join("E:\\", "INFORMATYKA", "Python", "KCK", "PROJEKT_CzytnikNut", "output", imgNr.__str__(), imgNr.__str__() + 'staves')
        nr = 0
        wsSizes = []
        for workspace in workSpaces:
            nr += 1
            if not os.path.exists(directory):
                os.mkdir(directory)
            cv2.imwrite(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + 'staves/' + imgNr.__str__() + '-' + nr.__str__() + '.jpg', workspace)
            wsWidth, wsHeight = getImageSize(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + 'staves/' + imgNr.__str__() + '-' + nr.__str__() + '.jpg')
            wsSizes.append([wsWidth, wsHeight])

        copyWorkSpaces = deepcopy(workSpaces)
        nr = 0
        for w in range(len(copyWorkSpaces)):
            nr += 1
            sumOfHeights = 0
            for h in range(w):
                sumOfHeights += wsSizes[h][1]
            for i in range(5):
                for j in range(imgWidth):
                    copyWorkSpaces[w][int(staves[w][i] - sumOfHeights)][j] = 150
                staves[w][i] -= sumOfHeights
            cv2.imwrite(OUTPUT_LOCATION + imgNr.__str__() + '/' + imgNr.__str__() + 'staves/' + imgNr.__str__() + '-' + nr.__str__() + '-lines.jpg', copyWorkSpaces[w])

        ind = -1
        for workspace in workSpaces:
            ind += 1
            wsElements = addAtribiutesToElements(getElementsFromImage(workspace, wsSizes[ind][0], wsSizes[ind][1]))
            wsStaves = staves[ind]
            print('Stave #' + (ind+1).__str__() + ' - - - - - - - - - - -')
            avgDist = getAverageDistanceBetweenLines([wsStaves])
            MAGIC_FUNCTION(wsElements, wsStaves, avgDist)
            for elem in wsElements:
                print((wsElements.index(elem)+1).__str__() + ':' + '\t' + elem['type'].value)
                print('\t' + elem['pitch'] + ' ' + elem['pos'].__str__())
            print('\n')


