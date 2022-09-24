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
from locale import RADIXCHAR
from multiprocessing.managers import ValueProxy

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

def solve_exercise(exercise_location : str, answer_location : str):
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
    varY = exercise["y"]

    # Check type of exercise
    if exercise["type"] == "integer_arithmetic":
        # Check what operation within the integer arithmetic operations we need to solve
        if exercise["operation"] == "addition":
            integer_addition()
            # Solve integer arithmetic addition exercise
            pass
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            pass
        elif exercise["operation"] == "multiplication":
            # Solve integer arithmetic subtraction exercise
            pass
        elif exercise["operation"] == "multiplication_primary":
            # Solve integer arithmetic subtraction exercise
            pass
        elif exercise["operation"] == "multiplication_karatsuba":
            # Solve integer arithmetic subtraction exercise
            pass
        elif exercise["operation"] == "extended_euclidean_algorithm":
            # Solve integer arithmetic subtraction exercise
            pass
    else: # exercise["type"] == "modular_arithmetic"
        # Check what operation within the modular arithmetic operations we need to solve
        if exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            pass
        elif exercise["operation"] == "addition":
            # Solve modular arithmetic addition exercise
            pass
        elif exercise["operation"] == "substraction":
            # Solve modular arithmetic substraction exercise
            pass
        elif exercise["operation"] == "multiplication":
            # Solve modular arithmetic multiplication exercise
            pass
        elif exercise["operation"] == "inversion":
            # Solve modular arithmetic inversion exercise
            pass


    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)

#removes the sign from the beggining and puts True for negative values and False for positive values
def sign ():
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


def loop(m, x, y, radix, signedX, signedY, answer, operation):

    carry = 0
    ans_sign = ''

    for i in range(m+1, 1, -1):

        dictX, dictY = get_operands(x, y, i, i, signedX, signedY)

        if operation == '+':
            addResult = dictX + dictY + carry
        else:
            addResult = dictX - dictY - carry

        if addResult >= radix:
            answer[i] = str(radix_dict[str(addResult - radix)])
            carry = 1
        else:
            # if -x[i] - y[i] = -c < 0
            if addResult < 0:
                addResult = -addResult
                ans_sign = '-'
                # if |c| > radix
                if addResult >= radix:
                    answer[i] = str(radix_dict[str(addResult - radix)])
                    carry = 1
                    continue
            answer[i] = str(radix_dict[str(addResult)])
            carry = 0

    answer[1] = str(carry) if carry == 1 else ans_sign
    answer[0] = ans_sign if carry == 1 else ''

    return ('').join(answer)


def integer_addition(x: str, y: str, r: int):

    m, signedX, signedY, x, y = determine_m(x, y)
    radix = r
    answer = list('0' * (m+2))
    xz = '0' * (m - len(x))
    yz = '0' * (m - len(y))

    xx = xz+x
    yy = yz+y

    answer = loop(m, xx, yy, radix, signedX, signedY, answer, '+')

    return answer

def integer_subtraction(x: str, y: str, r: int):
    m, signedX, signedY, x, y = determine_m(x, y)
    radix = r
    answer = list('0' * (m+2))
    xz = '0' * (m - len(x))
    yz = '0' * (m - len(y))

    xx = xz+x
    yy = yz+y

    answer = loop(m, xx, yy, radix, signedX, signedY, answer, '-')

    return answer


def multiplication_karatsuba(x,y, length, radix):
    xH = 0
    xL = 0
    yH = 0
    yL = 0
    answer = 0
    number2 = 0
    number0 = 0
    number1 = 0

    if (length == 1):
        int_x = int(radix_dict[x])
        int_y = int(radix_dict[y])
        int_xy = int_x * int_y
        right_digit = str(radix_dict[int_xy % radix])
        left_digit = str(radix_dict[int_xy // radix])
        return left_digit + right_digit

    
    if (length % 2 != 0):
        length += 1
    xH = x[:len(x)//2]
    xL = x[len(x)//2:] #x = xH*pow(radix, length/2) + xL
    yH = y[:len(y)//2]
    yL = y[len(y)//2:] #y = yH*pow(radix, length/2) + yL

    #need to figureout how to handle the numbers so that I transfer them into ints on which manipulations can be made

    number2 = multiplication_karatsuba(xH,yH, length/2, radix)
    number0 = multiplication_karatsuba(xL, yL, length/2, radix)
    number1 = multiplication_karatsuba(integer_addition(xH, xL, radix), integer_addition(yH, yL, radix), length/2, radix) - number0 - number2
    answer = number2*pow(radix, length) + number1*pow(radix, length/2) + number0

    return answer

def extended_euclidean_algorithm(x, y, radix):
    a1 = 1
    a2 = 0
    b1 = 0
    b2 = 1
    while(y > 0):
        q = x // y #find a way to do divison??? get radix rep of number?
        q_length = len(str(q))
        r = integer_subtraction(x, multiplication_karatsuba(q, y, q_length, radix), radix) #change to functions -,*
        x = y
        y = r
        a3 = integer_subtraction(a1, multiplication_karatsuba(q,a2, q_length, radix), radix)
        b3 = integer_subtraction(b1, multiplication_karatsuba(q, b2, q_length, radix), radix)
        a1, b1 = a2, b2
        a2, b2 = a3, b3

    d = x

    return d, a1, b1
    
def modular_addition(x, y, mod, radix):
    z = integer_addition(x, y, radix)
    if z < mod:
        z = z
    else:
        z = integer_subtraction(z, mod, radix)
    return z

def modular_subtraction(x, y, mod, radix):
    z = integer_subtraction(x, y, radix)
    if z >= 0:
        z = z
    else:
        z = integer_addition(z, mod,radix)
    return z


