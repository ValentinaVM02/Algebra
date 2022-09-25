

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

def get_key(val):

    for key, value in radix_dict.items():
        if val == value:
            return key
 
    return "key doesn't exist"
        

def anyBaseToDecimal(string, base):
    base = int(base)
    integer = 0
    for character in string:
        assert character in radix_dict
        value = radix_dict[character]
        assert value < base
        integer *= base
        integer += value
    return integer

def decimalToAnyBase(number, base):
    if base < 2 or base > 16:
        return False
    remainders = []
    while number > 0:
        remainders.append(get_key(number % base))
        number = number // base
    remainders.reverse()
    return ''.join(remainders)

def clean_str(s:str):

    index = 0 if s[0] != '-' else 1

    while len(s) > 1:
        if s[index] == '0':
           s = s[1:] if not get_sign(s) else s[0]+s[1:]
        else:
            break 
    
    
    return s



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

    lenx = len(x)
    leny = len(y)
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


def get_operands(x, y, i):
    # index - 2 since the answer contains extra 2 indices
    index = i - 2
    x_index = int(radix_dict[x[index]])
    y_index = int(radix_dict[y[index]])
    # convert index to corresponding digit (i.e. '2' -> 2, 'A' -> 10) and sign (i.e. '-A' -> -10)

    return x_index, y_index


def loop(m, x, y, radix, signedX, signedY, answer, operation):

    carry = 0
    ans_sign = ''

    # if x,y < 0 and operation is addition, then adding them together and converting the result to negative suffices
    if ((signedX and signedY) and operation == "+") or ((signedX and not signedY) and operation == "-"):
        ans_sign = '-'

        for i in range(m+1, 1, -1):
            dictX, dictY = get_operands(x,y,i)

            addResult = dictX + dictY + carry

            carry = 1 if addResult >= radix else 0
            addResult -= radix if carry == 1 else 0

            answer[i] = str(radix_dict[str(addResult)])   
    
    
    # if x,y>0, then adding each bit suffices
    elif ((not signedX and not signedY) and operation == "+") or ((not signedX and signedY) and operation == "-"):

        for i in range(m+1, 1, -1):
            dictX, dictY = get_operands(x,y,i)
            addResult = dictX + dictY + carry

            carry = 1 if addResult >= radix else 0
            addResult -= radix if carry == 1 else 0
            answer[i] = str(radix_dict[str(addResult)])   

    # if x,y > 0, then subtracting each digit and 
    elif ((not signedX and not signedY) and operation == "-") or ((not signedX and signedY) and operation == "+"):

        for i in range(m+1, 1, -1):

            dictX, dictY = get_operands(x,y,i)
            
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


    elif ((signedX and signedY) and operation == "-") or ((not signedY and signedX) and operation == "+"):
        loop(m,y,x, radix, False, False, answer,"-")
      
     
    answer[1] = str(carry) if carry == 1 else ans_sign
    answer[0] = ans_sign if carry == 1 else ''

    return ('').join(answer)


def integer_addition(x: str, y: str, r: int):

    # print('addition', x, y)

    m, signedX, signedY, x, y = determine_m(x, y)
    radix = r
    answer = ['0'] * (m+2)
    xz = '0' * (m - len(x))
    yz = '0' * (m - len(y))

    xx = xz+x
    yy = yz+y

    answer = loop(m, xx, yy, radix, signedX, signedY, answer, '+')

    return answer


def integer_subtraction(x: str, y: str, r: int):

    m, signedX, signedY, x, y = determine_m(x, y)
    radix = r
    answer = ['0'] * (m+2)
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

        # store the least significant bit of the result since that wont change anymore
        ans += result[len(result) - 1]

        result = result[0:len(result) - 1]

        values.pop(i)
        values[i] = result
    
    # concat the last result of the values with accumilated bits (reversed since least significant at index = m - 1)
    ans = values[0] + ans[::-1]

    if ans[0] == '0':
        ans = ans[1:]

    return ans


# use hexhero to create an array of carries and add them at the end and adjust all positions to fit hex numbers
def integer_multiplication_naive(x: str, y: str, r: int):
    
    # m = len(x)+len(y) (x,y without signs)
    radix = r

    # m + 1 because index 0 is for the sign
    rows = [] 

    ans = '-' if (get_sign(x) and not get_sign(y)) or (get_sign(y) and not get_sign(x)) else ''

    x = x[1:] if get_sign(x) else x    
    y = y[1:] if get_sign(y) else y

    num_x = anyBaseToDecimal(x,radix)

    for i in range(len(y) - 1, -1, -1):
        num_y = anyBaseToDecimal(str(radix_dict[y[i]]),radix)

        result = decimalToAnyBase(num_x * num_y, radix)

        rows.append(result)

    answer = row_handler(rows, radix)
    
    return ans+('').join(answer)

print(integer_addition('0', '6', 11))
