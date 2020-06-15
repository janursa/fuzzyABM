# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.17.1)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(abm_base-populate NONE)

include(ExternalProject)
ExternalProject_Add(abm_base-populate
                     "UPDATE_DISCONNECTED" "False" "GIT_REPOSITORY" "https://github.com/janursa/ABM_extension.git" "GIT_TAG" "master"
                    SOURCE_DIR          "/Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-src"
                    BINARY_DIR          "/Users/matin/Downloads/testProjs/ABM_extension/build/_deps/abm_base-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
)
