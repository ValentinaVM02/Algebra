

from array import array
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


#print(integer_addition('A', 'A', 15))
# print(integer_addition('8980167853058A1BB849ABAA66B628B502A33811590775327680B590530919A09128A33B889612707B7594276816B654954B59A39557149412749317B96A773A10819572B96BA99A99508B934602B4351BAA19858AB3735B522983634B86430909304A9BB807A528A77B07B969647671B0152718678589732B08491559A8BB07B785B99435772824984852114938783383311A30086B280B56051B40BA54A9A68B4B0033481296282A9BB215B00A4013381844598679B716B01A2A4A291595B109122916707341BB347B84075A749207144AA27277897168467A57907A759B21497BB5352391989A5A33437695A332816346B637401153A874206523B27BBA5B301899AB973290A31171A561184B8312337BB566A7B53A2904AA041289B7513196947463028A59AA24828347086644A57938015A2473818B44430BB623B014B7264B1A893314905A54695724759516A9530108376547154912A29AA2A9959468A6993770968A275168652B3A15B9B22A40A4B83A63A6448B479339B42B2513417B2A406354517454A399B5A48476B7396853AA7B648248BA3A357B783873598813315B30BA62380A0B41903714195489740B46B312AA05BB9BB8B4BB4B36BB7A256143872262131266422B38868B25',
#                        '43A22A402262367794B8BB153A4432A29089172896113A49479A7411B345B3221713A32612B79A2027038775A6B48A597494B9B52919837BA54AA380802979A0659A32A5748062344813088332A4506358006548681352A9B33745A3AB0A3A5536B9B06413498031546B74834133AA0869A726235B6BB0548B110823A1786565A2602292A13575819675B62B202A17875752857883903A969B92990A651B42995B0ABB31006A525A419A21917918098805159349B24516638B2662BA5B8B538A7155A4859ABB132B7482387735541B577435AB6244214310270A11431228732BA542488812552A302A892AA24304584487573681786AB2A9807A65233A6A1B16A8B5016947BBBA22936B0375787A1684119690A78465B30B50687A48782722A3BA96A0B12AB6271679084631AA32A777968930882280003A29414884A811B158317A5B5BB7B15B426481667263468A004B958675473B9586545781A9B6253B0BA462BABBA1834518AB54182B56BB87B4B47A45B3BA1153A0979726554133964829B95A50A5301B242BB04B361A4739839633A147A68A1450571349A984A10560732978898982A754304A617850A6496983AA49310045572AB811236B755558264489B0B39A264AB36256B7517451A4A',
#                        12))


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
def row_handler(values: array, r: int):
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

    multiples = create_table(r)
    
    for i in range(len(y) - 1, -1, -1):  # digits of y
        smallRow = []
        for j in range(len(x) - 1, -1, -1):  # digits of x

            dictX, dictY = get_operands_multiplication(x, y, j, i)

            radix_rep = multiples[dictX][dictY]

            smallRow.append(radix_rep)
        
        rows.append(smallRow)

    for index in range(0, len(rows)):
        rows[index] = row_handler(rows[index], radix)

    answer = row_handler(rows, radix)

    # ans = ''
    # if (get_sign(x) and not get_sign(y)) or (get_sign(y) and not get_sign(x)):
    #     ans = '-' + ('').join(answer)
    # else:
    #     ans = ('').join(answer)
    
    return ans+('').join(answer)

# start = time.time()
# print(integer_multiplication_naive('-535152611414755551232273360066476036736622060375407272326610245353267266277754403125103262054202637641560740707012443427215730033046622755220463024704232404227026011325244063345707610602204247540323042565423163415755061041045045456240767772245211213017632042037023746132535516733305642537757657604516325314600430600153027774237616353365625624344441510521530000540377652041007406631031733062527765753660275167527521761335237562420774304456102766774156151520512412150037302613034032753723754404376451151040622375672335055763337536174200200344343374743417435502512021720522264565551206056730626306617143737741012360713625655714210533630637045520366707064267664351664412312224333631767642555055055367452466425027566257315133463512317537007011650010565751600725176662236546667663006214222167250374132057276716201413115107046336115522107504036526234707650575434620725067456630510151304257413622516623010216252565462241711100415121015216452300633042235771700504232071442355041073300336507222155655741423502713430665162371314660171154271040137376770551665365530447105374520065171300772264654067507622151336304576110', 
#                                    '-403217032146052657410524404331703620475777000457560251015434643402702230141036603212660111347420403146366515473256315576443667470660453114675247165507475515161444357176042055417447631540745171374133267407257510113644544365414717213062317421315071507173506367251602544516462627221245047563755057422470442654305127365552314472120571635036624561343327214612315602652547307454747354625763315022723776435755315450643606536641006045630766553717436003712015561524433556311161032576553663110451363113027322066224273614727010510721434104221461715411347770473624503262115342373306543042207435750763305543706542110577164360431703746610573343105014642633357246560135024611610510347054353266363573314760702147545713346300157456276512734107252173177305217577302473532641136622400302321113044624177506041011176043402766615307676451010572034211677120246036630433626341007262574766340320722511471314245670372633135336273675760521553453124244544411755072504726620445077540012074567605151443022602613407016065631245205706722260251413047737153423101655157000367213651710030571705630451451770415340655131304246534117335363517304', 
#                                     8))
# current = time.time()
# print(current - start)