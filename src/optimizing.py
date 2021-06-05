import re
import src.classes as c

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
    equation = re.sub(r"\)\(", ")*(", equation) # if we have stuff like "(x+3)(x-3)" we make it to "(x+3)*(x-3)"
    equation = re.sub(r"(?<=[^\+\-\*\^\)])\(", "*(", equation) # we convert "3x(x+3)" to "3x*(x+3)"
    equation = re.sub(r"\)(?=[^\+\-\*\^\()])", ")*", equation) # we convert "(x+3)3x" to "(x+3)*3x"

    # this is a fairly complex regex, but it's idea is simple
    # 1. match any operator (-, +, *, ^, (, )), where it matches the '-' only when it's used for subtraction
    # 2. match a positive element - for example '5xy', 'y', '2w'
    # 3. match every negative element (when it's surrounded in brackets)
    
    #result = [i[0] for i in re.findall(r"(([\+\*\^\(\)]|(?<!\()\-)|(?<!\(\-)(\d*(\.\d+)?)[a-z]*|(?<=\()(\-\d*(\.\d+)?[a-z]*))", equation)]
    result = [i[0] for i in re.findall(r"(([\+\*\(\)]|(?<!\()\-|(?<=\))\^)|(?<!\(\-)(\d*(\.\d+)?)([a-z](\^\d+)?)?|(?<=\()(\-\d*(\.\d+)?[a-z]*))", equation)]
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
        negative = False
        if i[0] == '-':
            i = i[1:]
            negative = True

        temp = []
        operator_stack = []
        for j in i:
            if j not in ['+', '-', '*', '^', '(', ')']:
                temp.append(j)

            elif j in operators.keys():
                #print(f"operator_stack = {operator_stack}")
                while operator_stack != [] and operator_stack[0] != '(' and (operators[operator_stack[0]][0] > operators[j][0] or (operators[operator_stack[0]][0] == operators[j][0] and operators[j][1] == 'L')):
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

        if negative:
            temp[0] = '-' + temp[0]

        result.append(temp)
    return result

def solve_RPN(expression): # here we optimize the equation based on the RPN 
    # test equation - "5x^(2*2^(20-4*5))+5x-10.5+11x"
    # another test equation - "5x*12-10.5*5+5x^(2*2^(20-4*5))+11x^(2(15^(-5x+5x)))"
    expression = RPN(expression)
    for i in range(len(expression)):
        if len(expression[i]) < 3:
            continue
        stack = []
        for j in range(len(expression[i])):
            if expression[i][j] in ['+', '-', '*', '^']:
                #print(f"stack = {stack}, operation = {expression[i][j]}")
                if len(stack) == 1:
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
        temp = ''
        
        for j in i:
            if j == '-':
                temp = '-' + temp
            else:
                temp += str(j)

        if temp[0] == '-':
            result += temp
        else:
            result += '+' + temp

    return result

def reconstruct_equation(unit_list):
    result = ''
    for i in unit_list:
        if i.value() < 1:
            result += str(i)
        else:
            result += '+' + str(i)

    if result[0] == '+':
        result = result[1:]

    return result

def sort_equation(equation):
    equation = [c.Unit(i) for i in split_equation(equation)]
    return sorted(equation, reverse = True, key = lambda unit: unit.power())            

def optimize(equation):
    equation = reconstruct_operations(solve_RPN(equation))
    equation = [c.Unit(i) for i in split_equation(equation)]
    equation = optimize_equation(equation)
    return reconstruct_equation(sort_equation(reconstruct_equation(equation)))
