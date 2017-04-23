def rotate_left( V, i ):
    n = len(V)
    assert n > 1 # rotation makes no sense for empty vectors or vectors of size 1
    assert i >= 0
    if i == 0: return V

    i %= n # if i>n, i = i % n

    for it in xrange( i//2 ):
        V[it], V[i-it-1] = V[i-it-1], V[it] # swap up to i
    for it in xrange ( i, i + ((n-i)//2) ):
        V[it], V[n-it+i-1] = V[n-it+i-1], V[it] # swap from i to n

    for it in xrange ( n//2 ):
        V[it], V[n-it-1] = V[n-it-1], V[it] # swap to reverse the whole V
    return V

if __name__ == "__main__": # a few random tests
    from random import shuffle
    for n in xrange(2, 10):
        for i in xrange(12):
            print "size:", n, "rotation:", i
            Vector = range(n)
            shuffle(Vector)
            print Vector, "original"
            rotate_left (Vector, i)
            print Vector, "rotated"
