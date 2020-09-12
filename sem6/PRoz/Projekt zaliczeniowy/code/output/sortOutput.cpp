#include <iostream>
#include <list>
#include <fstream>
#include <string>

using namespace std;

typedef struct {
    int lamport;
    int procId;
    string lineText;
} OutputLine;

string getString(char x) {
    string s(1, x);
    return s;
}

bool compLamport(OutputLine x, OutputLine y) {
    return x.lamport < y.lamport;
}

int main() {
    list<OutputLine> outputList;
    list<OutputLine>::iterator it;
    ifstream file("unsortedOutput.txt");
    string line;
    while(getline(file, line)) {
        if (line.find('<') == string::npos)
            continue;
        int pos = line.find("[", 7);
        string procId = getString(line[pos + 1]) + getString(line[pos + 2]);
        string lamport = getString(line[pos + 5]) + getString(line[pos + 6]) + getString(line[pos + 7]) + getString(line[pos + 8]);
        OutputLine outputLine = { stoi(lamport), stoi(procId), line };
        outputList.push_back(outputLine);
    }
    outputList.sort(compLamport);
    for (it = outputList.begin(); it != outputList.end(); it++) {
        cout << it->lineText << endl;
    }

    return 0;
}

