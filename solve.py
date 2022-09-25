##
# 2WF90 Algebra for Security -- Software Assignment 1
# Integer and Modular Arithmetic
# solve.py
#
#
# Group number:
# 28
#
# Author names and student IDs:
# Atilla Rzazade (1552848)
# Daua Karajeanes (1619675)
# Valentina Marinova (1665154)
# Gergana Valkova (1676385)
##

# Import built-in json library for handling input/output
import json
# from locale import RADIXCHAR
from radix import *

radix_dict = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    '10': 'A',
    '11': 'B',
    '12': 'C',
    '13': 'D',
    '14': 'E',
    '15': 'F'
}

radix = 10
varX = 0
varY = 0
conversionX = False
conversionY = False
answer = 0
lengthNumX = 0
lengthNumY = 0

# removes the sign from the beggining and puts True for negative values and False for positive values
def sign():
    global varX
    global varY
    global conversionX
    global conversionY
    sign = '-'

    if sign in varX:
        varX = varX[1:]
        conversionX = True
    else:
        conversionX = False

    if sign in varY:
        varY = varY[1:]
        conversionY = True
    else:
        conversionY = False


def get_sign(a):
    return True if a[0] == '-' else False


def determine_m(x, y):
    m = 0
    signedX = get_sign(x)
    signedY = get_sign(y)

    x = x[1:] if signedX else x
    y = y[1:] if signedY else y

    if len(x) == len(y):
        m = len(x)
    elif len(y) > len(x) and signedY:
        # -1 because 0th index is sign
        m = len(y) - 1
    elif len(x) > len(y) and signedX:
        # same
        m = len(x) - 1
    elif len(x) != len(y) and not signedX and not signedY:
        m = max(len(x), len(y))

    return m, signedX, signedY, x, y


def get_operands(x, y, i, j, signedX, signedY):
    # index - 2 since the answer contains extra 2 indices
    index_x = i - 2
    index_y = j - 2
    x_index = int(radix_dict[x[index_x]])
    y_index = int(radix_dict[y[index_y]])
    # convert index to corresponding digit (i.e. '2' -> 2, 'A' -> 10) and sign (i.e. '-A' -> -10)
    dictX = -1*x_index if signedX else x_index
    dictY = -1*y_index if signedY else y_index

    return dictX, dictY


def multiplication_karatsuba(x, y, length, radix):
    x = x[1:] if get_sign(x) else x    
    y = y[1:] if get_sign(y) else y
    result = karatsuba_recursive(x, y, length, radix)
    return result
    

