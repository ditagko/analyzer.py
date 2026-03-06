# Keystroke Dynamics Analyzer 

A Python-based desktop application that analyzes raw keystroke data from multiple text files to extract behavioral typing metrics. 

This tool was developed to process keystroke logs, map keycodes to their actual characters, and calculate specific typing habits, such as the frequency of key presses and the pause durations after specific punctuation marks.

Features
User-Friendly GUI**: A simple desktop interface built with `tkinter` for easy directory selection and execution.
Data Parsing & Cleaning**: Reads raw `.txt` files, filters out invalid rows, and handles keycode mapping (e.g., mapping "13" to "Enter").
Behavioral Metrics extraction**: 
    Calculates the relative frequency of each key pressed.
    Measures pause ratios (pauses > 5.0 seconds) after specific keys like Spacebar, Enter, and punctuation marks.
Automated Export


Language: Python 


How to Use
1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/yourusername/Keystroke-Dynamics-Analyzer.git](https://github.com/yourusername/Keystroke-Dynamics-Analyzer.git)
