# 🧮 Scientific Calculator

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fully-featured scientific calculator built with Python and PyQt5. It supports standard arithmetic operations, advanced scientific functions, memory operations, and a sleek modern interface.

## Table of Contents

- [Features](#-features)
- [Screenshot](#-screenshot)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Standard Arithmetic:** `+`, `-`, `*`, `/`
- **Scientific Functions:** `sin`, `cos`, `tan`, `log`, `ln`, `√`, `x²`, `xʸ`, `1/x`, `!` (factorial)
- **Mathematical Constants:** `π` and `e`
- **Memory Functions:** `MC`, `MR`, `M+`, `M-`, `MS`
- **Entry Management:** `C` (clear all), `CE` (clear entry), `⌫` (backspace), `±` (change sign)
- **Parentheses Support:** For grouping expressions.
- **Real-time Feedback:** An expression display that shows the ongoing calculation.
- **Keyboard Input:** Supports keyboard input for most operations.
- **Error Handling:** Gracefully handles errors like division by zero and invalid input.
- **Modern UI:** A dark, modern GUI with hover and press effects for a better user experience.

## 📸 Screenshot

<img width="227" height="369" alt="Calculator Screenshot" src="https://github.com/user-attachments/assets/4d30e4f6-98a9-4d8e-9acd-7318203292fc" />

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/11Siya05/PyQt-Scientific-Calculator
    cd PyQt-Scientific-Calculator
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install PyQt5
    ```

## 🎮 Usage

Run the calculator from the command line:

```bash
python main.py
```

Use the on-screen buttons or your keyboard to perform calculations.

**Examples:**
- **sin(30):** Press `3`, `0`, then `sin`.
- **5³:** Press `5`, `xʸ`, `3`, then `=`.
- **Store a number:** Enter a number and press `MS`.
- **Recall a number:** Press `MR`.

## 💡 How It Works

- **Display Management:** The calculator uses two `QLineEdit` widgets to show the current input and the full expression.
- **Operations:** It handles basic arithmetic, repeated `=` calculations, and provides clear error messages.
- **Scientific Functions:** The `math` module from Python's standard library is used for scientific calculations, with input validation to prevent errors.
- **Memory:** A single numeric value can be stored, recalled, and modified using the memory functions.
- **UI:** The user interface is built with PyQt5, using a `QGridLayout` for the buttons and a `QVBoxLayout` for the main window layout. Styling is done with QSS (Qt Style Sheets).


