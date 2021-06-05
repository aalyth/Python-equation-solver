import re
import math
import numpy as np

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
    
    print(f"values = {values}")

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
            solution1 = str((-b - sqrt_d) / (2 * a))
            solution2 = str((-b + sqrt_d) / (2 * a))


        if sqrt_d != int(sqrt_d): # if it's not a perfect square root we add the square root representation
            if imaginary:
                solution1 = f"({-b} - √{-d}) / {2 * a} = " + solution1
                solution2 = f"({-b} + √{-d}) / {2 * a} = " + solution2
            else:
                solution1 = f"({-b} - √{d}) / {2 * a} = " + str((-b - sqrt_d) / (2 * a))
                solution2 = f"({-b} + √{d}) / {2 * a} = " + str((-b + sqrt_d) / (2 * a))
            
        return [solution1, solution2]
    
    try:
        temp = math.sqrt(D)
        solutions = get_roots(values[0], values[1], D, temp)

    except ValueError:
        D = D * -1
        temp = math.sqrt(D)
        solutions = get_roots(values[0], values[1], D, temp, True)

    finally:
        result.update({f'{variable}1' : solutions[0]})
        result.update({f'{variable}2' : solutions[1]})

    return result

def biquadratic_equation(equation):
    variable = get_variable(equation)
    equation = re.sub(r"[a-z]\^2", f"{variable}", equation)
    equation = re.sub(r"[a-z]\^4", f"{variable}^2", equation)
    solutions = quadratic_equation(equation)

    print(solutions)

    result = {}
    for i in range(len(solutions)):
        if re.search(r"=", solutions[f"{variable}{i+1}"]):
            solutions[f"{variable}{i+1}"] = re.findall(r"(?<== ).+", solutions[f"{variable}{i+1}"])[0]
        
        try:
            if not re.search(r"i", solutions[f"{variable}{i+1}"]):
                temp = math.sqrt(float(solutions[f"{variable}{i+1}"]))
                temp1, temp2 = str(-temp), str(temp)
            else:
                temp1 = "-√(" + solutions[f"{variable}{i+1}"] + ")"
                temp2 = "√(" + solutions[f"{variable}{i+1}"] + ")"

        except ValueError:
            temp = math.sqrt(-float(solutions[f"{variable}{i+1}"]))
            temp1, temp2 = str(-temp)+"i", str(temp)+"i"

        finally:
            result.update({f"{variable}{i+1}.1" : temp1})
            result.update({f"{variable}{i+1}.2" : temp2})
    
    return result

def sqrt_complex(expression):
    """
    the formula is:
    we have the complex number w = x + yi
    and it's square root sqrt(w) = z = a + bi
    we have l = √(x^2 + y^2)
    x = √((l + x) / 2)
    y = sgn(x) * √((l - x) / 2)
    """

    real = float(re.findall(r"(\-?\d*(\.\d+)?(?!i))", expression)[0][0])
    if real == '':
        real = 0
    imaginary = re.findall(r"(\-?\d*(\.\d+)?)i", expression)[0][0]
    if imaginary == '':
        imaginary = 1
    elif imaginary == '-':
        imaginary = -1
    else:
        imaginary = float(imaginary)
    
    print(f"real = {real}, imaginary = {imaginary}")
    temp = math.sqrt(real**2 + imaginary**2)
    a = math.sqrt((temp + real) / 2)
    b = np.sign(real) * math.sqrt((temp - real) / 2)
    print(f"temp = {temp}, a = {a}, b = {b}")
    if b < 0:
        return f"{a} - {-b}i"
    else:
        return f"{a} + {b}i"

#print(quadratic_equation('5b^2-15b-468'))
#print(biquadratic_equation('5x^4+7x^2-18'))
