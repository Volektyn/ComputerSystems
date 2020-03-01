def Booth_alg(multiplicand, multiplier, multiplicand_length, multiplier_length):
    if multiplicand < 0:
        multiplicand = TwoComp(("{0:0%db}" % multiplicand_length).format(multiplicand))
    else:
        multiplicand = ("{0:0%db}" % multiplicand_length).format(multiplicand)

    if multiplier < 0:
        multiplier = TwoComp(("{0:0%db}" % multiplier_length).format(multiplier))
    else:
        multiplier = ("{0:0%db}" % multiplier_length).format(multiplier)
    
    print(multiplicand, multiplicand_length)
    print(multiplier, multiplicand_length)

    #ilen = multiplicand_length + multiplier_length + 1                  #The common length of internal variables
    a = multiplicand + GenZeroStr(multiplier_length + 1)            #A: place M in leftmost position. Fill the left bits with 0.
    s = TwoComp(multiplicand) + GenZeroStr(multiplier_length + 1)   #S: place negative M in leftmost position.
    p = GenZeroStr(multiplicand_length) + multiplier + "0"          #P: place R by rightmost 0.

    print("Internal variables:")
    print(f"M = {multiplicand}")
    print(f"R = {multiplier}")
    print(f"A = {a}")
    print(f"S = {s}")
    print(f"P = {p}")

    for i in range(multiplier_length):   
        print("Step %d:" % (i+1))

        op = p[-2:]
        print("    " + "The last 2 bits of p are: %s" % "".join(op))
        if   op == "10":
            print("    " + "P = (P+S) >> 1")
            p = BitAdd(p, s, len(p))
        elif op == "01":
            print("    " + "P = (P+A) >> 1")
            p = BitAdd(p, a, len(p))
        elif op == "00":
            print("    " + "P = P >> 1")
        elif op == "11":
            print("    " + "P = P >> 1")

        p = BitShift(p, 1)
        print("    " + "P = %s\n" % p)

    p = p[:-1]
    return p

def BitShift(n, shift):
    """Shift the bits rightward in arithmetical method.
    If shift is negative, it shifts the bits leftward."""

    if shift > 0:       #Right shift
        if n[0] == "0":
            n_ = "".join(["0"] * shift) + n
        else:
            n_ = "".join(["1"] * shift) + n
        return n_[:len(n)]
    else:
        n_ = n + "".join(["0"] * (-shift))
        return n_[-len(n):]


def BitAdd(m, n, length):
    """
        Return m+n in string.
        length -- The length of returned number (overflowed bit will be ignored)
    """

    lmax = max(len(m), len(n))
    c = 0
    ml = [0] * (lmax - len(m)) + [int(x) for x in list(m)]
    nl = [0] * (lmax - len(n)) + [int(x) for x in list(n)]
    rl = []
    for i in range(1, lmax+1):
        if ml[-i] + nl[-i] + c == 0:
            rl.insert(0, 0)
            c = 0
        elif ml[-i] + nl[-i] + c == 1:
            rl.insert(0, 1)
            c = 0
        elif ml[-i] + nl[-i] + c == 2:
            rl.insert(0, 0)
            c = 1
        elif ml[-i] + nl[-i] + c == 3:
            rl.insert(0, 1)
            c = 1
    if c == 1:
        rl.insert(0, 1)
    if length > len(rl):
        rl = [0] * (length - len(rl)) + rl
    else:
        rl = rl[-length:]
    rl = "".join([str(x) for x in rl])
    return rl


def TwoComp(n):
    """Return the two's complement of given number."""

    l = list(n)
    l = ["0" if l[i] == "1" else "1" for i in range(len(l))]
    return BitAdd("".join(l), "1", len(l))

def GenZeroStr(n):
    """Generate a bunch of zeroes."""

    return "".join(["0"] * n)

def BitSubtraction(m, n):
    """Return m - n"""

    diff = len(m) - len(n)

    if (diff > 0):
        n = "0" * diff + n
    elif (diff < 0):
        m = "0" * (-diff) + m
    
    print(f"\tSubstraction {m} - {n}\n")
    
    sign = 0
    subtr = "0" * len(m)
    carry = 0

    for i in reversed(range(len(m))):
        d = int(m[i]) - int(n[i])

        subtr = list(subtr)
        if d <= 0:
            if (carry == 0 and d != 0):
                carry = 1
                subtr[i] = "1"
            elif (carry == 1):
                subtr[i] = "0"
            else:
                subtr[i] = "0"
        else:
            if (carry == 1):
                carry = 0
                subtr[i] = "0"
            else:
                subtr[i] = "1"

    if (carry == 1):
        sign = 1

    return "".join(subtr), sign


#   Dividend / Divisor = Quotient and Remainder
def Division_with_shift_remainder(dividend, divisor):
    print(f"Division: {dividend} / {divisor}")
    quotient = ""
    remainder = "0" * 16
    half_register_length = int(len(remainder) / 2)
    temp_remainder = ""

    remainder = BitAdd(remainder, dividend, len(remainder))
    print(f"Initial value of remainder:{remainder}")

    for _ in range(half_register_length):
        remainder = remainder[1:]
        remainder += "0"
        temp_remainder = remainder[:]
        print(f"Remainder: {remainder}") # , half of register size {remainder[:half_register_length]}")

        substraction_res, sign = BitSubtraction(remainder[:half_register_length], divisor)

        remainder = substraction_res + remainder[half_register_length:]

        if (sign == 1):
            remainder = temp_remainder[:]
            quotient += "0"
        else:
            quotient += "1"
        
        print(f"Quotient: {quotient}")
    
    return quotient, remainder[:half_register_length]

    


if __name__ == "__main__":
    # multiplicand = int(input("Enter multiplicand: "))
    # multiplier = int(input("Enter multiplier: "))
    # multiplicand_length = int(input("Enter length of multiplicand: "))
    # multiplier_length = int(input("Enter multipliplier: "))
    #print(f"The answer is: {Booth_alg(multiplicand, multiplier, multiplicand_length, multiplier_length)}") #3, -4, 4, 4
    divident = input("Enter divident: ")
    divisor = input("Enter divisor: ")
    quotient, remainder = Division_with_shift_remainder(divident, divisor) # (dividend = '01001000',divisor = '1000')
    print(f"\nAnswer:\n\tquotient:{quotient},\n\tremainder:{remainder}")

