import re
import optimizing as opt

class Equation():
    def __init__(self, expression):
        self.expression = expression.replace(' ', '')
        self.power = self.get_equasion_power()
        self.left_side = re.findall(r'.+(?==)', self.expression)[0]
        self.right_side = re.findall(r'(?<==).+', self.expression)[0]
        self.transfer_to_left_side()
        self.left_side = opt.optimize(self.left_side)
        print(self.left_side)

    def get_equasion_power(self):
        highest_power = 1
        for i in re.finditer('\^', self.expression):
            current_number = 0

            for j in range(i.start()+1, len(self.expression)):
                if not self.expression[j].isdigit():
                    break
                current_number = current_number * 10 + int(self.expression[j])

            if current_number > highest_power:
                highest_power = current_number

        return highest_power

    # transfers the whole equation on the left side so it's equal to 0
    def transfer_to_left_side(self):
        right_side = opt.split_equation(self.right_side)

        def reverse(string):
            if string[0] == '-':
                return '+' + string[1:]
            else:
                return '-' + string

        for i in right_side:
            self.left_side += reverse(i)
        self.right_side = '0'
        #print(self.left_side)

Equation('x^2 + 4x  + 5 = 2x^2 - 5x - 11')
