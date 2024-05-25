import argparse
import blosum as bl
# standard transition matrix build as dictionary
# if base row cell equals column base cell retun 1 otherwise -1
# 4x4 = 16 keys 
transm = {'AA':  1,
          'AC': -1,
          'AG': -1,
          'AT': -1,
          'CA': -1,
          'CC':  1,
          'CG': -1,
          'CT': -1,
          'GA': -1,
          'GC': -1,
          'GG':  1,
          'GT': -1,
          'TA': -1,
          'TC': -1,
          'TG': -1,
          'TT':  1}

LAr="\u2192"     # left Arrow
UpAr="\u2193"    # Up Arrow
DiAr="\u2198"    # Diagonal Arrow

def read_submat_file(filename):
    sm = {}
    f = open(filename, "r")
    line = f.readline()
    tokens = line.split("\t")
    ns = len(tokens)
    alphabet = []
    for i in range(0, ns):
        alphabet.append(tokens[i][0])
    for i in range(0,ns):
        line = f.readline();
        tokens = line.split("\t");
        for j in range(0, len(tokens)):
            k = alphabet[i]+alphabet[j]
            sm[k] = int(tokens[j])
    return sm




def printMatrix(s):
    #print(s)
    for i in range(len(s)):
        print("{}".format(s[i:i+1]))


def NeedlWunsch(seq1 , seq2 , transm , d):
    # d is the penalty gap
    scoreM = [['0,S'.rjust(4)]]         # score matrix a list of lists


    for i in range(1, len(seq2)+1):
        # initialize gap row
        scoreM[0].append((" 0"+','+'-').rjust(4))     # fill first row with gap penalty (d) multiplied by pos first pos = 0
    for i in range(1, len(seq1)+1):
        scoreM.append([" 0"+","+"-"])
    print("")
    print("Initial State of Score Matrix")
    printMatrix(scoreM)
    print("")
    print("===================================================")
    for i  in range(0, len(seq1)):
        for j in range (len(seq2)):
            localscore = int(scoreM[i][j].split(",")[0])
            s1 = localscore + scoreM_pos(seq1[i], seq2[j], transm , d);  #diagonal
            localscore = int(scoreM[i][j+1].split(",")[0])
            s2 =  localscore + d
            localscore = int(scoreM[i+1][j].split(",")[0])
            s3 = localscore + d
            if max(s1, s2, s3, 0) <= 0:
                s=" 0"+", -"
            else:
                s=str(max(s1, s2, s3, 0))+','+ maxof3tuple(s1 , s2 , s3)
            s=s.rjust(4)
            scoreM[i+1].append(s)
    return scoreM


def maxof3tuple(cell1 ,  cell2, cell3):
    if cell1  > cell2:
        if cell1 > cell3:
            return DiAr   # from Diagonal: cell1 > cell2, cell3
        else:
            return LAr    # from Left:     cell3 > cell1 > cell2 
    else:
        if cell2 > cell3:
            return  UpAr   # from Up:       cell2 > cell1, cell3 
        else:
            return LAr     # from Left:     cell3 > cell2 > cell1


def recover_align(traceM, seq1 , seq2):
    res = ["", ""]
    i = len(seq1)
    j = len(seq2)

    while i>0 or j >0:
        if traceM[i][j] == 1:
            res[0] = seq1[i-1] + res[0]
            res[1] = seq2[j-1] + res[1]
            i -= 1
            j -= 1
        elif traceM[i][j] == 3:
            res [0] = "-" + res[0]
            res [1] = seq2[j-1] + res[1]
            j -= 1
        else:
            res[0] = seq1[i-1] + res[0]
            res[1] = "-" + res[1]
            i -= 1
    return res


def scoreM_pos(cell1 , cell2 , transitionmatrix , gappenalty):
    dkey = cell1+cell2
    if  cell1 == "-" or cell2=="-":
         return  gappenalty   # return the gap penalty 
    else:
         return transitionmatrix[dkey]  #return value from disctionary key


def smblosum(seqstr1, seqstr2):
    sm = {}
    matrix = bl.BLOSUM(50)
    for j in "AGEHPW":
        for i in "AGEHPW":
           val = matrix[j][i]
           sm[i+j] = int(val)
    print(sm)
    return sm


def parseArgs():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('sq1', action='store', type=str, help='SWP Release')
    parser.add_argument('sq2', action='store', type=str, help='SWP diff file')
    args = parser.parse_args()
    return args
    
 
if __name__ == "__main__":
    args = parseArgs()
    print('Starting ...')
    print('Arguments:')
    print('\tsq1: ' + args.sq1)
    print('\tsq2: ' + args.sq2)
    #S = NeedlWunsch(args.sq1 , args.sq2 , transm , -1)
    transm = smblosum(args.sq1 , args.sq2)
    S = NeedlWunsch(args.sq1 , args.sq2 , transm , -2)

    print("Results:\n") #
    print("Score:") #
    printMatrix(S)

    print("")
    #recover_align(S, args.sq1 , args.sq2)

