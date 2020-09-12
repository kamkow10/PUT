SOURCES=$(wildcard *.cpp)
HEADERS=$(SOURCES:.cpp=.h)
FLAGS=-DDEBUG -g

all: main

main: $(SOURCES) $(HEADERS)
	g++ output/sortOutput.cpp -o output/sortOutput.out
	mpiCC $(SOURCES) $(FLAGS) -o main.out

clear: clean_binary clean_output_text

clean_binary:
	rm main.out
	rm output/sortOutput.out

clean_output_text:
	rm output/unsortedOutput.txt

run: main
	mpirun -np 8 ./main.out

run_unixlab: main
	mpirun -H lab-os-10,lab-os-11,lab-os-12,lab-os-13 -np 4 main.out
