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
from radix import get_radix_rep, integer_addition, integer_subtraction
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
        r = integer_subtraction(x, multiplication_karatsuba(q, y, length, radix), radix)
        x = y
        y = r
        length = max(len(str(q)), len(str(a2)))
        a3 = integer_subtraction(a1, multiplication_karatsuba(q, a2, length, radix), radix)
        length = max(len(str(q)), len(str(b2)))
        b3 = integer_subtraction(b1, multiplication_karatsuba(q, b2, length, radix), radix)
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
    x1, x2 = 1, 0
    while(mod>0):
        q = division(x, mod, radix)
        q_length = len(str(q))
        r = integer_subtraction (x, multiplication_karatsuba(q, mod, q_length, radix), radix)
        x, mod = mod, r
        x3 = integer_subtraction (x1, multiplication_karatsuba(q, x2, q_length, radix), radix)
        x1, x2 = x2, x3
    
    if x == 1:
        return x1
    else:
        print('inverse does not exist')

# x = "2055874C17B6A157153A43DD9CA6349B57C59904C050A2BA3635B496781294B820B46610105DBC41D3B6D362984574C00468984B4831B5313D83573524A46D6746A28D0A54B82B5162B1CB001DD99661D65227130B7CD0AC08AB153B32972D216AB9D4C211A1ADC184182C596327B7DD263C4CCB04AC531C4D48CC91625086D3BAD0187B990535864364674C5A4A281037A27C8249A76D65C3CD7275AB224D865C9A4C8504D1AB7289DCC6DBC79242AB3A0589AB81D68D187B1581DD44A9255C5C7AD640C646D346B8BA8D5DC5954C337AD33284335999C105C78AA379BA1A439BBC481CA705029A3548375B47295D93B39B9A50ABB225157310860144B989B872766A75B276DB5167AD8DA62C503AA85837A13A96463DC72638D7842589C81616A809601907A2A85171B335573A2B01798292C951BA0137B6A8D21B27DA494622917D0CC01288D8212B7657706A9AC836D8703B1B1DB03209A6196938D372543631917A7D0A7C34632AA1C289D3415334C7B79B3A40C020C145A18DCCCAA4DD94D944DBD02C265088D080367901051D585C8D3C1A2D1117D34586D7ACAD582BD7D592D73CCD1CA586D3D973D3CC89C0BA23B9D80"
# y = "2D0D08BB790302A19964CA7297121C6AC3103331271802D9718C7278AA5C13C82929751710A625CA6D723526BCC226B782A49AD27A4BC71C3C3B85A977B1CDA6189DAD6AA82A81B763B1CC880A11B08347044455A920B65077C7DC3442ACBA3A4519937D2349B0189B67138612CCAD1307746BAB2B8219A64175CA5A28C87191DD9BB589C057AAC5B211386A320B6522D90065D3D17B792187DC2568384B0C7256AD65B48372C52AA121400644130B8165AD174C22D814D710AD8A477331B6252967341086B0CB90D305A5C68691C0A69AA1A410532944A03D3D6A4ABB193DABCB95601B43BA1B789AB9706B04389A0AC5BC45B85C701449B711CB1C96C704BB2B2D869B75352BD5C06B18BBC26D2C3C17CB2A4269CB1A3A0A088931B697D78B15D16BB1513BC6A4B8446CB8965C60813B4632DD6231C2171ABD2C00B277822715A02D31C517159D3C88BA159D4A62C8BC1A9325B601D6BB653AC7161DD39B2CA48B23121A41BD904B6D88781AD897A6B78AA83D2A28596854207842AD9CC2D059DB1680A3DABB5823314C745A65B2D51C67C8A65229C133A4C6CA30C862B5D69DAB2332208A7DA09226968CA9186D9A63C40C803"
# start = time.time()
# result = extended_euclidean_algorithm(y, x, 14)
# current = time.time()
# print(result)
# print(current - start)


# x ="13113033243303203040341433103011311233423224102014244223321411111300142204302311202223020433004033044214134133244232322434402024410402104023300023033322304314101404133001404333102022014101233303204230303230422413243144314212114431342030433222401233401311301202032314403001033412210011240002222131014400441431024234204301214413220310220323144130011433010031201132013120344104043433140200230234024404432241033200423211033100440321241030334330221111302003032310222213023241131104041224241203212223040112303100412021304424024413130340400002114004411114002400104200041231402220203413114323224131040440430332244213224303344132344231322232310114443021201340004040144204331012401343102440331000114211011032440322041423220330001344323101110323103232021030413132133231104203410411404242110241333414121040333311134211314232111224133140333412412422023401403311104101042143042202114440212213232030140202300114413223044304434104412313422412201210133042111400142344434241021434342223301321241344323303014202230341222010132312400401041443144304332324432143403314141004240204140022403141421030023143143012212302243324342404233211302201324124121440011110110014140320331124022103344041312034330440434014044422202211241344122200403343101041203414442311123010342123112301430411030024122004000010401310304414333233421230120202404103044311104403003203402032443002410110331234210313310311224012444302241443013011303014220100213102114201030011431241211130"
# y = "200122333323122421432313220232211004021120142200411014313132101431142434202203400212012222104410143034230322100303304330133132440231141021133142110410141214300143332340301022210404211004342232240130242031344401111431314221420141420114234303321310330314241114121031401123044241202224301404044143413233422332032224012312100334231030332104333032313321303243434442033231010402334324342402433022404113334443202033121241043003140002203233302020020241433004424102101330030202130033333104443231222142310423133011414121202102403041021340301220044413214123101434331131022301313034010144213213304214420133321444022041241030134440144321331344421021004142312411220331222040244142414413014003343232444400113201434244322400333302100000113311334213044441120433020201133302342314114332234421144244122140102320140110401000344414213220134242010331410424132423204423242103033140324044404112132331134440042432021444313120303242220040431233140320444442422132331212141333142122133012110442010112100002100221332232221134013200003001031202444242001344213413003413202311432002004021320244132343332013002121032323131221223234202332233012444103223211032123400110102120434422043023242234324003114232144040300132441032423144000341443424222410413414013342412124031414112140300420320044134000402334443140343332311144414210211443442241224103423444042303301344002204044304340342401030120314041111333124134341340324001343122314111214111304323220043202042031213424003"
# modulus = "124420141100344331213220142234212133433211221322200210133331022130223221113132114242001104142112134434112442100220401143223133403023110023013440431340301222411441320241323230120134111440413231124433300422113240221431211221023013124224034422103001203434204203010040420413141321241110212043043400111011340322124024030310040242013413243030412322401201303344220224421030420424130404031134331223220310140321122011342212403243013214443021421413420321231001321432140011404100320134044424434413410410143143034333300422343022224111423134401442320402440143234023231031212411003324030142034103221113240032003200434104123132012211111204432112041134432042443244303403100034420034234120021342100241410124431304142133344334020230243212331242003304012020110242221024410343212331113412100423022244323014042444322202242131031402224134220043332241214431301331241143311010102024243131224111033411321201033214233003213412012300120144003244403002114420421001223144423321420204132221110122421421320340310222201242220233224132024423344341113334021303143033334340304333421414231411131403232323332041034014231113211220140120144200032204220444141232442243231300110212101011101330203204140012231121324322110322320403243320244232111013101422440334234034230041134401100032443404432130043244130300244443130204300031043122102413131004030441334421003430233421002132434410030410412013210023131344333143033100104130113101020211243212014244100323040014310143443212234"

result = modular_addition('A', '2', '5', 16) 
print(result)

#invalid inputs
