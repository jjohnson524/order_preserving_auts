def Ball(F,k):
    N = F.rank()
    B_ind = [] #describing the ball first in terms of indices of the generators
    gens = [i for i in range(-N,N+1) if i != 0] #negative index corresponds to the inverse of a generator
    B_ind.append([(g,) for g in gens])

    for i in range(2,k+1):
        words = []
        for w in B_ind[-1]:
            for g in gens:
                if w[-1] != -g:
                    words.append(w+(g,))
        B_ind.append(words)


    B=[F.one()] #turning indices into free group elements

    for l in range(0,k):
        for s in B_ind[l]:
            w=F.one()
            for letter in s:
                if letter>0:
                    w=w*F.gens()[letter-1]
                else:
                    w=w*F.gens()[-letter-1].inverse()
            B.append(w)
    len(B)
    return B

def PairsinBall(B):
    D=[]
    while len(B)>1:
        D.append((B[-1],B[-1].inverse()))
        B.remove(B[-1].inverse())
        B.remove(B[-1])

    return D
