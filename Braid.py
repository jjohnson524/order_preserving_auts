import sys
from sage.all import *
import word_length

def FreeGroup1(N):
    gens=[]
    for i in range(1,N+1):
        gens.append('x'+str(i))
    #gensstring=','.join(gens)
    F=Groups().free(names=gens)
    return F

class Braid:
    def __init__(self, gens):
        self.gens=gens
        N=1
        for i in range(len(gens)):
            if abs(gens[i])+1>N:
                N=abs(gens[i])+1
        self.strands=N

    def get_group_gens(self):
        F = FreeGroup1(self.strands)
        G=[]
        for i in range(1,self.strands+1):
            G.append(F([i]))
        return G

    def mirror(self):
        mir_gens=[]
        for i in range(len(self.gens)):
            mir_gens.append(-self.gens[i])
        return Braid(mir_gens)

    def inverse(self):
        inv_gens=[]
        for i in range(len(self.gens)):
            inv_gens.append(-self.gens[len(self.gens)-i-1])
        return Braid(inv_gens)

    def action(self, optimize = False):
        F = FreeGroup1(self.strands)
        finalHom=F.hom([g for g in F.gens()]) #initializing to identity hom on F
        i=len(self.gens)
        while i>0:
            element=self.gens[i-1]
            genImage=[]
            if element>0:
                for j in range(1,self.strands+1):
                    if j==element:
                        genImage.append(F([j+1]))
                    elif j==element+1:
                        genImage.append(F([-j,j-1,j]))
                    else:
                        genImage.append(F([j]))
                currentHom=F.hom(genImage)
                finalHom=currentHom*finalHom 
            else: #for inverses of artin generators
                for j in range(1,self.strands+1):
                    if j==-element+1:
                        genImage.append(F([j-1]))
                    elif j==-element:
                        genImage.append(F([j,j+1,-j]))
                    else:
                        genImage.append(F([j]))
                currentHom=F.hom(genImage)
                finalHom=currentHom*finalHom
            i-=1
            if optimize:
                finalHom = optimal_conj_suggest(finalHom, self.strands)
        return finalHom    

    def inverse_action(self, optimize = False):
        inv_braid=self.inverse()
        return inv_braid.action(optimize)

    def permutation(self):
        SymG=SymmetricGroup(self.strands)
        finalPerm=SymG("()")
        for i in range(len(self.gens)):
            element=abs(self.gens[i])
            currentPerm=SymG("(" + str(element) + "," + str(element+1) +")")
            finalPerm=currentPerm*finalPerm 
        return finalPerm    

def longest_word_function(H,N):
    longest_word=[]
    longest_length=0
    F = FreeGroup1(N)
    Free_gens=F.gens()
    for i in range(N):#idenitfies the longest word
        current_word=H(Free_gens[i])
        current_length=word_length.word_length(current_word)
        if current_length>longest_length:
            longest_word=current_word
            longest_length=current_length
    return longest_word

def single_conj_suggest(H,N):
    sign=1
    F = FreeGroup1(N)
    Free_gens=F.gens()
    long_word=longest_word_function(H,N)
    conj_Tietze=long_word.Tietze()[0] #returns signed index of generator of first word element in longest word
    if conj_Tietze<0:
        sign=-1
    conj_elem=Free_gens[abs(conj_Tietze)-1]**-sign
    gen_image=[]
    for i in range (N):
        gen_image.append(conj_elem*H(Free_gens[i])*conj_elem**-1)
    return F.hom(gen_image)


def optimal_conj_suggest(H,N):
    sug_hom=H
    done=False
    F = FreeGroup1(N)
    longest_word=longest_word_function(H,N)
    longest_length=word_length.word_length(longest_word)
    while done==False:
        new_hom=single_conj_suggest(sug_hom,N)
        if word_length.word_length(longest_word_function(new_hom,N))< word_length.word_length(longest_word_function(sug_hom,N)):
            sug_hom=new_hom
        else: done=True
    return sug_hom

def get_actions(gens,optimize = False):
    print('Input Braid: '+str(gens))
    braid=Braid(gens)
    if optimize:
        lead = 'Optimized '
    else:
        lead = ''
    f=braid.action(optimize)
    f_inv=braid.inverse_action(optimize)
    G=braid.get_group_gens()
    action_out = lead + 'Braid Action: ['
    for i in range(braid.strands):
        action_out = action_out + 'beta(' + str(G[i]) + ')=' + str(f(G[i]))
        if i < braid.strands-1:
            action_out = action_out + ', '
    action_out = action_out + ']'
    print(action_out)

    action_out = lead + 'Braid Inverse: ['
    for i in range(braid.strands):
        action_out = action_out + 'beta^-1(' + str(G[i]) + ')=' + str(f_inv(G[i]))
        if i < braid.strands-1:
            action_out = action_out + ', '
    action_out = action_out + ']'
    print(action_out)
