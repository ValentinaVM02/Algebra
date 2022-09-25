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
from multiprocessing.managers import ValueProxy
from Features import modularReduction, modularInverse
from radix import get_radix_rep, integer_addition, integer_subtraction, integer_multiplication_naive
import time

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
    # m is the wordlength of result
    m, signedX, signedY, x, y = determine_m(x, y)
    radix = r
    answer = list('0' * (m+2))
    xz = '0' * (m - len(x))
    yz = '0' * (m - len(y))

    xx = xz+x
    yy = yz+y

    answer = loop(m, xx, yy, radix, signedX, signedY, answer, '-')

    return answer


def multiplication_karatsuba(x, y, length, radix):
    print(x, y)
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
    xH = x[:length//2] if length > 1 else x
    xL = x[length//2:] if length > 1 else x #x = xH*pow(radix, length/2) + xL
    yH = y[:length//2] if length > 1 else y
    yL = y[length//2:] if length > 1 else y #y = yH*pow(radix, length/2) + yL
    print(xH, xL, yH, yL)
    #need to figureout how to handle the numbers so that I transfer them into ints on which manipulations can be made
    print(integer_addition(yH, yL, radix))
    number2 = multiplication_karatsuba(xH,yH, length/2, radix)
    number0 = multiplication_karatsuba(xL, yL, length/2, radix)
    number1 = integer_subtraction(integer_subtraction(multiplication_karatsuba(integer_addition(xH, xL, radix), integer_addition(yH, yL, radix), length/2, radix), number0, radix), number2, radix)
    answer = integer_addition(integer_addition(integer_multiplication_naive(number2, "1" + length * "0", radix), integer_multiplication_naive(number1,"1" + (length // 2) * "0", radix), radix), number0, radix)

    return answer

def division(x, y, radix):
    i = 0
    while(x[:1] != '-'):
        x = integer_subtraction(x, y, radix)
        i += 1
    return get_radix_rep(i, radix)

def extended_euclidean_algorithm(x, y, radix):
    a1 = '1'
    a2 = '0'
    b1 = '0'
    b2 = '1'
    while(y[:1] != '-' and y[:1] != '0'):
        q = division(x, y, radix)
        length = max(len(str(y)), len(str(q)))
        r = integer_subtraction(x, integer_multiplication_naive(q, y, radix), radix)
        x = y
        y = r
        length = max(len(str(q)), len(str(a2)))
        a3 = integer_subtraction(a1, integer_multiplication_naive(q, a2,radix), radix)
        length = max(len(str(q)), len(str(b2)))
        b3 = integer_subtraction(b1, integer_multiplication_naive(q, b2,radix), radix)
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
        # for i in range (len(x)-1):
        #     if x[i] != y[i]:
        #         if x[i] > y[i]:
        #             x_greater = True
        #             break
        #         else:
        #             x_greater = False
        #             break
    else:
        x_greater = False
    return x_greater


def modular_addition(x, y, mod, radix):
    x = modularReduction(x, mod, radix)
    y = modularReduction(y, mod, radix)
    print(x)
    print(y)
    z = integer_addition(x, y, radix)
    if compare(z, mod):
        z = integer_subtraction(z, mod, radix)
    return z

def modular_subtraction(x, y, mod, radix):
    z = integer_subtraction(x, y, radix)
    if compare(z, '0'):
        z = z
    else:
        z = integer_addition(z, mod, radix)
    return z

# def modular_multiplication(x, y, mod, radix):
#     x_length = len(str(x))
#     z = multiplication_karatsuba(x, y, x_length, radix)
#     z = modular_reduction(z, mod, radix)
#     return z


def inversion (x, mod, radix):
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


print(multiplication_karatsuba('29','39', 2, 12))


# x = "2055874C17B6A157153A43DD9CA6349B57C59904C050A2BA3635B496781294B820B46610105DBC41D3B6D362984574C00468984B4831B5313D83573524A46D6746A28D0A54B82B5162B1CB001DD99661D65227130B7CD0AC08AB153B32972D216AB9D4C211A1ADC184182C596327B7DD263C4CCB04AC531C4D48CC91625086D3BAD0187B990535864364674C5A4A281037A27C8249A76D65C3CD7275AB224D865C9A4C8504D1AB7289DCC6DBC79242AB3A0589AB81D68D187B1581DD44A9255C5C7AD640C646D346B8BA8D5DC5954C337AD33284335999C105C78AA379BA1A439BBC481CA705029A3548375B47295D93B39B9A50ABB225157310860144B989B872766A75B276DB5167AD8DA62C503AA85837A13A96463DC72638D7842589C81616A809601907A2A85171B335573A2B01798292C951BA0137B6A8D21B27DA494622917D0CC01288D8212B7657706A9AC836D8703B1B1DB03209A6196938D372543631917A7D0A7C34632AA1C289D3415334C7B79B3A40C020C145A18DCCCAA4DD94D944DBD02C265088D080367901051D585C8D3C1A2D1117D34586D7ACAD582BD7D592D73CCD1CA586D3D973D3CC89C0BA23B9D80"
# y = "2D0D08BB790302A19964CA7297121C6AC3103331271802D9718C7278AA5C13C82929751710A625CA6D723526BCC226B782A49AD27A4BC71C3C3B85A977B1CDA6189DAD6AA82A81B763B1CC880A11B08347044455A920B65077C7DC3442ACBA3A4519937D2349B0189B67138612CCAD1307746BAB2B8219A64175CA5A28C87191DD9BB589C057AAC5B211386A320B6522D90065D3D17B792187DC2568384B0C7256AD65B48372C52AA121400644130B8165AD174C22D814D710AD8A477331B6252967341086B0CB90D305A5C68691C0A69AA1A410532944A03D3D6A4ABB193DABCB95601B43BA1B789AB9706B04389A0AC5BC45B85C701449B711CB1C96C704BB2B2D869B75352BD5C06B18BBC26D2C3C17CB2A4269CB1A3A0A088931B697D78B15D16BB1513BC6A4B8446CB8965C60813B4632DD6231C2171ABD2C00B277822715A02D31C517159D3C88BA159D4A62C8BC1A9325B601D6BB653AC7161DD39B2CA48B23121A41BD904B6D88781AD897A6B78AA83D2A28596854207842AD9CC2D059DB1680A3DABB5823314C745A65B2D51C67C8A65229C133A4C6CA30C862B5D69DAB2332208A7DA09226968CA9186D9A63C40C803"
# start = time.time()
# result = extended_euclidean_algorithm(y, x, 14)
# current = time.time()
# print(result)
# print(current - start)

# print(integer_subtraction('12022000201020100202110202112201020220112111222210002202201120121221110122120000212211021201122011022102212022102002002212102021000111122201210222101202020010202020211002020110000121222121212021020201210000122010220022012021021011212012012221112210021001011122212020222020102010102100221202022202111000202201222212122100121122002220112022010222121022211212110021202122000012020222111011222112112210200000020121020022212222202201211101021212022200211010010220121212010121020022022221122112201220121102202101110222022202212101122121121211211001020120120111210011122111100000201002221212021010202220120101001100012211010122122012121112012101210001011101000011021121222222222000220122112100112002121101112012201121112020122121220010012200221010100222210001002010200221220112010201222101200202211102210212012221201122120200020100011222111121201011211112120100012122022111010102100202210001102022120221111010222011222011210212021122111220102001111122000221220220110120122202002221011011001011020111222212021012200002012012221112002102000200112221011010011011102200100110021012210021222120200221121101112201101021110202021100012201210222012002222221122221100221122010002022211102020002002121221012211002012002021021101100111201112121111202202121002002120111012212121010121010012020111212010202212001020002201111222011000201021010220010010110211112021021220111002202112022120201112000202120221201221220202000022211111102011021122122111000022002122222020012210011220200001201112222112012200211012112222000122110011002221021211102000211220011121022111022122000120110022112111221011121010022112112111022201002112210001102112100112210222012021202012202000002200101001000120000001221122222110021100121220021101220012101102020221100111001001202111221000201221120221212122101220200111220102022000200200212021110022222001010211212021111112112112010220001101220021222211022100101012022120101102020110002211020001021112201000110100102100012012111101111011002001220220222000202120012211012221220012021221222110011221111020210000221010020110202001001212200212200000112110201021010111101222102021000222000222200021202', 
#                           '10222201201110112202022220210000122011002122010202121122111022100101211202000002111100121111211022011011021012220202011011010022001211121001021120001111202211002002110121012021101122111012020111012222020202102001000101022201000001012010102201210222101021012102200102101101110110221020110002202001200010001201012011000022111122001211221002121100012210120110111211011100012011221210210200002002021201021222221022101021212200200020112122012020102221200122010210001010121201012010210120011220010121110101200100222201101222221121200110022011022100212222011102121021102221022112221112002020022102010112112201021101002201002012100011022022102012011111021221120211222111010020012211111012120020010012211211222102001121112200201112101222101221010102221122210001110202002202211000201002102220001210001002010000202011021220011211201111202121120011002222012110202011020012112101021020200000100120001102121102220222100122011111200120201111222111122220101020221111120122022202120021002202020110010221120021010122012000100000212222202101001121221001100102220210222021212210111011022010102110110200120210022221011022221201110000121021210222220122010220221212021211102020221202111201122202222111020002201212000221000222202200111022211000211221020110210102222100102111201212001111020001001021001222000210010212200001201001011111102010222111201020211202121112122222002022120102100110201002121002201201121100102112001222111220012102100101102010112122201201211111221121222210221202012220120120210010100202200122101101012220200020121120210222111100221102220221102121122222011200022010120210120100120000222222210222210012100121021211211220012002122111022012211112012201222201122001222022201110110120002012121110001010221020200220220120011011100020212102022210210220221000222110220011220121220202000102220222102120011121201021221202101001112001221000200222222122000100221112020020100002021112002211000110012222202112200011200121122000000021020100110121021210110120020012021100111101101222221102111021111112221022202202101222212211101020021010010011120201002211121002021112221012100202202020112101211111222002002101112101',
#                           3))

# print(integer_subtraction('AFF', 'EDA', 16))
