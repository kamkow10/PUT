from bitarray import bitarray

alphabetExt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
               'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1',
               '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ']

BIT_SIZE = 6


def computeSignsProbabilities(filePath):
    counterList = []
    for i in range(len(alphabetExt)):
        counterList.append(0)
    inFile = open(filePath, 'r')
    for line in inFile.readlines():
        for sign in line:
            counterList[alphabetExt.index(sign)] += 1
    sumOfSigns = sum(counterList)
    signsProbs = []
    for i in range(len(alphabetExt)):
        signsProbs.append([alphabetExt[i], counterList[i] / sumOfSigns])
    signsProbs.sort(key=lambda elem: elem[1], reverse=True)
    return signsProbs


def intToBin(value):
    binStr = bin(value)[2:]
    for i in range(BIT_SIZE - len(binStr)):
        binStr = '0' + binStr
    return bitarray(binStr)


def codeToStr(bitArray):
    return bitArray.__str__().split('\'')[1]


def intToBitStr(value):
    return codeToStr(intToBin(value))


def create(signsProbs):
    codes = {}
    code = 0
    for sign, prob in signsProbs:
        codes[sign] = intToBitStr(code)
        code += 1
    return codes


def encode(codes, filePath):
    file = open(filePath, 'r')
    encodedLines = ''
    for line in file.readlines():
        for sign in line:
            encodedLines += codes[sign]
    return encodedLines


def decode(codes, encodedLines):
    reverseCodes = {v: k for k, v in codes.items()}
    decodedLines = ''
    for code in [(encodedLines[i:i+BIT_SIZE]) for i in range(0, len(encodedLines), BIT_SIZE)]:
        decodedLines += reverseCodes[code]
    return decodedLines


def save(codes, encodedLines, dir):
    codeFile = open(dir + '/codeFile', 'w')
    for sign, code in codes.items():
        codeFile.writelines(sign + code + '\n')
    encodedFile = open(dir + '/encodedFile', 'wb')
    encodedLines += '111111'
    bitarray(encodedLines).tofile(encodedFile)
    codeFile.close()
    encodedFile.close()


def load(encodedFilePath, codeFilePath):
    codeFile = open(codeFilePath, 'r')
    codes = {}
    for line in codeFile.readlines():
        codes[line[0]] = line[1:-1]
    encodedFile = open(encodedFilePath, 'rb')
    encodedBitArray = bitarray()
    encodedBitArray.fromfile(encodedFile)
    allEncodedLines = codeToStr(encodedBitArray)
    encodedLines = ''
    for code in [(allEncodedLines[i:i+BIT_SIZE]) for i in range(0, len(allEncodedLines), BIT_SIZE)]:
        if code == '111111':
            break
        encodedLines += code
    return codes, encodedLines


if __name__ == '__main__':
    signProbs = computeSignsProbabilities('../data/generatorOne.txt')
    codes = create(signProbs)
    # encodedLines = encode(codes, '../data/norm_wiki_sample.txt')
    encodedLines = encode(codes, '../data/norm_wiki_sample.txt')
    # decodedLines = decode(codes, encodedLines)
    save(codes, encodedLines, 'encodedTest')
    codes, encodedLinesFromFile = load('encodedTest/encodedFile', 'encodedTest/codeFile')

    print('Is compression correct: {}'
          .format(open('../data/norm_wiki_sample.txt', 'r').readlines()[0] == decode(codes, encodedLinesFromFile))
    )

    print()
