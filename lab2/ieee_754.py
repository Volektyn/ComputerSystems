def set_sign(x1, x2):
    return int(x1[0]) ^ int(x2[0])

def BitAddition(a, b):
        diff = len(a)-len(b)
        print (f"\n Addition {a} + {b}")

        a = [int(a[i]) for i in range(0, len(a))]
        b = [int(b[i]) for i in range(0, len(b))]
        
        if (diff > 0):
            b = [0,] * diff + b   
        elif (diff < 0):
            a = [0,] * (-diff) + a 

        carry = 0
        sum = [0] * len(a)

        for i in reversed(range(len(a))):
            d = (a[i] + b[i] + carry) // 2
            sum[i] = (a[i] + b[i] + carry) - 2*d
            carry = d
        
        if (carry == 1):
            sum = [carry] + sum

        sum = [str(sum[i]) for i in range(0, len(sum))]
        sum = "".join(sum)
        print(f" Sum: {sum}\n")

        return sum

def BitSubtraction(a, b):
    diff = len(a) - len(b)

    print(f"\n Subtraction {a} - {b}")
    a = [int(a[i]) for i in range(0, len(a))]
    b = [int(b[i]) for i in range(0, len(b))]

    if (diff > 0):
        b = [0,] * diff + b   
    elif (diff < 0):
        a = [0,] * (-diff) + a 

    sign = 0
    subtr = [0,] * len(a)
    carry = 0
    for i in reversed(range(len(a))):
        d = a[i] - b[i]
        if d <= 0:
            if (carry == 0 and d != 0):
                carry = 1
                subtr[i] = 1
            elif (carry == 1 and d == 0):
                subtr[i] = 1
            elif (carry == 1 and d != 0):
                subtr[i] = 0
            else:
                subtr[i] = 0
        else:
            if (carry == 1):
                carry = 0
                subtr[i] = 0
            else:
                subtr[i] = 1

    if (carry == 1):
        sign = 1         

    subtr = [str(subtr[i]) for i in range(0, len(subtr))]
    subtr = "".join(subtr)
    print(f" Subtraction result: {subtr}\n")

    return subtr, sign


def multiply_significands(multiplicand, multiplier):
        register = '0' * 48
        half_register_length = int(len(register) / 2)
        multiplicand = '0' * (half_register_length - len(multiplicand)) + multiplicand
        multiplier = '0' * (half_register_length - len(multiplier)) + multiplier

        register = BitAddition(register, multiplier)

        iteration = 0

        while (iteration <= len(multiplicand)):
            currentBit = int(register[-1])
            register = "0" + register[:-1]

            if (currentBit == 1):
                register = BitAddition(register[:half_register_length], multiplicand) + register[half_register_length:]

            iteration += 1

        return register

def set_exponent(ini_exponent):
    exponent = ''
    if len(ini_exponent) < 8:
        exponent = '0' * (8 - len(ini_exponent)) + ini_exponent
    elif len(ini_exponent) > 8:
        seperator = ini_exponent.index('1')
        ini_exponent = ini_exponent[seperator:]
        if len(ini_exponent) > 8:
            exponent = '1' * 8
        exponent = ini_exponent
    else:
        exponent = ini_exponent
    
    return exponent


def set_mantissa(ini_mantissa):
    mantissa = ''
    if len(ini_mantissa) < 23:
        mantissa = ini_mantissa + '0' * (23 - len(ini_mantissa))
    elif len(ini_mantissa) > 23:
        seperator = ini_mantissa.index('1')
        ini_mantissa = ini_mantissa[seperator:]
        while(len(ini_mantissa) > 23):
            ini_mantissa = ini_mantissa[:-1]
        mantissa = ini_mantissa
    else:
        mantissa = ini_mantissa
    
    return mantissa


if __name__ == '__main__':
    X1 = '01000010111110100100000000000000'
    X2 = '01000001010000010000000000000000' 
    
    print(f"Begin multiplaction:\nX1 = {X1}\nX2 = {X2}")
    sign = set_sign(X1, X2)
    print(f"1) Sign: {sign}\n")

    print("2) Begin multiply significands")
    mult_mantissas = multiply_significands('1' + X1[9:], '1' + X2[9:])
    print(f"\n    Multiply significands res: {mult_mantissas}     \n")

    # mult_mantissas = mult_mantissas[1:] + '0'

    mantissa = set_mantissa(mult_mantissas)
    mantissa = mantissa[1:] + '0'

    bias = BitSubtraction('01111111', '00000001')[0]
    print("3) The exponents of the Multiplier (E1) and the multiplicand (E2) bits are added and the base value is subtracted from the added result.",
                  "\nThe subtracted result is put in the exponential field of the result block.")
    print("Bias: " + bias)

    temp_exponent = BitAddition(X1[1:9], X2[1:9])
    # print(f"X1_exp: {X1[1:9]}, X2_exp: {X2[1:9]}")
    temp_exponent = BitSubtraction(temp_exponent, bias) [0]

    exponent = set_exponent(temp_exponent)

    print(f"Exponent: {exponent}\n")

    print(f"X1: {X1}, X2: {X2}\nResult of X1*X2: {sign}|{exponent}|{mantissa}")

    #print("Correct answer 0|10001001|01111001010101001000000")
    
# 263 - 126 = 9


