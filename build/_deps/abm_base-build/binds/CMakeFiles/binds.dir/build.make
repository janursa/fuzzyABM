# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.17

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CMake.app/Contents/bin/cmake

# The command to remove a file.
RM = /Applications/CMake.app/Contents/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/matin/Downloads/testProjs/ABM_extension

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/matin/Downloads/testProjs/ABM_extension/build

# Include any dependencies generated for this target.
include _deps/abm_base-build/binds/CMakeFiles/binds.dir/depend.make

# Include the progress variables for this target.
include _deps/abm_base-build/binds/CMakeFiles/binds.dir/progress.make

# Include the compile flags for this target's objects.
include _deps/abm_base-build/binds/CMakeFiles/binds.dir/flags.make

_deps/abm_base-build/binds/CMakeFiles/binds.dir/binds.cpp.o: _deps/abm_base-build/binds/CMakeFiles/binds.dir/flags.make
_deps/abm_base-build/binds/CMakeFiles/binds.dir/binds.cpp.o: _deps/abm_base-src/binds/binds.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/matin/Downloads/testProjs/ABM_extension/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object _deps/abm_base-build/binds/CMakeFiles/binds.dir/binds.cpp.o"
	cd /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-build/binds && /Library/Developer/CommandLineTools/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/binds.dir/binds.cpp.o -c /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-src/binds/binds.cpp

_deps/abm_base-build/binds/CMakeFiles/binds.dir/binds.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/binds.dir/binds.cpp.i"
	cd /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-build/binds && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-src/binds/binds.cpp > CMakeFiles/binds.dir/binds.cpp.i

_deps/abm_base-build/binds/CMakeFiles/binds.dir/binds.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/binds.dir/binds.cpp.s"
	cd /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-build/binds && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-src/binds/binds.cpp -o CMakeFiles/binds.dir/binds.cpp.s

# Object files for target binds
binds_OBJECTS = \
"CMakeFiles/binds.dir/binds.cpp.o"

# External object files for target binds
binds_EXTERNAL_OBJECTS =

_deps/abm_base-build/binds/binds.cpython-37m-darwin.so: _deps/abm_base-build/binds/CMakeFiles/binds.dir/binds.cpp.o
_deps/abm_base-build/binds/binds.cpython-37m-darwin.so: _deps/abm_base-build/binds/CMakeFiles/binds.dir/build.make
_deps/abm_base-build/binds/binds.cpython-37m-darwin.so: _deps/fmtlib-build/libfmt.a
_deps/abm_base-build/binds/binds.cpython-37m-darwin.so: _deps/abm_base-build/binds/CMakeFiles/binds.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/matin/Downloads/testProjs/ABM_extension/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module binds.cpython-37m-darwin.so"
	cd /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-build/binds && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/binds.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
_deps/abm_base-build/binds/CMakeFiles/binds.dir/build: _deps/abm_base-build/binds/binds.cpython-37m-darwin.so

.PHONY : _deps/abm_base-build/binds/CMakeFiles/binds.dir/build

_deps/abm_base-build/binds/CMakeFiles/binds.dir/clean:
	cd /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-build/binds && $(CMAKE_COMMAND) -P CMakeFiles/binds.dir/cmake_clean.cmake
.PHONY : _deps/abm_base-build/binds/CMakeFiles/binds.dir/clean

_deps/abm_base-build/binds/CMakeFiles/binds.dir/depend:
	cd /Users/matin/Downloads/testProjs/ABM_extension/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/matin/Downloads/testProjs/ABM_extension /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-src/binds /Users/matin/Downloads/testProjs/ABM_extension/build /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-build/binds /Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-build/binds/CMakeFiles/binds.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : _deps/abm_base-build/binds/CMakeFiles/binds.dir/depend
