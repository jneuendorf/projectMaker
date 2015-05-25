################################################################################
# COMPILE VARS
CC = g++
COMPILE = $(CC) -c

################################################################################
# PROJECT VARS
NAME = pmake
SOURCES = main.o io.o

################################################################################
# build app
make: $(SOURCES)
	$(CC) -Wall $(SOURCES) -o $(NAME)

remake: clean make

main.o: main.hpp libs.hpp
	$(COMPILE) main.cpp

io.o: io.hpp libs.hpp
	$(COMPILE) io.cpp

# my_string.o: my_string.h
# 	$(COMPILE) my_string.c

################################################################################
# RUN
run: make
	./pmake

remakerun: clean make run

################################################################################
# CLEAN
clean:
	rm -f $(SOURCES)
	rm -f $(NAME)
	rm -f a.out
