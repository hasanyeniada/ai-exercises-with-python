import random

#P(+D)
def P_DPlus(iterationCount):

    total_plus_D = 0

    for i in range(0, iterationCount):

        resA = getBooleanResultOfA()
        resB = getBooleanResultOfB(resA)
        resC = getBooleanResultOfC(resA)
        resD = getBooleanResultOfD(resB, resC)

        if (resD):
            total_plus_D += 1

    probability_D_plus = total_plus_D / iterationCount

    return probability_D_plus

#P(+D,-A)
def P_plusD_and_minusA(iterationCount):

    total_plusD_and_minusA = 0

    for i in range(0, iterationCount):

        resA = getBooleanResultOfA()
        resB = getBooleanResultOfB(resA)
        resC = getBooleanResultOfC(resA)
        resD = getBooleanResultOfD(resB, resC)

        if (resD) and (not resA):
            total_plusD_and_minusA += 1

    probability_plusD_and_minusA = total_plusD_and_minusA / iterationCount

    return probability_plusD_and_minusA

#P(+E|-B)
def P_plusE_given_minusB(iterationCount):

    #P(+E|-B) = P(+E|-B) / (P(+E,-B) + P(-E,-B)

    total_plusE_and_minusB = 0
    total_minusE_and_minusB = 0

    for i in range(0, iterationCount):

        resA = getBooleanResultOfA()
        resB = getBooleanResultOfB(resA)
        resC = getBooleanResultOfC(resA)
        resE = getBooleanResultOfE(resC)

        if (resE) and (not resB):
            total_plusE_and_minusB += 1

        if (not resE) and (not resB):
            total_minusE_and_minusB += 1

    total_minusE_and_minusB = total_minusE_and_minusB / iterationCount
    total_plusE_and_minusB = total_plusE_and_minusB / iterationCount

    probability_plusE_given_minusB = total_plusE_and_minusB / (total_plusE_and_minusB + total_minusE_and_minusB)

    return probability_plusE_given_minusB

#P(+A|+D,-E)
def P_plusA_given_plusD_and_minusE(iterationCount):

    #P(+A|+D,-E) = P(+A,+D,-E) / P(+A,+D,-E) + P(-A,+D,-E)

    total_plusA_and_plusD_and_minusE = 0
    total_minusA_and_plusD_and_minusE = 0

    for i in range(0, iterationCount):

        resA = getBooleanResultOfA()
        resB = getBooleanResultOfB(resA)
        resC = getBooleanResultOfC(resA)
        resD = getBooleanResultOfD(resB, resC)
        resE = getBooleanResultOfE(resC)

        if (resA) and (resD) and (not resE):
            total_plusA_and_plusD_and_minusE += 1

        if (not resA) and (resD) and (not resE):
            total_minusA_and_plusD_and_minusE += 1

    total_plusA_and_plusD_and_minusE = total_plusA_and_plusD_and_minusE / iterationCount
    total_minusA_and_plusD_and_minusE = total_minusA_and_plusD_and_minusE / iterationCount

    probability_plusA_given_plusD_and_minusE = total_plusA_and_plusD_and_minusE / (total_plusA_and_plusD_and_minusE + total_minusA_and_plusD_and_minusE)

    return probability_plusA_given_plusD_and_minusE

