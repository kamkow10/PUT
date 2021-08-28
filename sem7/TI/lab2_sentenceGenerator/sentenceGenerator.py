import random


def computeMarkovSource(inFilePath, markovLevel):
    markov = {}
    inFile = open(inFilePath, 'r')
    for line in inFile.readlines():
        splitLine = line.split()
        for i in range(len(splitLine) - markovLevel):
            words = wordListToString(splitLine[i:i + markovLevel])
            wordsWithTail = wordListToString(splitLine[i:i + markovLevel + 1])
            if words not in markov:
                markov[words] = {}
            if wordsWithTail not in markov[words]:
                markov[words][wordsWithTail] = 1
            else:
                markov[words][wordsWithTail] += 1
    for k, v in markov.items():
        sum = 0
        for k1, v1 in v.items():
            sum += v1
        markov[k] = {k1: v1 for k1, v1 in
                     sorted({k2: v2 / sum for k2, v2 in v.items()}.items(), key=lambda item: item[1], reverse=True)}
    return markov


def wordListToString(wordList):
    result = ''
    for word in wordList:
        result += word + ' '
    return result[:-1]


def generateUsingMarkov(size, markov, outFilePath):
    markovSize = len([k for k, v in markov.items()][0].split())
    rangeMarkov = {}
    for k, v in markov.items():
        rangeMarkov[k] = []
        probs = [v1 for k1, v1 in v.items()]
        for i in range(len(probs) + 1):
            rangeMarkov[k].append(0.0)
        for i in range(1, len(rangeMarkov[k]) - 1):
            rangeMarkov[k][i] += probs[i - 1]
            rangeMarkov[k][i + 1] += rangeMarkov[k][i]
        rangeMarkov[k][-1] = 1
    content = ''
    if markovSize == 1:
        startWords = 'probability'
    elif markovSize == 2:
        startWords = 'probability of'
    else:
        print('bad markov source')
        return
    currentString = startWords
    for i in range(size):
        rand = random.random()
        randIndex = 0
        for j in range(len(rangeMarkov[currentString]) - 1):
            if rangeMarkov[currentString][j] <= rand <= rangeMarkov[currentString][j + 1]:
                randIndex = j
                break
        content += [k for k, v in markov[currentString].items()][randIndex].split()[-1] + ' '
        if len(content.split()) < markovSize:
            currentString = wordListToString(startWords.split()[-(markovSize - len(content.split())):]) + ' ' + wordListToString(content.split())
        else:
            currentString = wordListToString(content.split()[-markovSize:])
    open(outFilePath, 'w+').write(content)


def printMarkovSource(markovSource):
    for k, v in markovSource.items():
        print('\'%s\': {' % k)
        for k1, v1 in v.items():
            print('\t\'%s\': %f' % (k1, v1))
        print('}')


def getWordsCount(filePath):
    wordCount = {}
    file = open(filePath, 'r')
    for line in file.readlines():
        for word in line.split():
            if word not in wordCount:
                wordCount[word] = 1
            else:
                wordCount[word] += 1
    return {k: v for k, v in sorted(wordCount.items(), key=lambda elem: elem[1], reverse=True)}


def getWordsProbabilities(filePath):
    wordCount = getWordsCount(filePath)
    sumOfWords = sum([v for k, v in wordCount.items()])
    return {k: v / sumOfWords for k, v in wordCount.items()}


def generateOne(size, wordProbs, filePath):
    rangesList = []
    for i in range(len(wordProbs) + 1):
        rangesList.append(0.0)
    for i in range(1, len(rangesList) - 1):
        rangesList[i] += wordProbs[i - 1][1]
        rangesList[i + 1] += rangesList[i]
    rangesList[-1] = 1
    content = ''
    for i in range(size):
        rand = random.random()
        randIndex = 0
        for j in range(len(rangesList) - 1):
            if rangesList[j] <= rand <= rangesList[j + 1]:
                randIndex = j
                break
        content += wordProbs[randIndex][0] + ' '
    open(filePath, 'w+').write(content)


if __name__ == '__main__':

    print('zad1\n')
    wordCount = getWordsCount('../data/norm_wiki_sample.txt')
    print('Sum of words: {}'.format(len(wordCount)))
    print('Polish man know {:.2f}% words of wikipedia'.format(len(wordCount) / 30000))
    print()
    wordProbabilities = getWordsProbabilities('../data/norm_wiki_sample.txt')
    wordCountList = [[k, v] for k, v in wordCount.items()]
    wordProbabilitiesList = [[k, v] for k, v in wordProbabilities.items()]
    for i in range(10):
        print('{:<20} {:>8} {:>8.2f}%'.format(wordCountList[i][0], wordCountList[i][1],
                                              wordProbabilitiesList[i][1] * 100))
    print()
    sum30000 = sum([v for k, v in wordProbabilitiesList[:30000]])
    print('30 000 most popular words are {:.2f}% of all words in Wikipedia textfile'.format(sum30000 * 100))
    sum6000 = sum([v for k, v in wordProbabilitiesList[:6000]])
    print('6 000 most popular words are {:.2f}% of all words in Wikipedia textfile'.format(sum6000 * 100))
    print()

    print('zad2\n')
    generateOne(100, wordProbabilitiesList, 'outputOne.txt')
    print()

    print('zad3\n')
    markov1 = computeMarkovSource('../data/norm_wiki_sample.txt', 1)
    generateUsingMarkov(400, markov1, 'outputMarkov1.txt')

    markov2 = computeMarkovSource('../data/norm_wiki_sample.txt', 2)
    generateUsingMarkov(400, markov2, 'outputMarkov2.txt')

