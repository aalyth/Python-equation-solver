import re
import math

def quadric_equation(equation):
    result = {}
# I use the formula ax^2 + bx + c = 0 as an example
# we put the equation in the right order
    def get_equation_part(string):
        if string[0] == '-' or string[0] == '+':
            return string
        else:
            return '+' + string

    new_equation = ''
    equation_parts = ['', '', '']
    current_part = equation[0]
    for i in range(1, len(equation)):
        if equation[i] != '+' and equation[i] != '-':
            current_part += equation[i]
        if equation[i] == '+' or equation[i] == '-' or i == len(equation) - 1:
            if re.search(r'\^', current_part):
                current_part = re.sub(r'\+', '', current_part)
                equation_parts[0] = current_part
            elif re.search(r'[a-z]', current_part):
                equation_parts[1] = get_equation_part(current_part)
            else:
                equation_parts[2] = get_equation_part(current_part)
            current_part = equation[i]

    for i in equation_parts:
        new_equation += i

    del equation_parts
    del current_part

# now we get the values of a, b and c respectively
    equation = new_equation
    values = [1, 1, 1]
    current_number = ''
    counter = 0
    for i in range(len(equation)):
        if equation[i].isdigit():
            current_number += equation[i]
            if i == len(equation) - 1 and current_number != '':
                values[counter] = int(current_number)
        elif equation[i] == '+':
            current_number = ''
        elif equation[i] == '-':
            current_number = '-'
        elif equation[i].isalpha() or i == len(equation) - 1:
            if current_number != '': values[counter] = int(current_number)
            current_number = ''
            counter += 1

# now we apply the formula (-b ± sqrt(D)) / 2*a
# where D = b^2 - 4 * a * c

    print(equation)
    D = values[1]**2 - 4 * values[0] * values[2]
    if D < 0:
        return {'error' : 'using imaginary numbers'}
    x1 = (-values[1] - math.sqrt(D)) / (2 * values[0])
    x2 = (-values[1] + math.sqrt(D)) / (2 * values[0])
    result.update({'x1' : x1})
    result.update({'x2' : x2})


    return result

print(quadric_equation('5b^2-108b+468'))
