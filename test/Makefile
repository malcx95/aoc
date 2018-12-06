PROGRAM=test
CXXFLAGS=-std=c++17 -Wall -Wextra -Wpedantic
SOURCES=../util/input.hpp ../util/input.cpp ../util/stringextra.hpp
OPTIMIZATION=-O2

.PHONY: build
.PHONY: clean
.PHONY: distrib      

build: $(PROGRAM)

clean:
	rm $(PROGRAM)

distrib:
	tar -czf $(PROGRAM).tar.gz $(PROGRAM).cpp Makefile

$(PROGRAM): $(PROGRAM).cpp
	g++ $(PROGRAM).cpp $(SOURCES) $(CXXFLAGS) $(OPTIMIZATION) -o $(PROGRAM)
