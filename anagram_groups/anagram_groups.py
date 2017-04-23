#### I figured that sorting of strings may be considered a higher level function of the language (although it's available in almost every language's standard libraries)
#### this can be replaced by python's internal "sorted" in the definition of "anagram_id" further below, simply by changing sort_f = mergesort for sort_f = sorted
#### >>> begin Mergesort and aux
def merge(leftHalf, rightHalf):
    merged = []
    i = j = 0

    while i < len(leftHalf) or j < len(rightHalf):
        if i >= len(leftHalf): # exhausted the left half
            merged.append(rightHalf[j])
            j += 1
        elif j >= len(rightHalf): #exhausted the right half
            merged.append(leftHalf[i])
            i += 1
        elif rightHalf[j] < leftHalf[i]:
            merged.append(rightHalf[j])
            j += 1
        else:
            merged.append(leftHalf[i])
            i += 1

    return merged

def mergesort(list_):
    if len(list_) < 2:
        return list_
    elif len(list_) == 2: #  faster while still keeping the code reasonably small
        if list_[0]<=list_[1] : return list_
        else: return [list_[1], list_[0]]

    midpoint = len(list_) // 2
    return merge(mergesort(list_[:midpoint]), mergesort(list_[midpoint:]))

##### <<< end Mergesort and aux

#### anagram_id is the hash function. So long as each word maps to the same thing to its anagrams, it will be correct. I opted for sorting since it's simple and fast (words are typically small).
####   there are possible alternatives, like sparse matrices or storing the product of the prime factorisation and mapping each character to a prime number. I also implemented the latter one.
#def anagram_id_sorting( word, sort_f = sorted ): # using Python's built-in Timsort
def anagram_id_sorting( word, sort_f = mergesort): 
    return ''.join( sort_f( list ( word ) ) )

charToPrime = {} # nitpick: could use smaller primes for the most frequent letters to improve efficiency, but it's unlikely to make any difference with typical word sizes
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]
for i in xrange(26):
    charToPrime[chr(ord('a')+i)] = primes[i]
charToPrime['-'] = primes[26]   # dictionary words are assumed to be composed by (lower-case) letters and the hyphen. I converted to lower-case ...
    #... in the method that builds up the hash table to guarantee this, and I also added the hyphen to this mapping.

# alternative based on prime factors
def anagram_id_primes( word ):   # rename to anagram_id to test this instead
    # this list comprehension works on valid data (no invalid characters)
    mapped_primes = [charToPrime[x] for x in word]

    #mapped_primes = []
    #for x in word:
    #    if x in charToPrime:
    #        mapped_primes.append(charToPrime[x])
    ## invalid characters are simply ignored for grouping purposes    

    return reduce(lambda x, y: x * y, mapped_primes)


class Anagram_Grouper:
    def __init__( self, anagram_hashing_function = anagram_id_sorting ):
        self.word_dic = {} # indexed by anagram id
        self.anagram_id = anagram_hashing_function
    

    def build_from_iterable(self, wordlist):
        for word in wordlist:
            word = word.strip().lower()  # sanitize the data - allows for the iterable to be readlines/file
            anagram_id_ = self.anagram_id(word)
            
            if anagram_id_ in self.word_dic:
                self.word_dic[anagram_id_].append( word )
            else:
                self.word_dic[anagram_id_] = [ word ]

        
    def display(self, minSize = 2): # groups of 1 are uninteresting
        "auxiliary method for displaying anagram groups already stored. Optional parameter: minSize (filters by the minimum amount of words in the group)"
        for k in sorted( self.word_dic.keys() ):
            if len( self.word_dic[k] ) >= minSize:
                #print k, sorted(self.word_dic[k])
                print sorted( self.word_dic[k] )
        
if __name__ == "__main__":
    a = Anagram_Grouper()
    f = open("corncob_lowercase.txt", "rb")
    a.build_from_iterable(f)
    f.close()
    a.display()
    
    print "-----"
    b = Anagram_Grouper()
    b.build_from_iterable(['opts', 'post', 'pots', 'spot', 'stop', 'tops'] + ['sorting', 'storing'] + ['outer', 'route'] + ['resort', 'roster', 'sorter'] + ['singleThing'] + ['peru', 'pure'])
    b.build_from_iterable(['lustre', 'result', 'rustle', 'ulster'])
    b.build_from_iterable(['feints', 'finest', 'infest'])
    b.display(minSize =  0)
    