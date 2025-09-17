🧮 Scientific Calculator

A fully-featured scientific calculator built with Python and PyQt5. It supports standard arithmetic operations, advanced scientific functions, memory operations, and a sleek modern interface. Perfect for daily calculations or learning scientific math functions.

✨ Features

Standard arithmetic: +, -, *, /

Scientific functions: sin, cos, tan, log, ln, √, x², xʸ, 1/x, factorial (!)

Mathematical constants: π and e

Memory functions: MC, MR, M+, M-, MS

Entry management: C (clear all), CE (clear entry), ⌫ (backspace), ± (change sign)

Parentheses support for grouping

Expression display for real-time feedback

Keyboard input support

Error handling (division by zero, invalid inputs)

Dark modern GUI with hover and press effects

<img width="227" height="369" alt="image" src="https://github.com/user-attachments/assets/4d30e4f6-98a9-4d8e-9acd-7318203292fc" />



A sleek, modern calculator interface built with PyQt5.

🚀 Installation

Clone the repository:

git clone https://github.com/11Siya05/PyQt-Scientific-Calculator
cd PyQt-Scientific-Calculator


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate


Install dependencies:

pip install PyQt5

🎮 Usage

Run the calculator:

python main.py


Use the buttons or your keyboard to perform calculations.

Examples:

sin(30) → press 3, 0, then sin, then =

5^3 → press 5, xʸ, 3, =

Store in memory → press MS

Recall memory → press MR

💡 How It Works

Display management: Shows current input and full expression

Operations: Handles basic arithmetic, repeated = calculations, and error handling

Scientific functions: Uses Python math module with input validation

Memory: Stores a single numeric value with M+, M-, MS, MR, MC

UI: Built with PyQt5, uses QGridLayout for buttons and QLineEdit for display
