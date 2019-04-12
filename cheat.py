import sys


class Letter:
    letter= '0'
    neighbours = []

    def __init__(self, letter):
        self.letter = letter
        self.neighbours = []

    def isNeighbour(self, letter):
        for n in self.neighbours:
            if n.letter == letter:
                return n
        return False

    def __str__(self):
        s = ""
        for n in self.neighbours:
            s += n.letter + str(n)
            if n.letter == '.':
                s += "\n"
        return s


    def isIn(self, word):
        pt = self
        for l in word+".":
            t =  pt.isNeighbour(l)
            if t:
                pt = t
            else:
                return False

        return True

if len(sys.argv) != 2:
    print("Bad usage:\npython dico.py [word length]")
    exit(0)

wordLength = int(sys.argv[1])

if wordLength <= 0:
    print("Bad usage:\npython dico.py [word length]")
    exit(0)


"""
Dictionary tree:
    the root is '0'
    each word inserted has a child '.'
"""
dico = Letter('0')


"""
Open dico.txt to feed the dictionary tree
"""
file = open("dico.txt","r")
for line in file:
    w = line.replace("\n","")

    pt = dico
    for l in w:
        t = pt.isNeighbour(l)
        if not t:
            pt.neighbours.append(Letter(l))

        pt = pt.isNeighbour(l)

    pt.neighbours.append(Letter('.'))


# Game grid input
arr = [['a','b','c','d'],['e','f','g','h'],['i','j','k','l'],['m','n','o','p']]
arr = [['v','e','s','e'],['g','o','v','i'],['l','b','e','h'],['a','g','b','e']]
arr = [['0','0','0','e'],['0','0','v','i'],['0','0','e','h'],['0','0','b','e']]


let_lst = Letter('.') # list of the letters in the grid
for row in arr:
    for l in row:
        let_lst.neighbours.append(Letter(l))


# Make the links between the letters:
L = 4
H = 4
for h in range(H):
    for l in range(L):
        for of_y in range(-1,2):
            for of_x in range(-1,2):
                if of_x == 0 and of_y == 0:
                    continue
                x = l+of_x
                y = h+of_y
                if x >= 0 and x < L and y >= 0 and y < H:
                    let_lst.neighbours[h*H+l].neighbours.append(let_lst.neighbours[y*H+x])

"""
Recursive function to explore every possible word in the grid
Input:
    - l: the length of the word we are looking for
    - word: a string containing the current word in the recursive search
    - letters: a list of Letter object from the grid, the last one is the one to visit
    - dic is the Letter obj from the dictionary corresponding to the last letter of the word searched
"""
def look(l, word, letters, dic):
    let = letters[-1]
    word += let.letter
    let.letter = '0' # visited letter
    # letters: the visited already appended
    # dic already pointing on the visited letter

    if len(word) == l:
        if dic.isNeighbour('.'): # the generated word exists, one word of the desired length found
            print("found:", word)
    else:
        for n in let.neighbours:
            #print(n)
            #print("ii",n,n.letter)
            #print(dic.letter,"<<")
            if dic.isNeighbour(n.letter):
                #print("<<<"+word+">>>")
                letters.append(n)
                #print("WTF: ")
                #print(dic.isNeighbour(n.letter))
                look(l, word, letters, dic.isNeighbour(n.letter))
                letters.pop()

    let.letter = word[-1]
    word = word[:-1]


dic = dico
for l in let_lst.neighbours:
    word = ""
    letters = [l]
    """
    dic or letters modifies my l...
    ps is that the grid is not cleaned as it is supposed to be normally no '0' visited before look()

    letters: the last is the one we want to visit
    """
    if l.letter != '0':
        look(wordLength,word,letters, dic.isNeighbour(l.letter))

