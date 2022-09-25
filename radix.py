

from Features import decimalToAnyBase, anyBaseToDecimal
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


def get_sign(a):
    return True if a[0] == '-' else False

def get_radix_rep(a: int, r: int):
    m = 0
    num = int(a)
    while num >= r**m:
        m += 1

    rep = ['0'] * m
    rem = 0
    co = num
    for i in range(m-1, -1, -1):
        co = int(num / (r))
        b = str(num - co * r)
        rep[i] = str(radix_dict[b])
        num = co

    return ('').join(rep)

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

def create_table(r:int):
    multiples = []

    for i in range(0, r):
        multiple = 0
        row = [] * r
        for j in range(0, r):
            multiple = i*j
            multiple = get_radix_rep(multiple, r)
            if multiple == '':
                multiple = '0'
            row.append(multiple)
        multiples.append(row)
    
    return multiples


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

    if (signedX and signedY) and operation == "+":
        ans_sign = '-'

        for i in range(m+1, 1, -1):
            dictX, dictY = get_operands(x,y,i,i, signedX, signedY)
            dictX, dictY = -dictX, -dictY

            addResult = dictX + dictY + carry

            carry = 1 if addResult >= radix else 0
            addResult -= radix if carry == 1 else 0

            answer[i] = str(radix_dict[str(addResult)])   

    elif (not signedX and not signedY) and operation == "+":

        for i in range(m+1, 1, -1):
            dictX, dictY = get_operands(x,y,i,i, signedX, signedY)

            addResult = dictX + dictY + carry

            carry = 1 if addResult >= radix else 0
            addResult -= radix if carry == 1 else 0
            answer[i] = str(radix_dict[str(addResult)])   

    elif (not signedX and not signedY) and operation == "-":

        for i in range(m+1, 1, -1):

            dictX, dictY = get_operands(x,y,i,i,signedX,signedY)
            
            if i == 2 and dictX < dictY:
                addResult = -(dictX - dictY + carry)
                answer[i] = str(radix_dict[str(addResult)])
                ans_sign = '-'
                continue

            dictX += radix if dictY > dictX else 0
            addResult = dictX - dictY + carry
            addResult = 0 if addResult < 0 else addResult
            answer[i] = str(radix_dict[str(addResult)])
            carry = -1 if dictX >= radix else 0


    elif (signedX and signedY) and operation == "-":
        loop(m,y,x, radix, False, False, answer,"-")
      
     
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


#print(integer_subtraction('-A', 'F', 16))


def determine_m_multiplication(x, y):
    signedX = get_sign(x)
    signedY = get_sign(y)

    x = x[1:] if signedX else x
    y = y[1:] if signedY else y

    m = len(x)+len(y)

    return m, signedX, signedY, x, y


def get_operands_multiplication(x, y, i, j):
    dictX = radix_dict[x[i]]
    dictY = radix_dict[y[j]]

    return dictX, dictY




#print(get_radix_rep('255', 16))


# the idea is to handle each multiplication as a row and add together all the rows at the end
def row_handler(values, r: int):
    ans = ''
    result = 0
    i = 0


    while i < len(values) - 1:

        valX, valY = values[i], values[i+1]

        valX = '0' + valX
        valY += '0'

        result = integer_addition(valX, valY, r)

        ans += result[len(result) - 1]

        result = result[0:len(result) - 1]

        values.pop(i)
        values[i] = result
    
    ans = values[0] + ans[::-1]

    if ans[0] == '0':
        ans = ans[1:]

    return ans


# use hexhero to create an array of carries and add them at the end and adjust all positions to fit hex numbers
def integer_multiplication_naive(x: str, y: str, r: int):

    
    # m = len(x)+len(y) (x,y without signs)
    radix = r

    # m + 1 because index 0 is for the sign

    smallRow = []
    rows = [] 

    ans = '-' if (get_sign(x) and not get_sign(y)) or (get_sign(y) and not get_sign(x)) else ''

    x = x[1:] if get_sign(x) else x    
    y = y[1:] if get_sign(y) else y

    for i in range(len(y) - 1, -1, -1):
        num_y = anyBaseToDecimal(str(radix_dict[y[i]]),radix)
        num_x = anyBaseToDecimal(x,radix)

        result = decimalToAnyBase(num_x * num_y, radix)

        rows.append(result)

    answer = row_handler(rows, radix)
    
    return ans+('').join(answer)

start = time.time()
#print(integer_multiplication_naive('-535152611414755551232273360066476036736622060375407272326610245353267266277754403125103262054202637641560740707012443427215730033046622755220463024704232404227026011325244063345707610602204247540323042565423163415755061041045045456240767772245211213017632042037023746132535516733305642537757657604516325314600430600153027774237616353365625624344441510521530000540377652041007406631031733062527765753660275167527521761335237562420774304456102766774156151520512412150037302613034032753723754404376451151040622375672335055763337536174200200344343374743417435502512021720522264565551206056730626306617143737741012360713625655714210533630637045520366707064267664351664412312224333631767642555055055367452466425027566257315133463512317537007011650010565751600725176662236546667663006214222167250374132057276716201413115107046336115522107504036526234707650575434620725067456630510151304257413622516623010216252565462241711100415121015216452300633042235771700504232071442355041073300336507222155655741423502713430665162371314660171154271040137376770551665365530447105374520065171300772264654067507622151336304576110', 
#                                   '-403217032146052657410524404331703620475777000457560251015434643402702230141036603212660111347420403146366515473256315576443667470660453114675247165507475515161444357176042055417447631540745171374133267407257510113644544365414717213062317421315071507173506367251602544516462627221245047563755057422470442654305127365552314472120571635036624561343327214612315602652547307454747354625763315022723776435755315450643606536641006045630766553717436003712015561524433556311161032576553663110451363113027322066224273614727010510721434104221461715411347770473624503262115342373306543042207435750763305543706542110577164360431703746610573343105014642633357246560135024611610510347054353266363573314760702147545713346300157456276512734107252173177305217577302473532641136622400302321113044624177506041011176043402766615307676451010572034211677120246036630433626341007262574766340320722511471314245670372633135336273675760521553453124244544411755072504726620445077540012074567605151443022602613407016065631245205706722260251413047737153423101655157000367213651710030571705630451451770415340655131304246534117335363517304', 
#                                    8))
current = time.time()
#print(current - start)
#print(integer_multiplication_naive('122', '211', 3))