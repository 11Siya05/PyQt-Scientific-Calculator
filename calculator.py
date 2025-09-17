import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator")
        self.setGeometry(100, 100, 450, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 15px;
                font-size: 24px;
                font-family: 'Courier New', monospace;
                min-height: 60px;
            }
            QPushButton {
                background-color: #404040;
                color: white;
                border: 1px solid #606060;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #606060;
            }
            .operator {
                background-color: #ff9500;
            }
            .operator:hover {
                background-color: #ffad33;
            }
            .scientific {
                background-color: #007acc;
            }
            .scientific:hover {
                background-color: #0099ff;
            }
            .special {
                background-color: #666666;
            }
            .special:hover {
                background-color: #777777;
            }
        """)
        
        # Initialize variables
        self.current_input = ""
        self.result = 0
        self.operation = None
        self.waiting_for_operand = False
        self.last_operation = None
        self.last_operand = None
        self.memory = 0
        self.expression = ""  # Track the full expression
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setText("0")
        self.display.setMaxLength(50)  # Allow longer expressions
        layout.addWidget(self.display)
        
        # Expression display (shows the full calculation)
        self.expression_display = QLineEdit()
        self.expression_display.setAlignment(Qt.AlignRight)
        self.expression_display.setReadOnly(True)
        self.expression_display.setText("")
        self.expression_display.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                color: #888888;
                border: none;
                padding: 5px 15px;
                font-size: 16px;
                font-family: 'Courier New', monospace;
                min-height: 25px;
            }
        """)
        layout.addWidget(self.expression_display)
        
        # Memory indicator
        self.memory_label = QLabel("M: 0")
        self.memory_label.setStyleSheet("color: #888888; padding: 5px;")
        layout.addWidget(self.memory_label)
        
        # Button layout
        button_layout = QGridLayout()
        layout.addLayout(button_layout)
        
        # Define buttons
        buttons = [
            # Row 0 - Memory and special functions
            ('MC', 0, 0, 'special'), ('MR', 0, 1, 'special'), ('M+', 0, 2, 'special'), ('M-', 0, 3, 'special'), ('MS', 0, 4, 'special'),
            
            # Row 1 - Scientific functions
            ('sin', 1, 0, 'scientific'), ('cos', 1, 1, 'scientific'), ('tan', 1, 2, 'scientific'), ('log', 1, 3, 'scientific'), ('ln', 1, 4, 'scientific'),
            
            # Row 2 - More scientific functions
            ('√', 2, 0, 'scientific'), ('x²', 2, 1, 'scientific'), ('xʸ', 2, 2, 'scientific'), ('1/x', 2, 3, 'scientific'), ('π', 2, 4, 'scientific'),
            
            # Row 3 - Parentheses and operations
            ('(', 3, 0, 'special'), (')', 3, 1, 'special'), ('C', 3, 2, 'special'), ('CE', 3, 3, 'special'), ('⌫', 3, 4, 'special'),
            
            # Row 4 - Numbers and operations
            ('7', 4, 0, ''), ('8', 4, 1, ''), ('9', 4, 2, ''), ('/', 4, 3, 'operator'), ('!', 4, 4, 'scientific'),
            
            # Row 5
            ('4', 5, 0, ''), ('5', 5, 1, ''), ('6', 5, 2, ''), ('*', 5, 3, 'operator'), ('e', 5, 4, 'scientific'),
            
            # Row 6
            ('1', 6, 0, ''), ('2', 6, 1, ''), ('3', 6, 2, ''), ('-', 6, 3, 'operator'), ('±', 6, 4, 'special'),
            
            # Row 7
            ('0', 7, 0, '', 1, 2), ('.', 7, 2, ''), ('+', 7, 3, 'operator'), ('=', 7, 4, 'operator')
        ]
        
        # Create and place buttons
        for button_info in buttons:
            text = button_info[0]
            row = button_info[1]
            col = button_info[2]
            style_class = button_info[3] if len(button_info) > 3 else ''
            row_span = button_info[4] if len(button_info) > 4 else 1
            col_span = button_info[5] if len(button_info) > 5 else 1
            
            button = QPushButton(text)
            button.clicked.connect(lambda checked, t=text: self.button_clicked(t))
            
            # Apply styles
            if style_class:
                button.setProperty('class', style_class)
                if style_class == 'operator':
                    button.setStyleSheet(button.styleSheet() + "QPushButton { background-color: #ff9500; } QPushButton:hover { background-color: #ffad33; }")
                elif style_class == 'scientific':
                    button.setStyleSheet(button.styleSheet() + "QPushButton { background-color: #007acc; } QPushButton:hover { background-color: #0099ff; }")
                elif style_class == 'special':
                    button.setStyleSheet(button.styleSheet() + "QPushButton { background-color: #666666; } QPushButton:hover { background-color: #777777; }")
            
            button_layout.addWidget(button, row, col, row_span, col_span)
    
    def button_clicked(self, text):
        if text.isdigit() or text == '.':
            self.input_digit(text)
        elif text in ['+', '-', '*', '/', 'xʸ']:
            self.input_operator(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear_all()
        elif text == 'CE':
            self.clear_entry()
        elif text == '⌫':
            self.backspace()
        elif text == '±':
            self.change_sign()
        elif text in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', '1/x', '!']:
            self.scientific_function(text)
        elif text in ['π', 'e']:
            self.input_constant(text)
        elif text in ['MC', 'MR', 'M+', 'M-', 'MS']:
            self.memory_function(text)
        elif text in ['(', ')']:
            self.input_parenthesis(text)
    
    def input_digit(self, digit):
        if self.waiting_for_operand:
            self.display.setText(digit)
            self.waiting_for_operand = False
        else:
            if self.display.text() == '0' and digit != '.':
                self.display.setText(digit)
            else:
                self.display.setText(self.display.text() + digit)
        
        # Update expression display during input
        if self.operation and not self.waiting_for_operand:
            op_symbol = '^' if self.operation == 'xʸ' else self.operation
            self.expression_display.setText(f"{self.result} {op_symbol} {self.display.text()}")
    
    def input_operator(self, op):
        current_value = float(self.display.text())
        
        if self.operation and not self.waiting_for_operand:
            # Complete the previous operation first
            self.calculate()
            current_value = float(self.display.text())
        
        self.result = current_value
        self.operation = op
        self.waiting_for_operand = True
        
        # Update expression display
        op_symbol = '^' if op == 'xʸ' else op
        self.expression_display.setText(f"{current_value} {op_symbol} ")
    
    def calculate(self):
        if self.operation and not self.waiting_for_operand:
            try:
                current_value = float(self.display.text())
                
                # Update expression display to show full calculation
                op_symbol = '^' if self.operation == 'xʸ' else self.operation
                self.expression_display.setText(f"{self.result} {op_symbol} {current_value} =")
                
                if self.operation == '+':
                    result = self.result + current_value
                elif self.operation == '-':
                    result = self.result - current_value
                elif self.operation == '*':
                    result = self.result * current_value
                elif self.operation == '/':
                    if current_value == 0:
                        self.display.setText("Error: Division by zero")
                        self.expression_display.setText("Error: Division by zero")
                        return
                    result = self.result / current_value
                elif self.operation == 'xʸ':
                    result = self.result ** current_value
                
                # Store for repeat operations
                self.last_operation = self.operation
                self.last_operand = current_value
                
                # Format result
                if result == int(result) and abs(result) < 1e15:
                    self.display.setText(str(int(result)))
                else:
                    # Use scientific notation for very large/small numbers
                    if abs(result) >= 1e12 or (abs(result) < 1e-4 and result != 0):
                        self.display.setText(f"{result:.6e}")
                    else:
                        self.display.setText(f"{result:.10g}")
                
                self.operation = None
                self.waiting_for_operand = True
                
            except Exception as e:
                self.display.setText("Error")
                self.expression_display.setText("Error")
        elif self.last_operation and self.last_operand is not None:
            # Repeat last operation (when pressing = multiple times)
            try:
                current_value = float(self.display.text())
                op_symbol = '^' if self.last_operation == 'xʸ' else self.last_operation
                self.expression_display.setText(f"{current_value} {op_symbol} {self.last_operand} =")
                
                if self.last_operation == '+':
                    result = current_value + self.last_operand
                elif self.last_operation == '-':
                    result = current_value - self.last_operand
                elif self.last_operation == '*':
                    result = current_value * self.last_operand
                elif self.last_operation == '/':
                    if self.last_operand == 0:
                        self.display.setText("Error: Division by zero")
                        self.expression_display.setText("Error: Division by zero")
                        return
                    result = current_value / self.last_operand
                elif self.last_operation == 'xʸ':
                    result = current_value ** self.last_operand
                
                # Format result
                if result == int(result) and abs(result) < 1e15:
                    self.display.setText(str(int(result)))
                else:
                    if abs(result) >= 1e12 or (abs(result) < 1e-4 and result != 0):
                        self.display.setText(f"{result:.6e}")
                    else:
                        self.display.setText(f"{result:.10g}")
                        
            except Exception as e:
                self.display.setText("Error")
                self.expression_display.setText("Error")
    
    def scientific_function(self, func):
        try:
            value = float(self.display.text())
            
            # Show the function being applied in expression display
            self.expression_display.setText(f"{func}({value}) =")
            
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            elif func == 'log':
                if value <= 0:
                    self.display.setText("Error: Invalid input")
                    self.expression_display.setText("Error")
                    return
                result = math.log10(value)
            elif func == 'ln':
                if value <= 0:
                    self.display.setText("Error: Invalid input")
                    self.expression_display.setText("Error")
                    return
                result = math.log(value)
            elif func == '√':
                if value < 0:
                    self.display.setText("Error: Invalid input")
                    self.expression_display.setText("Error")
                    return
                result = math.sqrt(value)
                self.expression_display.setText(f"√({value}) =")
            elif func == 'x²':
                result = value ** 2
                self.expression_display.setText(f"({value})² =")
            elif func == '1/x':
                if value == 0:
                    self.display.setText("Error: Division by zero")
                    self.expression_display.setText("Error")
                    return
                result = 1 / value
                self.expression_display.setText(f"1/({value}) =")
            elif func == '!':
                if value < 0 or value != int(value) or value > 170:
                    self.display.setText("Error: Invalid input")
                    self.expression_display.setText("Error")
                    return
                result = math.factorial(int(value))
                self.expression_display.setText(f"{int(value)}! =")
            
            # Format result
            if result == int(result) and abs(result) < 1e15:
                self.display.setText(str(int(result)))
            else:
                # Use scientific notation for very large/small numbers
                if abs(result) >= 1e12 or (abs(result) < 1e-4 and result != 0):
                    self.display.setText(f"{result:.6e}")
                else:
                    self.display.setText(f"{result:.10g}")
            
            self.waiting_for_operand = True
            
        except Exception as e:
            self.display.setText("Error")
            self.expression_display.setText("Error")
    
    def input_constant(self, constant):
        if constant == 'π':
            value = math.pi
            self.expression_display.setText("π")
        elif constant == 'e':
            value = math.e
            self.expression_display.setText("e")
        
        self.display.setText(f"{value:.10g}")
        self.waiting_for_operand = True
    
    def memory_function(self, func):
        try:
            current_value = float(self.display.text())
            
            if func == 'MC':
                self.memory = 0
            elif func == 'MR':
                self.display.setText(str(self.memory))
                self.waiting_for_operand = True
            elif func == 'M+':
                self.memory += current_value
            elif func == 'M-':
                self.memory -= current_value
            elif func == 'MS':
                self.memory = current_value
            
            # Update memory display
            self.memory_label.setText(f"M: {self.memory:.6g}")
            
        except:
            pass
    
    def input_parenthesis(self, paren):
        # Basic parenthesis support - adds to display for visual reference
        # Full expression evaluation would require a more complex parser
        current_text = self.display.text()
        if current_text == '0':
            self.display.setText(paren)
        else:
            self.display.setText(current_text + paren)
    
    def clear_all(self):
        self.display.setText("0")
        self.expression_display.setText("")
        self.result = 0
        self.operation = None
        self.waiting_for_operand = False
        self.last_operation = None
        self.last_operand = None
        self.expression = ""
    
    def clear_entry(self):
        self.display.setText("0")
        self.waiting_for_operand = False
        # Don't clear expression display on CE, only clear current entry
    
    def backspace(self):
        text = self.display.text()
        if len(text) > 1:
            new_text = text[:-1]
            self.display.setText(new_text)
            # Update expression display if in the middle of an operation
            if self.operation and not self.waiting_for_operand:
                op_symbol = '^' if self.operation == 'xʸ' else self.operation
                self.expression_display.setText(f"{self.result} {op_symbol} {new_text}")
        else:
            self.display.setText("0")
    
    def change_sign(self):
        try:
            value = float(self.display.text())
            value = -value
            if value == int(value):
                self.display.setText(str(int(value)))
            else:
                self.display.setText(str(value))
        except:
            pass

    def keyPressEvent(self, event):
        key = event.key()
        
        # Number keys
        if Qt.Key_0 <= key <= Qt.Key_9:
            self.button_clicked(chr(key))
        # Operator keys
        elif key == Qt.Key_Plus:
            self.button_clicked('+')
        elif key == Qt.Key_Minus:
            self.button_clicked('-')
        elif key == Qt.Key_Asterisk:
            self.button_clicked('*')
        elif key == Qt.Key_Slash:
            self.button_clicked('/')
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.button_clicked('=')
        elif key == Qt.Key_Period:
            self.button_clicked('.')
        elif key == Qt.Key_Backspace:
            self.button_clicked('⌫')
        elif key == Qt.Key_Delete:
            self.button_clicked('CE')
        elif key == Qt.Key_Escape:
            self.button_clicked('C')


def main():
    app = QApplication(sys.argv)
    calculator = ScientificCalculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()