import random

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

alphabetExt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
               'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1',
               '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ']


def generateZero(size, filePath):
    content = ''
    for i in range(size):
        content += (alphabet[random.randint(0, len(alphabet) - 1)])
    open(filePath, 'w+').write(content)


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


def generateOne(size, signsProbs, filePath):
    rangesList = []
    for i in range(len(signsProbs) + 1):
        rangesList.append(0.0)
    for i in range(1, len(rangesList)):
        for j in range(i, len(rangesList)):
            rangesList[j] += signsProbs[i - 1][1]
    rangesList[-1] = 1
    content = ''
    for i in range(size):
        rand = random.random()
        randIndex = 0
        for j in range(len(rangesList) - 1):
            if rangesList[j] <= rand <= rangesList[j + 1]:
                randIndex = j
                break
        content += signsProbs[randIndex][0]
    open(filePath, 'w+').write(content)


# visualization of local 'markov' dict
# {
#     'a': {
#         'ab': 0.023526,
#         'ac': 0.015322,
#         'ad': 0.005354,
#         ...
#     }
#     ...
# }
def computeMarkovSource(inFilePath, markovLevel):
    markov = {}
    inFile = open(inFilePath, 'r')
    for line in inFile.readlines():
        for i in range(len(line) - markovLevel):
            signs = line[i:i + markovLevel]
            signsWithTail = line[i:i + markovLevel + 1]
            if signs not in markov:
                markov[signs] = {}
            if signsWithTail not in markov[signs]:
                markov[signs][signsWithTail] = 1
            else:
                markov[signs][signsWithTail] += 1
    for k, v in markov.items():
        sum = 0
        for k1, v1 in v.items():
            sum += v1
        markov[k] = {k1: v1 for k1, v1 in sorted({k2: v2 / sum for k2, v2 in v.items()}.items(), key=lambda item: item[1], reverse=True)}
    return markov


def generateUsingMarkov(size, markov, outFilePath):
    markovSize = len([k for k, v in markov.items()][0])
    rangeMarkov = {}
    for k, v in markov.items():
        rangeMarkov[k] = []
        probs = [v1 for k1, v1 in v.items()]
        for i in range(len(probs) + 1):
            rangeMarkov[k].append(0.0)
        for i in range(1, len(rangeMarkov[k])):
            for j in range(i, len(rangeMarkov[k])):
                rangeMarkov[k][j] += probs[i - 1]
    content = ''
    startString = 'probability'[-markovSize:]
    currentString = startString
    for i in range(size):
        rand = random.random()
        randIndex = 0
        for j in range(len(rangeMarkov[currentString]) - 1):
            if rangeMarkov[currentString][j] <= rand <= rangeMarkov[currentString][j + 1]:
                randIndex = j
                break
        content += [k for k, v in markov[currentString].items()][randIndex][-1]
        if len(content) < markovSize:
            currentString = startString[-(markovSize - len(content)):] + content
        else:
            currentString = content[-markovSize:]
    open(outFilePath, 'w+').write(content)


def countAvgWordLength(filePath):
    alphabetWithoutSpace = alphabetExt[0:-1]
    file = open(filePath, 'r')
    wordCount = 0
    wordsLengths = []
    wordStarted = False
    for line in file.readlines():
        for char in line:
            if char in alphabetWithoutSpace:
                if not wordStarted:
                    wordCount += 1
                    wordStarted = True
                    wordsLengths.append(1)
                else:
                    wordsLengths[wordCount - 1] += 1
            elif char == ' ':
                wordStarted = False
    return sum(wordsLengths)/wordCount


def printMarkovSource(markovSource):
    for k, v in markovSource.items():
        print('\'%s\': {' % k)
        for k1, v1 in v.items():
            print('\t\'%s\': %f' % (k1, v1))
        print('}')


if __name__ == '__main__':

    print('zad1')
    # generateZero(10000000, 'generatorZero.txt')
    print('Average word length for generatorZero: %.2f' % countAvgWordLength('generatorZero.txt'))
    print()

    print('zad2')
    signProbabilities = computeSignsProbabilities('../data/norm_wiki_sample.txt')
    print('Probabilities for each sign (based on norm_wiki_sample.txt)')
    for sign, probability in signProbabilities:
        print('\'%s\': %s' % (sign, probability))
    print()

    print('zad3')
    generateOne(10000000, signProbabilities, 'generatorOne.txt')
    print('Average word length for generatorOne: %.2f' % countAvgWordLength('generatorOne.txt'))
    print('Average word length for norm_wiki_sample.txt: %.2f' % countAvgWordLength('../data/norm_wiki_sample.txt'))
    print()

    print('zad4')
    markovSource1 = computeMarkovSource('norm_wiki_sample.txt', 1)
    markovSource1ForTwoMostPopularSigns = {' ': markovSource1[' '], 'e': markovSource1['e']}
    printMarkovSource(markovSource1ForTwoMostPopularSigns)
    print()

    print('zad5')
    # printMarkovSource(markovSource1)
    generateUsingMarkov(10000000, markovSource1, 'generatorMarkov1.txt')
    print('Average word length for generatorMarkov1: %.2f' % countAvgWordLength('generatorMarkov1.txt'))

    markovSource3 = computeMarkovSource('norm_wiki_sample.txt', 3)
    # printMarkovSource(markovSource3)
    generateUsingMarkov(10000000, markovSource3, 'generatorMarkov3.txt')
    print('Average word length for generatorMarkov3: %.2f' % countAvgWordLength('generatorMarkov3.txt'))

    markovSource5 = computeMarkovSource('norm_wiki_sample.txt', 5)
    # printMarkovSource(markovSource5)
    generateUsingMarkov(10000000, markovSource5, 'generatorMarkov5.txt')
    print('Average word length for generatorMarkov5: %.2f' % countAvgWordLength('generatorMarkov5.txt'))
