import re
#import equation as eq

# stands for "string function"
def str_func(string1, string2, function):
    return str(function(int(string1), int(string2)))

# doing math stuff with objects of class unit
def unit_math(unit1, unit2, function):
    if unit1.suffix == unit2.suffix and type(unit1) == Unit and type(unit2) == Unit:
        return Unit(str(function(unit1.value(), unit2.value())) + unit1.suffix)
    else: return None

class Unit():
    def __init__(self, string):
        if re.findall(r'([a-z](\^\d+)?)', string) != []:
            self.suffix = re.findall(r'([a-z](\^\d+)?)', string)[0][0]
        else:
            self.suffix = ''
        self.prefix = re.sub(r'([a-z](\^\d+)?)', '', string)

    def __add__(self, other):
        return unit_math(self, other, lambda x,y: x + y)

    def __sub__(self, other):
        return unit_math(self, other, lambda x,y: x - y)

    def value(self):
        if self.prefix == '':
            return 1
        elif self.prefix == '-':
            return -1
        elif self.prefix[0] == '-' and self.prefix[1:].isdigit():
            return -int(self.prefix[1:])
        elif self.prefix.isdigit():
            return int(self.prefix)

# for easier testing
    def __repr__(self):
        return str(self.prefix) + str(self.suffix)

def split_equation(equation_string):
    return re.findall(r'\-?[^\+\-]+', equation_string)

def optimize_unit_list(unit_list):
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
        optimize_unit_list(unit_list)
    else:
        return unit_list

def reconstruct_equation(unit_list):
    result = ''
    if unit_list[0].value() == -1:
        result += '-' + unit_list[0].suffix
    elif unit_list[0].value() == 1:
        result += unit_list[0].suffix
    else:
        result += unit_list[0].prefix + unit_list[0].suffix

    for i in unit_list[1:]:
        if i.value() == 1:
            result += '+' + i.suffix
        elif i.value() == -1:
            result += '-' + i.suffix
        elif i.value() > 1:
            result += '+' + i.prefix + i.suffix
        else:
            result += i.prefix + i.suffix

    return result

def optimize(equation_left_side):
    units = [Unit(i) for i in split_equation(equation_left_side)]
    #print(units)
    units = optimize_unit_list(units)
    #print(units)
    return reconstruct_equation(units)
    #print(equation.left_side)

u1 = Unit('10x^2')
u2 = Unit('5x')
u3 = Unit('5x^2')
u4 = Unit('7x^2')
#u5 = Unit((u1 + u3) + u1.suffix)
#print(u1 + u2)
#print(optimize(eq.Equation('x^2 - 2x^2 + 4x + 5x + 5 + 11 = 0')))
