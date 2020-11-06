"""
Description: This is main file calling the basler viewer / inspector program interface.
Author: "Parth Desai"
"""
# Importing dependencies
# Own modules
from baslerAppWindow import ApplicationWindow

applicationName = 'Basler Camera Viewer'

if __name__ == "__main__":
    ApplicationWindow(applicationName)