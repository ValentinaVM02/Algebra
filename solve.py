##
# 2WF90 Algebra for Security -- Software Assignment 1 
# Integer and Modular Arithmetic
# solve.py
#
#
# Group number:
# group_number 
#
# Author names and student IDs:
# author_name_1 (author_student_ID_1) 
# author_name_2 (author_student_ID_2)
# author_name_3 (author_student_ID_3)
# author_name_4 (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json
from locale import RADIXCHAR
from multiprocessing.managers import ValueProxy

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
        # et cetera


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
        #varX = int(varX)
        conversionX = True
    else:
        #varX = int(varX)
        conversionX = False

    if sign in varY:
        varY = varY[1:]
        #varY = int(varX)
        conversionY = True
    else:
        #varY = int(varY)
        conversionY = False

# this is the function that considers the letters of the alfabeth when trasfering to decimal so the A,B,C,D..... all signs 
def valueNum (n):
    if n >= '0' and n <= '9':
        return ord(n) - ord('0')
    else:
        return ord(n) - ord('A') + 10

#change of radix with the help of valueNum (changes the Alphabet into numbers) and then chr() to go back to alphabet
def radixFun ():
    sign()

    global radix
    global varX
    global varY
    global answer
    global lengthNumX
    global lengthNumY

    power = 1
    changedX = 0
    changedY = 0
    lengthNumX = len(varX)
    lengthNumY = len(varY)

    #changing to base 10
    if (radix < 2 or radix > 16):
        answer = "Incorrect radix"
    else:
        for i in range(lengthNumX - 1, -1, -1):
            if valueNum(varX[i]) >= radix:
                print('Invalid number')
            changedX += valueNum(varX[i])*power
            power *= radix
        varX = str(changedX)
        for j in range(lengthNumY - 1, -1, -1):
            if valueNum(varY[j]) >= radix:
                print('Invalid number')
            changedY += valueNum(varY[j])*power
            power *= radix
        varY = str(changedY)


def integer_addition ():
    radixFun()
    
    global radix
    global varX
    global varY
    global conversionX
    global conversionY
    global answer
    global lengthNumX
    global lengthNumY

    carry = 0 
    #append to string
    # making a dictionary for A,B,C,D,E,F --> maybe we can use the valueNum function when we add them but then I am 
    for i in range (max(lengthNumX,lengthNumY) - 1, - 1, - 1):
        answer[i] = str (int(varX[i]) + int(varY[i]) + carry)
        if answer[i] >= radix:
            answer[i] = answer[i] - radix
            carry = 1
        else:
            carry = 0
    if (carry == 1):
        k = max(lengthNumX, lengthNumY) + 1 

    #if (conversionY == False and conversionX == False):
    #    answer = varX + varY
    #elif (conversionY == False and conversionX == True):
    #    answer = varY - varX
    #elif (conversionY == True and conversionX == False):
    #    answer = varX - varY
    #elif (conversionY == True and conversionX == True):
    #    answer = - varX - varY 
    

    


def integer_subtraction():
    radixFun()
    global radix
    global varX
    global varY
    global conversionX
    global conversionY
    global answer

    # confused :(
    if (conversionX == False and conversionX == False):
        return 0
    elif (conversionX == False and conversionY == True):
        return 0
    elif (conversionX == True and conversionY == False):
        return 0 
    elif (conversionX == True and conversionY == True):
        return 0





def multiplication_primary():
    return 0


def mutiplication_karatsuba():
    #finish it before midnight
    return 0


def extended_euclidean_algorithm():
    return 0

