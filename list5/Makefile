# Compiler and flags
CXX = clang++
CXXFLAGS = -std=c++11 -Wall

# Linker flags
LDFLAGS = -lsqlite3

# Output binary name
TARGET = library_manager

# Source files
SRCS = db.cpp

# Object files
OBJS = $(SRCS:.cpp=.o)

# Default target to build
all: $(TARGET)

# Rule to build the target
$(TARGET): $(OBJS)
	$(CXX) $(OBJS) -o $(TARGET) $(LDFLAGS)

# Rule to compile .cpp files to .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up build artifacts
clean:
	rm -f $(OBJS) $(TARGET)

# Run the program after compilation
run: $(TARGET)
	./$(TARGET)
