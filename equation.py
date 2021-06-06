import re
from typing import Type
import src.optimizing as opt
import src.solving as s

class Equation():
    def __init__(self, expression):
        self.expression = re.sub(r"[^\da-z\+\-\*\^\/\(\)\=\.]", '', expression)
        self.expression = re.sub(r"\*\*", '^', expression)
        
        try:
            self.left_side = re.findall(r'.+(?==)', self.expression)[0]
            self.right_side = re.findall(r'(?<==).+', self.expression)[0]
            self.transfer_to_left_side()
            self.left_side = opt.optimize(self.left_side)
            self.solution = self.solve()

        except IndexError:
            print("Error: you must assign a value to the expression for it to be an equation.")
        except ZeroDivisionError:
            print("Error: division by zero.")
        except:
            print("Error: couldn't handle the equation properly, please try a different one.")

    # transfers the whole equation on the left side so it's equal to 0
    def transfer_to_left_side(self):
        if self.right_side == '0':
            return self.left_side

        right_side = opt.split_parenthesis(self.right_side)

        def reverse(string):
            if string[0] == '-':
                return '+' + string[1:]
            else:
                return '-' + string

        for i in right_side:
            self.left_side += reverse(i)
        self.right_side = '0'

    def __repr__(self):
        try:
            return f"solutions for {self.left_side}: " + str(self.solution)
        except AttributeError:
            return ''

    def solve(self):
        equation = self.left_side
        if re.search(r"^\-?\d*(\.\d+)?([a-z])\^2([\+\-]\d*(\.\d+)?\2)?([\+\-]\d*(\.\d+)?)?$", equation):
            return s.quadratic_equation(equation)
        elif re.search(r"^\-?\d*(\.\d+)?([a-z])\^(\d)([\+\-]\d*(\.\d+)?\2\^(\d))?([\+\-]\d*(\.\d+)?)$", equation):
            temp = re.findall(r"^\d*(\.\d+)?([a-z])\^(\d)([\+\-]\d*(\.\d+)?\2\^(\d))?([\+\-]\d*(\.\d+)?)$", equation)[0]
            pow1, pow2 = temp[2], temp[5]
            if pow1 == '4' and (pow2 == '' or pow2 == '2'):
                return s.biquadratic_equation(equation)
        else:
            return None