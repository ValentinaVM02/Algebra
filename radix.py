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


# use hexhero to create an array of carries and add them at the end and adjust all positions to fit hex numbers
def integer_multiplication_naive(x: str, y: str, r: int):

    # m = len(x)+len(y) (x,y without signs)
    m, signedX, signedY, x, y = determine_m_multiplication(x, y)
    radix = r

    # m + 1 because index 0 is for the sign
    answer = ['0'] * (m+1)
    answer[0] = '-' if (signedX and not signedY) or (signedY and not signedX) else ''
    carry = 0
    ans_index = m
    counter = 0


    for i in range(len(x) - 1, -1, -1): # digits of y
        carry = 0
        ans_index = m - counter
        for j in range(len(y) - 1, -1, -1): # digits of x
            row = [0] * (len(x) + 1)
            # get operands
            dictX, dictY = get_operands_multiplication(x, y, i, j)

            # get decimal product
            decimalResult = (dictX * dictY)

            # get radix representation of the decimal result
            rad_result = get_radix_rep(decimalResult, r)

            
                     
        
        counter += 1

    for index in range(1, len(answer)):
        answer[index] = str(radix_dict[str(answer[index])])



    return ('').join(answer)


#print(integer_multiplication_naive('FF', 'FF', 16))

#print(integer_multiplication_naive('2E6C', 'AF3', 16))


def modular_reduction(x:str, m:str, r:int):
    
    xPrime = x[1:] if get_sign(x) else x

    k = len(x)

    n = len(m)
    

    return 
