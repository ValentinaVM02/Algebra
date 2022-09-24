

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

    seconds = time.time()
    local_time = time.ctime(seconds)
    print(local_time)

    # m = len(x)+len(y) (x,y without signs)
    radix = r

    # m + 1 because index 0 is for the sign

    smallRow = []
    mainRow = []

    for i in range(len(y) - 1, -1, -1):  # digits of y
        smallRow = []
        for j in range(len(x) - 1, -1, -1):  # digits of x

            dictX, dictY = get_operands_multiplication(x, y, j, i)

            decimal_result = (dictX*dictY)

            radix_rep = get_radix_rep(decimal_result, radix)

            smallRow.append(radix_rep)
        
        mainRow.append(row_handler(smallRow, radix))

    answer = row_handler(mainRow, radix)

    ans = ''
    if (get_sign(x) and not get_sign(y)) or (get_sign(y) and not get_sign(x)):
        ans = '-' + ('').join(answer)
    else:
        ans = ('').join(answer)

    seconds = time.time()
    local_time = time.ctime(seconds)
    print(local_time)
    
    return ans


print(integer_multiplication_naive('FA', 'ED', 16))
print(integer_multiplication_naive('7318665512158743638605182887841371307645447670453461740187886842285460110804256310080546155485046778363608500110234673013838173017530458560706070707713126821437573764342276656812630301431186825833037171346785113265346706601833378432566821732766823504286847488473054082610767630565405366804425587637823220651072351816738606021587177867035623716605483826508470114323656412447422807454032367513124246015323416112182132054273176446604471300367702035745834407032504734726667023080565283532517442762276238705877865570885436235744740846486366253535015023376404043763460661258664436614051817602265626070244257100354382015048561821742532626321271578412315816728867218707756147730355350321051353434236566277464765475375722376650448828467235121544641156704737478520252122115548843021301055746020380530774067163516800828720580320271270605087218011550255735266202788214122168247323320745730580777657424033776206203451855366227147377245808053335756414852704156422263474050542137280505780427261724671205814557631620757174762032204028602827034520754515245703031776', 
                                   '1568771344525852324131804138148802505753257655173371724107105074660656230256628473027874674317757244822742785775663506723327534180715833703401071617465314742013234485351032251153484185260643450668626460448745460515241258237763321043703485518743552650433714870524446615224154425234286032310515133387707535123238512533440840472803784711524486015757410618876707187324022408475576848040381272661523864655688161205714253833387667026225548576215854008022548134662252657616744431415734100732757365863174682653500871865607764257075563835252560604175301460027857128350521536551273818187830400435520571101247334433180242741245114184707620814625828800254801811811413885670316827435341526387147025782021133408383157028623231638776754840477052374530383586615072887426603342024213002804087201076322070118220818651821324506303733788248420286165404115511176562077205831100403111555008375135508124338773828723055185025888857703075881317146746180376668247185570372867688347354744578624718880138114621746257421442600554133510357462852040747022858481345676448874732072', 
                                    16))



