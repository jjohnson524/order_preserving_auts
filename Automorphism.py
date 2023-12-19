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

def makeword(group, wordlist):
    word = group.one()
    for syl in wordlist:
        word = word * group([syl[0]])**syl[1]
    return word

def makehom(imagelist):
    F = FreeGroup1(len(imagelist))
    images = []
    for i in range(F.rank()):
        images.append(makeword(F,imagelist[i]))
    return F.hom(images)

class Automorphism:
    def __init__(self, aut, aut_inverse,rank):
        self.aut=aut
        self.aut_inverse=aut_inverse
        self.rank = rank

    def get_group_gens(self):
        F = FreeGroup1(self.rank)
        G=[]
        for i in range(1,self.rank+1):
            G.append(F([i]))
        return G

    def action(self):
        return self.aut    

    def inverse_action(self):
        return self.aut_inverse

    def abelian_matrix(self):
        F = FreeGroup1(self.rank)
        outmatrix = []  
        for i in range(self.rank):
            newrow = []
            countgen = F([i+1])
            for j in range(self.rank):
                ingen = F([j+1])
                newrow.append(word_length.exponent_gen_sum(self.aut(ingen),countgen))
            outmatrix.append(newrow)
        return matrix(outmatrix)

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