#P(+B,-E|+A)
def P_plusB_and_minusE_given_plusA(iterationCount):

    #P(+B,-E|+A) = P(+B,-E,+A) / P(+A)
    #P(+A) = P(+B,+E,+A) + P(+B,-E,+A) + P(-B,+E,+A) + P(-B,-E,+A)

    total_plusB_and_plusE_and_plusA = 0    #+B,+E
    total_plusB_and_minusE_and_plusA = 0   #+B,-E
    total_minusB_and_plusE_and_plusA = 0   #-B,+E
    total_minusB_and_minusE_and_plusA = 0  #-B,-E

    for i in range(0, iterationCount):

        resA = getBooleanResultOfA()
        resB = getBooleanResultOfB(resA)
        resC = getBooleanResultOfC(resA)
        resE = getBooleanResultOfE(resC)

        if (resB) and (resE) and (resA):      #P(+B,+E,+A)
            total_plusB_and_plusE_and_plusA += 1

        if (resB) and (not resE) and (resA):  #P(+B,-E,+A)
            total_plusB_and_minusE_and_plusA += 1

        if (not resB) and (resE) and (resA):      #P(-B,+E,+A)
            total_minusB_and_plusE_and_plusA += 1

        if (not resB) and (not resE) and (resA):  #P(-B,-E,+A)
            total_minusB_and_minusE_and_plusA += 1

    total_plusB_and_minusE_and_plusA = total_plusB_and_minusE_and_plusA / iterationCount
    total_minusB_and_minusE_and_plusA = total_minusB_and_minusE_and_plusA / iterationCount
    total_minusB_and_plusE_and_plusA = total_minusB_and_plusE_and_plusA / iterationCount
    total_plusB_and_plusE_and_plusA = total_plusB_and_plusE_and_plusA / iterationCount

    #P(+A)
    p_plusA = total_plusB_and_plusE_and_plusA + total_plusB_and_minusE_and_plusA + total_minusB_and_plusE_and_plusA + total_minusB_and_minusE_and_plusA

    #P(+B,-E|+A) = P(+B,-E,+A) / P(+A)
    probability_plusB_and_minusE_given_plusA =  total_plusB_and_minusE_and_plusA / p_plusA

    return probability_plusB_and_minusE_given_plusA

#Gives Boolean  Result of A, according to taken random integer between (1,100).
def getBooleanResultOfA():
    random_A = get_random_number(1, 100)
    result_A = False

    if (random_A < 20):
        result_A = True

    return result_A

#Gives Boolean  Result of B, according to taken random integer between (1,100) and Result of A.
def getBooleanResultOfB(result_A):
    random_B = get_random_number(1, 100)
    result_B = False

    if (random_B < 80) and (result_A):
        result_B = True
    if (random_B < 20) and (not result_A):
        result_B = True

    return result_B

#Gives Boolean  Result of C, according to taken random integer between (1,100) and Result of A.
def getBooleanResultOfC(result_A):
    random_C = get_random_number(1, 100)
    result_C = False

    if (random_C < 20) and (result_A):
        result_C = True
    if (random_C < 5) and (not result_A):
        result_C = True

    return result_C

#Gives Boolean  Result of D, according to taken random integer between (1,100) and Result of B and C.
def getBooleanResultOfD(result_B, result_C):
    random_D = get_random_number(1, 100)
    result_D = False

    if (random_D < 5) and (not result_B) and (not result_C):
        result_D = True
    if (random_D < 80) and (not result_B) and (result_C):
        result_D = True
    if (random_D < 80) and (result_B) and (not result_C):
        result_D = True
    if (random_D < 80) and (result_B) and (result_C):
        result_D = True

    return result_D

#Gives Boolean  Result of E, according to taken random integer between (1,100) and Result of C.
def getBooleanResultOfE(result_C):
    random_E = get_random_number(1, 100)
    result_E = False

    if (random_E < 60) and (not result_C):
        result_E = True
    if (random_E < 80) and (result_C):
        result_E = True

    return result_E

#Gives random integer between (1,100)
def get_random_number(min, max):
    randA = random.randint(min, max)
    return randA

#MAIN
if __name__ == "__main__":

    print("Monte Carlo Technique is starting...")

    # P(+D)
    prob_D_plus = P_DPlus(100000)
    print("Probability of P(+D) = ", prob_D_plus)

    # P(+D,-A)
    prob_plusD_and_minusA = P_plusD_and_minusA(100000)
    print("Probability of P(+D,-A) = ", prob_plusD_and_minusA)

    # P(+E|-B)
    prob_plusE_given_minusB = P_plusE_given_minusB(100000)
    print("Probability of P(+E|-B) = ", prob_plusE_given_minusB)

    # P(+A|+D,-E)
    prob_plusA_given_plusD_and_minusE = P_plusA_given_plusD_and_minusE(100000)
    print("Probability of P(+A|+D,-E) = ", prob_plusA_given_plusD_and_minusE)

    # P(+B,-E|+A)
    prob_plusB_and_minusE_given_plusA = P_plusB_and_minusE_given_plusA(100000)
    print("Probability of P(+B,-E|+A) = ", prob_plusB_and_minusE_given_plusA)