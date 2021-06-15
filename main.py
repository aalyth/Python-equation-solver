import equation as eq
import sys
import re

if __name__ == '__main__':
    equation = ''.join(sys.argv[1:])
    equation = re.sub(r'\*\*', '^', equation)
    print(eq.Equation(equation))
