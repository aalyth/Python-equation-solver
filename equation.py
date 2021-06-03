from classes import Expression
import re
import optimizing as opt
import solving as s

class Equation():
    def __init__(self, expression):
        self.expression = re.sub(r"[^\da-z\+\-\*\^\(\)\=]", '', expression)
        self.left_side = re.findall(r'.+(?==)', self.expression)[0]
        self.right_side = re.findall(r'(?<==).+', self.expression)[0]
        self.transfer_to_left_side()
        self.left_side = opt.optimize(self.left_side)
        #print(self.left_side)
        self.solution = self.solve()
        

    # transfers the whole equation on the left side so it's equal to 0
    def transfer_to_left_side(self):
        right_side = opt.split_parenthesis(self.right_side)

        def reverse(string):
            if string[0] == '-':
                return '+' + string[1:]
            else:
                return '-' + string

        for i in right_side:
            self.left_side += reverse(i)
        self.right_side = '0'
        #print(self.left_side)

    def __repr__(self):
        return f"solutions for {self.left_side}: " + str(self.solution)

    def solve(self):
        equation = self.left_side
        if re.search(r"\d*(\.\d+)?([a-z])\^2[\+\-](\d*(\.\d+)?\2)?[\+\-](\d*(\.\d+)?)?", equation):
            return s.quadratic_equation(equation)

#s.quadratic_equation(Equation('x^2 + 4x  + 5 = 2x^2 - 5x - 11').left_side)
