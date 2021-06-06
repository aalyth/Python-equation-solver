import re
import math

def get_variable(equation):
    for i in equation:
        if i.isalpha():
            return i

def quadratic_equation(equation):
    # I use the formula ax^2 + bx + c = 0 as an example
    result = {}
    
    variable = get_variable(equation)

    # here we get the values of a, b and c
    values = []
    values.append(re.findall(r"(\-?\d+(\.\d+)?)?[a-z]\^2", equation)) #a
    equation = re.sub(r"(\-?\d+(\.\d+)?)?[a-z]\^2", '', equation)
    values.append(re.findall(r"(\-?\d*(\.\d+)?)[a-z](?!\^)", equation)) #b
    equation = re.sub(r"(\-?\d*(\.\d+)?)[a-z](?!\^)", '', equation)
    values.append(re.findall(r"((?<!\^)\-?\d+(\.\d+)?(?![a-z\.]))", equation)) #c

    for i in range(len(values)):
        if values[i] != []:
            values[i] = values[i][0][0]
            if values[i] not in ['-', '']:
                values[i] = float(values[i])
            elif values[i] == '':
                values[i] = 1
            elif values[i] == '-':
                values[i] = -1
        else:
            values[i] = 0

    # now we apply the formula (-b ± sqrt(D)) / (2*a)
    # where D = b^2 - 4 * a * c
    D = values[1]**2 - 4 * values[0] * values[2]
    
    def get_roots(a, b, d, sqrt_d, imaginary=False):
        if imaginary:
            temp = -b / (2 * a)
            if temp != 0:
                solution1 = f"{temp} - {sqrt_d / (2 * a)}i"
                solution2 = f"{temp} + {sqrt_d / (2 * a)}i"
            else:
                solution1 = f"-{sqrt_d / (2 * a)}i"
                solution2 = f"{sqrt_d / (2 * a)}i"
        else:
            solution1 = str(((-b) - sqrt_d) / (2 * a))
            solution2 = str(((-b) + sqrt_d) / (2 * a))

        if sqrt_d != int(sqrt_d): # if it's not a perfect square root we add the square root representation
            return [
                (solution1, f"({-b} - √{d}) / {2 * a}"),
                (solution2, f"({-b} + √{d}) / {2 * a}")
            ]
            
        return [(solution1, ''), (solution2, '')]

    try:
        temp = math.sqrt(D)
        solutions = get_roots(values[0], values[1], D, temp)

    except ValueError:
        D = D * -1
        temp = math.sqrt(D)
        solutions = get_roots(values[0], values[1], D, temp, True)

    finally:
        result.update({f"{variable}1" : solutions[0]})
        result.update({f"{variable}2" : solutions[1]})

    return result

def biquadratic_equation(equation):
    variable = get_variable(equation)
    equation = re.sub(r"[a-z]\^2", f"{variable}", equation)
    equation = re.sub(r"[a-z]\^4", f"{variable}^2", equation)
    solutions = quadratic_equation(equation)

    result = {}

    def invert_complex(num): # multiplies the complex number by -1
        result = '' if num[0] == '-' else '-'
        num = num if num[0] != '-' else num[1:]
        for i in num:
            if i == '+':
                result += '-'
            elif i == '-':
                result += '+'
            else:
                result += i
        return result

    for i in range(len(solutions)):
        try:
            if re.search(r"i", solutions[f"{variable}{i+1}"][0]) == None:
                temp = math.sqrt(float(solutions[f"{variable}{i+1}"][0]))
                temp1, temp2 = str(-temp), str(temp)
            else:
                temp1 = invert_complex(sqrt_complex(solutions[f"{variable}{i+1}"][0]))
                temp2 = sqrt_complex(solutions[f"{variable}{i+1}"][0])

        except ValueError:
            temp = math.sqrt(-float(solutions[f"{variable}{i+1}"][0]))
            temp1, temp2 = str(-temp)+"i", str(temp)+"i"

        finally:
            result.update({f"{variable}{i+1}.1" : (temp1,)})
            result.update({f"{variable}{i+1}.2" : (temp2,)})
    
    return result


def sqrt_complex(expression):
    """
    the formula is:
    we have the complex number w = x + yi
    and it's square root sqrt(w) = z = a + bi
    we have l = √(x^2 + y^2)
    x = √((l + x) / 2)
    y = sgn(y) * √((l - x) / 2)
    """

    def sgn(num): # signum function
        return -1 if num < 0 else 1

    expression = re.sub(r" ", '', expression)

    real = re.findall(r"(\-?\d*(\.\d+)?(?!i))", re.sub(r"(\-?\d*(\.\d+)?)", '', expression))[0][0]
    real = 0 if real == '' else float(real)

    imaginary = re.findall(r"(\-?\d*(\.\d+)?)i", expression)[0][0]
    if imaginary == '':
        imaginary = 1
    elif imaginary == '-':
        imaginary = -1
    else:
        imaginary = float(imaginary)
    
    temp = math.sqrt(real**2 + imaginary**2)
    a = math.sqrt((temp + real) / 2)
    b = sgn(imaginary) * math.sqrt((temp - real) / 2)
    if b < 0:
        return f"{a} - {-b}i"
    else:
        return f"{a} + {b}i"
