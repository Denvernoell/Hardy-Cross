from itertools import combinations
from math import pi


def diameter(diameter): return diameter*(1/12)
def area(diameter): return (pi*diameter**2*.25)
def K(length, diameter, area): return (
    (0.02*length)/((diameter)*(area**2)*2*32.2))


def hl(K, Q): return K*Q**2
def hl__Q(hl, Q): return hl/Q
def nhl__Q(hl__Q): return hl__Q*2
def correctedH1(hl, direction): return hl*direction


def start(loop):
    areas = []
    Ks = []
    for i in range(len(loop['diameters'])):
        loop['diameters'][i] = diameter(loop['diameters'][i])
        areas.append(area(loop['diameters'][i]))
        loop['areas'] = areas

        Ks.append(
            K(loop['lengths'][i], loop['diameters'][i], loop['areas'][i]))
        loop['K'] = Ks

    return(loop)


def middle(loop):
    hls = []
    hl__Qs = []
    nhl__Qs = []

    for i in range(len(loop['diameters'])):
        hls.append(hl(loop['K'][i], loop['flows'][i]))
        loop['headloss'] = hls

        hl__Qs.append(hl__Q(loop['headloss'][i], loop['flows'][i]))
        loop['hl__Qs'] = hl__Qs

        nhl__Qs.append(nhl__Q(loop['hl__Qs'][i]))
        loop['nhl__Qs'] = nhl__Qs
        # correctedHl.append(hl[i]*direction[i])
    return(loop)


def correction(loop):
    sum_headloss = 0
    sum_nhl__Q = 0
    delta_q = 0
    for i in range(len(loop['pipes'])):
        sum_headloss += loop['headloss'][i]*loop['directions'][i]
        sum_nhl__Q += loop['nhl__Qs'][i]
    delta_q = sum_headloss/sum_nhl__Q
    loop['sum_headloss'] = sum_headloss
    loop['sum_nhl__Qs'] = sum_nhl__Q
    loop['delta_q'] = -delta_q
    return(loop)


def qchange(loops):
    matches = findMatches(loops)
    newflows = []
    for loop in loops:
        for i in range(len(loop['flows'])):
            newflows.append(loop['flows'][i] +
                            (loop['delta_q']*loop['directions'][i]))
        loop['newflows'] = newflows
        # loop['flows'][i] += loop['delta_q']*loop['directions'][i]
    return(loops)


def findMatches(loops):
    myList = []
    for x, y in combinations(loops, 2):
        myList.append(set(x['pipes']) & set(y['pipes']))
    return(myList)
    # myList.append(set(loop))
# def changeMatches(loops):
#                 for match in matches:
#                 if loop['pipes'][i] in match:
#                     print(loop['flows'][i])
#                     loop['flows'][i] += loop['delta_q']*loop['directions'][i]
#                     print('Match')
#             print(i)


loop1 = {
    'pipes': [1, 4, 6, 3],
    'lengths': [5000, 4000, 5000, 4000],
    'diameters': [24, 18, 18, 18],
    'flows': [6.2, 4.0, 3.8, 3.8],
    'directions': [-1, -1, 1, 1]}
loop2 = {
    'pipes': [2, 5, 7, 4],
    'lengths': [5000, 4000, 5000, 4000],
    'diameters': [12, 18, 18, 18],
    'flows': [2.2, 0.2, 3.8, 4.0],
    'directions': [-1, -1, 1, 1]}
loops = [loop1, loop2]


def fullLoop(loops):
    for loop in loops:
        start(loop)
        middle(loop)
        correction(loop)
        # print(loop['flows'])
        # print(loop['directions'])
    qchange(loops)

    for num in range(8):
        # matches = findMatches(loops)
        # matchingPipe = []
        # if str(num) in matches:
        #     print('Match')
        for loop in loops:
            i = 0
            for pipe in loop['pipes']:
                if num == pipe:
                    print(f"{pipe} = {loop['newflows'][i]}")
                # print(i)
                i += 1

        # print(loop['flows'])

        # for key, value in loop.items():
        #     print(f"{key} = {value}")
        # print('\n')

    # print(findMatches(loops))
fullLoop(loops)
