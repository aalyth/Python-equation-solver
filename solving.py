import re
import math

def get_variable(equation):
    for i in equation:
        if i.isalpha():
            return i

def quadratic_equation(equation):
    # I use the formula ax^2 + bx + c = 0 as an example
    result = {}

    # here we get the values of a, b and c
    values = []
    values.append(re.findall(r"(\d+(\.\d+)?)?[a-z]\^2", equation)) #a
    values.append(re.findall(r"(\d+(\.\d+)?)?[a-z](?!\^)", equation)) #b
    values.append(re.findall(r"((?<!\^)\d+(?![a-z]))", equation)) #c

    for i in range(len(values)):
        if values[i] != []:
            values[i] = values[i][0][0]
            if values[i] != '':
                values[i] = float(values[i])
            else:
                values[i] = 1
        else:
            values[i] = 0

    # now we apply the formula (-b ± sqrt(D)) / (2*a)
    # where D = b^2 - 4 * a * c
    D = values[1]**2 - 4 * values[0] * values[2]
    variable = get_variable(equation)

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
    equation = re.sub(r"[a-z]\^4", f"{variable}^2", re.sub(r"[a-z]\^2", f"{variable}", equation))
    solutions = quadratic_equation(equation)

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
    we will have √(real + imaginary) = a + bi
    then: real + imaginary = (a + bi)^2 = a^2 + 2bi - b^2
    so we'll solve the system in wich:
    |a^2 + b^2 = real
    |2abi = imaginary
    and then we solve
    """

    real = re.findall(r"(\-?\d*(\.\d+)?(?!i))", expression)[0][0]
    imaginary = re.findall(r"(\-?\d*(\.\d)?i)", expression)[0][0]
    if imaginary[:-1] == '-':
        imaginary = '-1i'
    elif imaginary[:-1] == '':
        imaginary = '1i'

    print(f"imaginary[:-1] = {imaginary[:-1]}")
    sq_a = str(eval(f"{imaginary[:-1]}**2"))
    # here we automatically multiply the equation by 2b^2 and we get:
    # (imaginary (without i))^2 + 2b^4 = 2b^2 * real
    print(f"we pass: {sq_a}+2b^4-{2*float(real)}b^2")
    solutions_for_a = biquadratic_equation(f"{sq_a}+2b^4-{2*real}b^2")
    solutions_for_a = [i[i.index("=")+2:] if re.search(r"=", i) else i for i in solutions_for_a.values() ]
    print(f"solutions for {sq_a}+2b^4-{2*real}b^2 = {solutions_for_a}")


#print(quadratic_equation('5b^2-15b-468'))
#print(biquadratic_equation('5x^4+7x^2-18'))
