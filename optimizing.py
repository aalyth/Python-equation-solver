import re
#import equation as eq
import classes as c

def split_equation(equation_string): 
    return re.findall(r'\-?[^\+\-]+', equation_string)

def split_parenthesis(equation_string): # it is similar to split_equation but it groups the elements by parenthesis
    equation_string = split_equation(equation_string)
    result = [equation_string[0]]
    
    def get_parenthesis_diff(string):
        return len(re.findall(r"\(", string)) - len(re.findall(r"\)", string))

    inside_parenthesis = get_parenthesis_diff(result[0]) # the number of parenthesis we're in currently
    for i in equation_string[1:]:
        if inside_parenthesis != 0:
            if i[0] != '-':
                result[-1] += '+'
            result[-1] += i
        else:
            result.append(i)
        inside_parenthesis += get_parenthesis_diff(i)

    return result

def calculate(operand1, operand2, operator):
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '^':
        return operand1 ** operand2

def split_operations(equation):
    # this is a fairly complex regex but it's idea is simple
    # 1. match any operator (-, +, *, ^, (, )), where it matches the '-' only when it's used for subtraction
    # 2. match a positive element - for example '5xy', 'y', '2w'
    # 3. match every negative element (when it's surrounded in brackets)
    result = [i[0] for i in re.findall(r"(([\+\*\^\(\)]|(?<!\()\-)|(?<!\(\-)(\d*(\.\d+)?)[a-z]*|(?<=\()(\-\d*(\.\d+)?[a-z]*))", equation)]
    return [i for i in result if i != '']

def RPN(expression): # RPN stands for Reverse Polish Notation
    # this is the Shunting-yard algorithm
    expression = split_parenthesis(expression)
    result = []
    operators = {
        '+': [1, 'L'],
        '-': [1, 'L'],
        '*': [2, 'L'],
        '^': [3, 'R']
    }

    for i in expression:
        i = split_operations(i)
        temp = []
        operator_stack = []
        for j in i:
            if j not in ['+', '-', '*', '^', '(', ')']:
                temp.append(j)
            elif j in operators.keys():
                while operator_stack != [] and (operators[operator_stack[-1]][0] > operators[j][0] or (operators[operator_stack[-1]][0] > operators[j][0] and operators[j][1] == 'L')) and operators[operator_stack[-1]][1] != 'R':
                    temp.append(operator_stack.pop(0))
                operator_stack.insert(0, j)
            elif j == '(':
                operator_stack.insert(0, j)
            elif j == ')':
                for i in range(len(operator_stack)):
                    if operator_stack[0] == '(':
                        operator_stack.pop(0)
                        break
                    else:
                        temp.append(operator_stack.pop(0))
        while operator_stack != []:
            temp.append(operator_stack.pop(0))
        result.append(temp)
        
    return result

def solve_RPN(expression): # here we optimize the equation based on the RPN 
    # test equation - "5x^(2*2^(20-4*5))+5x-10.5+11x"
    expression = RPN(expression)
    print(expression)
    for i in range(len(expression)):
        if len(expression[i]) < 3:
            break
        stack = []
        for j in range(len(expression[i])):
            if expression[i][j] in ['+', '-', '*', '^']:
                if j == len(expression[i]) - 1 and expression[i][j] == '^':
                    stack.insert(1, '^')
                    break
                stack[-2] = calculate(stack[-2], stack[-1], expression[i][j])
                stack.pop(len(stack) - 1)
            else:
                stack.append(c.Expression(expression[i][j]))
        expression[i] = stack
    return expression

def optimize_equation(unit_list):
    made_changes = True
    while made_changes:
        made_changes = False
        for i in range(len(unit_list)):
            for j in range(i + 1, len(unit_list)):
                if unit_list[i] + unit_list[j] != None:
                    unit_list[i] = unit_list[i] + unit_list[j]
                    unit_list.pop(j)
                    if unit_list[i].prefix == '0':
                        unit_list.pop(i)
                    made_changes = True
                    break

    if made_changes:
        optimize_equation(unit_list)
    else:
        return unit_list

def reconstruct_operations(rpn_list):
    result = ''.join(str(i) for i in rpn_list[0])

    for i in rpn_list[1:]:
        for j in range(len(i)):
                if j == 0 and len(i) > 1:
                    if i[1] == '-':
                        result += '-' + i[j]
                        break
                    else:
                        result += '+' + i[j]
                else:
                    result += '+' + i[j]
    
    return result

def reconstruct_equation(unit_list):
    result = ''
    if unit_list[0].value() == -1:
        result += '-' + unit_list[0].get_suffix()
    elif unit_list[0].value() == 1:
        result += unit_list[0].get_suffix()
    else:
        result += unit_list[0].prefix + unit_list[0].get_suffix()

    for i in unit_list[1:]:
        if i.value() == 1:
            result += '+' + i.get_suffix()
        elif i.value() == -1:
            result += '-' + i.get_suffix()
        elif i.value() > 1:
            result += '+' + i.prefix + i.get_suffix()
        else:
            result += i.prefix + i.get_suffix()

    return result

def optimize(equation_left_side):
    units = [c.Unit(i) for i in split_equation(equation_left_side)]
    units = optimize_equation(units)
    return reconstruct_equation(units)

#print(optimize(eq.Equation('x^2 - 2x^2 + 4x + 5x + 5 + 11 = 0')))
