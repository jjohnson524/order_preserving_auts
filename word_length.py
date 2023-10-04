def word_length(w):
    S=w.syllables()
    l=0

    for tuple in S:
        l=l+abs(tuple[1])

    return l

def exponent_sum(w):
    S=w.syllables()
    l=0

    for tuple in S:
        l=l+tuple[1]

    return l

def exponent_gen_sum(w,gen):
    S=w.syllables()
    l=0

    for tuple in S:
        if tuple[0]==gen:
            l=l+tuple[1]

    return l
