import numpy as np

def isMutant (dna) :
    count = 0
    n = len(dna)

    dna_matrix =[]
    for row in dna :
        row = list(row)
        dna_matrix.append(row)

    dna_mirror =[]
    for row in dna_matrix :
        row = row[::-1]
        dna_mirror.append(row)

    dna_trans = []
    for i in range(n) :
        l = []
        for j in range(n) :
            l.append(dna[j][i])
        dna_trans.append(l)

    for row in dna :
        for i in range(n - 3) :
            s = set(row[i:i + 4])
            if len(s) == 1 :
                count += 1
                if count == 2 : 
                    return True

    for row in dna_trans :
        for i in range(n - 3) :
            s = set(row[i:i + 4])
            if len(s) == 1 :
                count += 1
                if count == 2 : 
                    return True

    for i in range(1-n,n,1) :
        diag = list(np.diag(dna_matrix, i))
        if len(diag) >= 4 :
            for j in range(len(diag) - 3) :
                s = set(diag[j:j + 4])
                if len(s) == 1 :
                    count += 1
                    if count == 2 : 
                        return True

    for i in range(1-n,n,1) :
        diag = list(np.diag(dna_mirror, i))
        if len(diag) >= 4 :
            for j in range(len(diag) - 3) :
                s = set(diag[j:j + 4])
                if len(s) == 1 :
                    count += 1
                    if count == 2 : 
                        return True

    return False

dna = ['ATGCGA','CAGTGC','TTATGT','AGAAGG','CCCCTA','TCACTG']
print(isMutant (dna))