import re
import unittest as ut
import equation as eq
import src.classes as c
from src.solving import get_variable
from src.optimizing import split_equation, reconstruct_equation

def check_solutions(equation, solutions):
    variable = get_variable(equation)
    result = [] # this is the result when we compute the given solution - so it should be full of zeroes
    
    for i in solutions.values():
        if re.search(r"i", i[0]) == None:
            temp = re.sub(f"{variable}", f"({round(float(i[0]), 7)})", eq.Equation(equation + "=0").left_side)
            temp = re.sub(r"(?<=\d)\(", "*(", re.sub(r"\^", "**", temp))
            result.append(round(eval(temp), 0))

        else:
            temp = re.sub(f"{variable}", f"({i[0]})", eq.Equation(equation + "=0").left_side)
            temp = eq.Equation(temp + "=0").left_side
            temp = [c.Unit(i) for i in split_equation(temp)]

            # here we just remove all the imaginary parts
            for i in range(len(temp)):
                if temp[i].get_suffix_str() != '':
                    if re.search(r"i", str(temp[i].suffix[0])) and int(str(temp[i].suffix[0])[2]) % 4 == 0:
                        temp[i] = c.Unit(str(temp[i].value()))
                    elif re.search(r"i", str(temp[i].suffix[0])) and int(str(temp[i].suffix[0])[2]) % 2 == 0:
                        temp[i] = c.Unit(str(temp[i].value() * -1))
            temp = reconstruct_equation(temp)
            
            result.append(round(eval(temp), 0))
    
    return result

class Tests(ut.TestCase):
    def test_quadratic_equations(self):
        self.assertEqual(check_solutions("5b^2-15b-468", eq.Equation("5b^2-15b-468=0").solution), [0, 0])
        self.assertEqual(check_solutions("5(x^(2*2^(20-4*5)))+5x-10.5+11x", eq.Equation("5(x^(2*2^(20-4*5)))+5x-10.5+11x=0").solution), [0, 0])
        self.assertEqual(check_solutions("5x*12-10.5*5+5x^(2*2^(20-4*5))+11x^(2(15^(-5x+5x)))", eq.Equation("5x*12-10.5*5+5x^(2*2^(20-4*5))+11x^(2(15^(-5x+5x)))=0").solution), [0, 0])
        self.assertEqual(check_solutions("4(x^(4-(1+((((1)))))))+5x", eq.Equation("4(x^(4-(1+((((1)))))))+5x=0").solution), [0, 0])
        self.assertEqual(check_solutions("38x^2+0.5x^2+9.3x+0.31", eq.Equation("38x^2+0.5x^2+9.3x+0.31=0").solution), [0, 0])
        
    def test_biquadratic_equations(self): 
        self.assertEqual(check_solutions("5x^4+7x^2-18", eq.Equation("5x^4+7x^2-18=0").solution), [0, 0, 0, 0])
        self.assertEqual(check_solutions("w^4-13w^2+36", eq.Equation("w^4-13w^2+36=0").solution), [0, 0, 0, 0])
        self.assertEqual(check_solutions("((69x-(1432*3)/2)^2)^2+2822549328x^3+2735343758592x", eq.Equation("((69x-(1432*3)/2)^2)^2=-2822549328x^3-2735343758592x").solution), [0, 0, 0, 0])

if __name__ == '__main__':
    ut.main()
