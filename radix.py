

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
    length = m


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

            carry = -1 if dictX >= radix else 0

            answer[i] = str(radix_dict[str(addResult)])

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
    mainRow = []
    rows = [] 

    # for i in range(len(y) - 1, -1, -1):  # digits of y
    #     smallRow = []
    #     for j in range(len(x) - 1, -1, -1):  # digits of x

    #         dictX, dictY = get_operands_multiplication(x, y, j, i)

    #         decimal_result = (dictX*dictY)

    #         radix_rep = get_radix_rep(decimal_result, radix)

    #         smallRow.append(radix_rep)
        
    #     mainRow.append(row_handler(smallRow, radix))

    # answer = row_handler(mainRow, radix)

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

    ans = ''
    if (get_sign(x) and not get_sign(y)) or (get_sign(y) and not get_sign(x)):
        ans = '-' + ('').join(answer)
    else:
        ans = ('').join(answer)
    
    return ans


# print(integer_multiplication_naive('FA', 'ED', 16))
# start = time.time()
# print(integer_multiplication_naive('7318665512158743638605182887841371307645447670453461740187886842285460110804256310080546155485046778363608500110234673013838173017530458560706070707713126821437573764342276656812630301431186825833037171346785113265346706601833378432566821732766823504286847488473054082610767630565405366804425587637823220651072351816738606021587177867035623716605483826508470114323656412447422807454032367513124246015323416112182132054273176446604471300367702035745834407032504734726667023080565283532517442762276238705877865570885436235744740846486366253535015023376404043763460661258664436614051817602265626070244257100354382015048561821742532626321271578412315816728867218707756147730355350321051353434236566277464765475375722376650448828467235121544641156704737478520252122115548843021301055746020380530774067163516800828720580320271270605087218011550255735266202788214122168247323320745730580777657424033776206203451855366227147377245808053335756414852704156422263474050542137280505780427261724671205814557631620757174762032204028602827034520754515245703031776', 
#                                    '1568771344525852324131804138148802505753257655173371724107105074660656230256628473027874674317757244822742785775663506723327534180715833703401071617465314742013234485351032251153484185260643450668626460448745460515241258237763321043703485518743552650433714870524446615224154425234286032310515133387707535123238512533440840472803784711524486015757410618876707187324022408475576848040381272661523864655688161205714253833387667026225548576215854008022548134662252657616744431415734100732757365863174682653500871865607764257075563835252560604175301460027857128350521536551273818187830400435520571101247334433180242741245114184707620814625828800254801811811413885670316827435341526387147025782021133408383157028623231638776754840477052374530383586615072887426603342024213002804087201076322070118220818651821324506303733788248420286165404115511176562077205831100403111555008375135508124338773828723055185025888857703075881317146746180376668247185570372867688347354744578624718880138114621746257421442600554133510357462852040747022858481345676448874732072', 
#                                     16))
# current = time.time()
# print(current - start)

#print(create_table(16))



#print('-110822B99C0AF663CE39FCDCA05AA77EA7D95C56A3F3BDE18B1236FAA5F138188D8DDD9FD60E6A461D5BBA368721C9C6C65F0474A4877538BB3B969FACD3B9FBADD64EE02575A7D8BFE8BF5019EE89DAACECD29B85F6D7CBE0B60FA8CC28A64BE96CF24B08F2CEC60A1E7839B1021530C0174618EC5AB4F77DB3D68E9D62C7A1B4A18EEF04560C91B755EF152F2833CB5F32D05C5961AB99B2C731946F6D1123FF9809FF448A0DD5DE76330EEA6C1CD030E3C630590D8542F61F7A537B51744120DF223E11A62010D1B99B43E2C8DB045501134BC9FD6B3FC614FF1DFCD97FB7A899A0BBC5F58978138A7CAF962D3A9A8C75EFA3F0FBFA53C0C450C086A09C7D1B884722B7243002CF9CBE499E050352E62970FEBFF5CC8B92C191D108DCA9A9493E123EC7A9E984B3B149ECA320C8EE7B5292CE9EC1F7B833983FD4EFF94827AB5AED7088A3565E700B4EC8D171847A1E043D1D4CE6A99857DE80BC2BBE789A68AAEEAC36E3F33E091130B095AD1592A7D6E8D80FAEDD24CB03F04CCC094E820C4B7D304F611EFB75E1A9DFB0FA8BA6751864AF845029129DC0B4285FB3BD34' == '-30A42BB9E2AF863D039FEDEC07AC97EC9DB5C78C3F3BE038D14571AC6135A18AF8DDD9FD8106C681F5BBA56A941CBE6E6612694A6A9953ABD3BB69FACF5B9FBADF84F004595A7F8BFEAC17219EEA9FCACECD29B8616D7CC00B80FA8CE28C84BEB6D144D0914CEE80C1E7A39D3243752E2396618EE5CD5177DD3F68E9D82C9C1D4C18EF126780EB1B755EF172F4A35EB5F52D25C5B81CD9BD4C93196716F1144019A0A01648C0DF5DE78350F0A6E1CF250E3C8527B0DA74318217C737D51966140E1423E11A84230F1B99D6402E8FD267701354BC9FF6D41E834FF1DFCF97FD7C899C0BBE615AB78358A7CB1982F3C9A8C95EFA3F11BFC53E0E470E088C2BC7F3BAA4942B9445224CF9EC06BA027237308499100BFF5EC8B92C3B1F328DCABAB4940343EC9A9E986D3D169EEA540E8EE7D7492CE9EC1F9BA35B83FF4F0194A27AB5AED9288A35860922B4EC8F371849C20063F3D4D06AB9A77DEA0BE2BC0989C88AAF0AC57041340093150D0B5AF17B2A7F708DA0FAEDF24CD24124CEE2950840C6D7F524F611EFD9603A9DFD0FC8BC8971884AF84502B329DE0D6285FD3BF54')


print(integer_subtraction(x= "-222",
    y="-532",
    r= 10))