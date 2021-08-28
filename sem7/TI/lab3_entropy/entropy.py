import math


def getSignsProbabilities(filePath, length):
    counterList = {}
    inFile = open(filePath, 'r')
    for line in inFile.readlines():
        for i in range(len(line) - length + 1):
            ngram = line[i:i + length]
            if ngram not in counterList:
                counterList[line[i:i + length]] = 1
            else:
                counterList[line[i:i + length]] += 1
    sumOfSigns = sum([v for k, v in counterList.items()])
    return {k: v / sumOfSigns for k, v in counterList.items()}


def getWordsProbabilities(filePath, length):
    wordCount = getWordsCount(filePath, length)
    sumOfWords = sum([v for k, v in wordCount.items()])
    return {k: v / sumOfWords for k, v in wordCount.items()}


def getWordsCount(filePath, length):
    sequenceCount = {}
    file = open(filePath, 'r')
    for line in file.readlines():
        words = line.split()
        for i in range(len(words) - length + 1):
            sequence = ''
            for word in words[i:i + length]:
                sequence += word + ' '
            sequence = sequence[0:len(sequence) - 1]
            if sequence not in sequenceCount:
                sequenceCount[sequence] = 1
            else:
                sequenceCount[sequence] += 1
    return {k: v for k, v in sorted(sequenceCount.items(), key=lambda elem: elem[1], reverse=True)}


def getEntropy(probs):
    entropy = 0
    for ngram, prob in probs.items():
        if prob == 0:
            continue
        entropy += prob * math.log(prob, 2)
    return -entropy


def getConditionalEntropy(probs, markovSource):
    conditionalEntropy = 0
    for ngram, ngramProb in probs.items():
        if ngram in markovSource:
            for ngramWithTail, tailProb in markovSource[ngram].items():
                conditionalEntropy += (ngramProb * tailProb) * math.log(tailProb, 2)
    return -conditionalEntropy


def computeMarkovSourceForSigns(inFilePath, markovLevel):
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
        markov[k] = {k1: v1 for k1, v1 in
                     sorted({k2: v2 / sum for k2, v2 in v.items()}.items(), key=lambda item: item[1], reverse=True)}
    return markov


def computeMarkovSourceForWords(inFilePath, markovLevel):
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


def computeResultsForFile(filename):
    results = []
    for level in range(1, 4):
        signsProbs = getSignsProbabilities(filename, level)
        if level == 1:
            results.append(getEntropy(signsProbs))
        markovSourceForSigns = computeMarkovSourceForSigns(filename, level)
        results.append(getConditionalEntropy(signsProbs, markovSourceForSigns))
    for level in range(1, 4):
        wordsProbs = getWordsProbabilities(filename, level)
        if level == 1:
            results.append(getEntropy(wordsProbs))
        markovSourceForWords = computeMarkovSourceForWords(filename, level)
        results.append(getConditionalEntropy(wordsProbs, markovSourceForWords))
    return results


def printAllResults(allResults):
    row = 1
    for name, results in allResults.items():
        if row == 1:
            print(
                "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("{:<20} | {:>20} | {:>20} | {:>20} | {:>20} | {:>20} | {:>20} | {:>20} | {:>20} |".format(
                name, results[0], results[1], results[2], results[3], results[4], results[5], results[6], results[7]
            ))
            print(
                "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            row += 1
        else:
            print(
                "{:<20} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} |".format(
                    name, results[0], results[1], results[2], results[3], results[4], results[5], results[6], results[7]
                ))
            print(
                "{:<20} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} | {:>20.2f} |".format(
                    '',
                    (results[0] / results[0]) * 100.0,
                    (results[1] / results[0]) * 100.0,
                    (results[2] / results[0]) * 100.0,
                    (results[3] / results[0]) * 100.0,
                    (results[4] / results[4]) * 100.0,
                    (results[5] / results[4]) * 100.0,
                    (results[6] / results[4]) * 100.0,
                    (results[7] / results[4]) * 100.0
                ))
            print(
                "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


if __name__ == '__main__':
    print('zad 2.1')
    print()
    print('Sx - signs entropy level x')
    print('Wx - words entropy level x')
    print('SCx - signs conditional entropy level x')
    print('WCx - words conditional entropy level x')
    print()

    allResults = {'filename': ['S1', 'SC1', 'SC2', 'SC3', 'W1', 'WC1', 'WC2', 'WC3'],
                  'norm_wiki_en.txt': computeResultsForFile('../data/norm_wiki_en.txt'),
                  'norm_wiki_eo.txt': computeResultsForFile('../data/norm_wiki_eo.txt'),
                  'norm_wiki_et.txt': computeResultsForFile('../data/norm_wiki_et.txt'),
                  'norm_wiki_ht.txt': computeResultsForFile('../data/norm_wiki_ht.txt'),
                  'norm_wiki_la.txt': computeResultsForFile('../data/norm_wiki_la.txt'),
                  'norm_wiki_nv.txt': computeResultsForFile('../data/norm_wiki_nv.txt'),
                  'norm_wiki_so.txt': computeResultsForFile('../data/norm_wiki_so.txt'),
                  'sample1.txt': computeResultsForFile('../data/sample0.txt'),
                  'sample2.txt': computeResultsForFile('../data/sample1.txt'),
                  'sample3.txt': computeResultsForFile('../data/sample2.txt'),
                  'sample4.txt': computeResultsForFile('../data/sample3.txt'),
                  'sample5.txt': computeResultsForFile('../data/sample4.txt')
                  }
    printAllResults(allResults)

    # markovSourceForSigns2 = computeMarkovSourceForSigns('../data/norm_wiki_en.txt', 2)
    # markovSourceForSigns3 = computeMarkovSourceForSigns('../data/norm_wiki_en.txt', 3)
    # markovSourceForSigns4 = computeMarkovSourceForSigns('../data/norm_wiki_en.txt', 4)
    #
    # markovSourceForWords2 = computeMarkovSourceForWords('../data/norm_wiki_en.txt', 2)
    # markovSourceForWords3 = computeMarkovSourceForWords('../data/norm_wiki_en.txt', 3)
    # markovSourceForWords4 = computeMarkovSourceForWords('../data/norm_wiki_en.txt', 4)

    print()
