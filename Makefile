SRC=./src
BIN=./bin
UNIT=./test
GAME=battleship.cpp
TEST=test_battleship.cpp

CXX=gcc
FLAGS = -g -Wall -Wextra

all : battleship test_battleship

clean :
	rm *.o

battleship:
	$(CXX) $(FLAGS) $(SRC)/$(GAME)

test_battleship:
	$(CXX) $(FLAGS) $(UNIT)/$(TEST)