def karatsuba_recursive(x, y, length, radix):
    print(x, y, length)

    xH = 0
    xL = 0
    yH = 0
    yL = 0
    answer = 0
    number2 = 0
    number0 = 0
    number1 = 0

    if (length == 1):
        int_x = int(radix_dict[str(x)])
        int_y = int(radix_dict[str(y)])
        int_xy = int_x * int_y
        right_digit = str(radix_dict[str(int_xy % radix)])
        left_digit = str(radix_dict[str(int_xy // radix)])
        return left_digit + right_digit

    if (length % 2 != 0):
        length += 1
        x = '0' + x
        y = '0' + y
    xH = x[:length//2] if length > 1 else x
    xL = x[length//2:] if length > 1 else x  # x = xH*pow(radix, length/2) + xL
    yH = y[:length//2] if length > 1 else y
    yL = y[length//2:] if length > 1 else y  # y = yH*pow(radix, length/2) + yL
    print('high = ', xH, xL, yH, yL)
    number2 = karatsuba_recursive(xH, yH, length//2, radix)
    number0 = karatsuba_recursive(xL, yL, length//2, radix)
    xh_xl = integer_addition(xH, xL, radix)
    yh_yl = integer_addition(yH, yL, radix)
    new_length = max(len(xh_xl), len(yh_yl))

    
    number1 = integer_subtraction(integer_subtraction(karatsuba_recursive(xh_xl, yh_yl, new_length, radix), number0, radix), number2, radix)
    print('numbers', number2, number1, number0)
    add1 = integer_multiplication_naive(number2, ("1" + length * "0"), radix)
    print(number1, 'and', ("1" + (length // 2) * "0"))
    add2 = integer_multiplication_naive(number1, ("1" + (length // 2) * "0"), radix)
    answer = integer_addition(add1, add2, radix)
    answer = integer_addition(answer, number0, radix)

    return answer


def division(x, y, radix):
    i = 0
    while (x[:1] != '-'):
        x = integer_subtraction(x, y, radix)
        i += 1
    return get_radix_rep(i, radix)


def extended_euclidean_algorithm(x, y, radix):
    a1 = '1'
    a2 = '0'
    b1 = '0'
    b2 = '1'
    while (y[:1] != '-' and y[:1] != '0'):
        q = division(x, y, radix)
        r = integer_subtraction(
            x, integer_multiplication_naive(q, y, radix), radix)
        x = y
        y = r
        a3 = integer_subtraction(
            a1, integer_multiplication_naive(q, a2, radix), radix)
        b3 = integer_subtraction(
            b1, integer_multiplication_naive(q, b2, radix), radix)
        a1, b1 = a2, b2
        a2, b2 = a3, b3

    d = x

    return d, a1, b1


def decimal(x):
    if x >= '0' and x <= '9':
        return ord(x) - ord('0')
    else:
        return ord(x) - ord('A') + 10


def compare(x, y):
    if len(x) > len(y):
        x_greater = True
    elif len(x) == len(y):
        x_greater = x > y
    else:
        x_greater = False
    return x_greater

def modularReduction(x,m,base):
    base = int(base)
    if base != '10':
        x_int = anyBaseToDecimal(x,base)
        m_int= anyBaseToDecimal(m,base)
    
    if(x_int > 0):
        if (x_int < m_int):
            answer = x_int
        elif(x_int == m_int):
            answer = 0
        elif(x_int > m_int):
            answer = x_int - m_int * (x_int // m_int)
    if(x_int < 0):
        while(x_int < m_int):
            x_int = x_int +m_int
        answer = x_int

    answer = str(decimalToAnyBase(answer,base))

    return answer

def modular_addition(x, y, mod, radix):
    x = modularReduction(x, mod, radix)
    y = modularReduction(y, mod, radix)

    z = integer_addition(x, y, radix)
    if compare(z, mod):
        z = integer_subtraction(z, mod, radix)
    return z


def modular_subtraction(x, y, mod, radix):
    x = modularReduction(x, mod, radix)
    y = modularReduction(y, mod, radix)

    z = integer_subtraction(x, y, radix)
    if compare(z, '0'):
        return z
    else:
        z = integer_addition(z, mod, radix)
    return z



def modular_inversion (x, mod, radix):
    x1, x2 = '1', '0'
    while(len(mod) > 1 or mod[0] != '0'):
        q = division(x, mod, radix)
        q_length = len(str(q))
        r = integer_subtraction (x, integer_multiplication_naive(q, mod, radix), radix)
        x, mod = mod, r
        x3 = integer_subtraction (x1, integer_multiplication_naive(q, x2, radix), radix)
        x1, x2 = x2, x3
    
    if x == 1:
        return x1
    else:
        print('inverse does not exist')


def solve_exercise(exercise_location: str, answer_location: str):
    """
    solves an exercise specified in the file located at exercise_location and
    writes the answer to a file at answer_location. Note: the file at
    answer_location might not exist yet and, hence, might still need to be created.
    """

    # Open file at exercise_location for reading.
    with open(exercise_location, "r") as exercise_file:
        # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data
        exercise = json.load(exercise_file)

    ### Parse and solve ###
    global radix
    global varX
    global varY
    radix = exercise["radix"]
    varX = exercise["x"]

    answer = ''

    # Check type of exercise
    if exercise["type"] == "integer_arithmetic":
        varY = exercise["y"]
        # Check what operation within the integer arithmetic operations we need to solve
        if exercise["operation"] == "addition":
            # Solve integer arithmetic addition exercise
            answer = integer_addition(varX,varY,radix)
            pass
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            answer = integer_subtraction(varX,varY,radix)
            pass
        elif exercise["operation"] == "multiplication_primary":
            # Solve integer arithmetic subtraction exercise
            answer = integer_multiplication_naive(varX,varY,radix)
            pass
        elif exercise["operation"] == "multiplication_karatsuba":
            # Solve integer arithmetic subtraction exercise
            answer = multiplication_karatsuba(varX,varY,radix)
            pass
        elif exercise["operation"] == "extended_euclidean_algorithm":
            # Solve integer arithmetic subtraction exercise
            answer = extended_euclidean_algorithm(varX,varY,radix)
            pass
    else:  # exercise["type"] == "modular_arithmetic"
        # Check what operation within the modular arithmetic operations we need to solve
        modulus = exercise["modulus"]
        varY = exercise["y"] if not(exercise["operation"] == 'reduction' or exercise["operation"] == 'inversion') else ''
        if modulus != '0':
            if exercise["operation"] == "reduction":
                # Solve modular arithmetic reduction exercise
                answer = modularReduction(varX,modulus,radix)
                pass
            elif exercise["operation"] == "addition":
                # Solve modular arithmetic addition exercise
                answer = modular_addition(varX,varY,modulus,radix)
                pass
            elif exercise["operation"] == "subtraction":
                # Solve modular arithmetic substraction exercise
                answer = modular_subtraction(varX,varY,modulus,radix)
                pass
            elif exercise["operation"] == "multiplication":
                # Solve modular arithmetic multiplication exercise
                answer = modular_multiplication(varX,varY,modulus,radix)
                pass
            elif exercise["operation"] == "inversion":
                # Solve modular arithmetic inversion exercise
                answer = modular_inversion(varX,modulus,radix)
                pass
        else:
            answer = 'can not use modulus (0 or negative)'

    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        data = {'answer': clean_str(answer)}
        json.dump(data, answer_file, indent=4)

solve_exercise('json/exercise3.json', 'json/answers/answer3.json')
