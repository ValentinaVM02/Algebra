import numbers, string
from shutil import register_unpack_format


radix_dict = {'0': 0,
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
         'F': 15}


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



def modularReduction(x,m,base):
    base = int(base)
    if base != '10':
        x_int = anyBaseToDecimal(x,base)
        m_int= anyBaseToDecimal(m,base)
    
    if(x_int > 0):
        if (x_int < m_int):
            answer = x_int
        elif(x_int == m_int):
            answer = 0
        elif(x_int > m_int):
            answer = x_int - m_int * (x_int // m_int)
    if(x_int < 0):
        while(x_int < m_int):
            x_int = x_int +m_int
        answer = x_int

    answer = str(decimalToAnyBase(answer,base))

    return answer

def modularMultiplication(x,y,m,base):
    z = multiplication_karatsuba(x , y, base)
    answer = modularReduction(z,m,base)
    return answer



def modularInverse(a,m):
    gcd, x, y = extended_euclidean_algorithm(a,m)

    if gcd != 1:
        return 'Inverse does not exist'
    else:
        return modularReduction(x,m) # x%m

       
       













