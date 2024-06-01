# Implements Smith-Waterman algorithm
# usage: python GE3_1_sw.py HGAEEWGAHG APAHEWEG
# 
import argparse

# use python library blosum installed with: pip install blosum
# this is needed if we want to use the blosum50 to get transition penalties
# instead of the standard matrix transm below where we have matc=1 not match = -1
import blosum as bl

from constants import *
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

# for BLOSUM use blosum python lib and create a dict dtnamically
# based on input sequences


def SmithWaterm(seq1 , seq2 , transm , d):
    # d is the penalty gap
    scoreM = [['0, S '.rjust(6)]]         # score matrix a list of lists

    for i in range(1, len(seq2)+1):
        # initialize gap row
        scoreM[0].append((" 0"+','+str(Empty+Dash+Empty)).rjust(7))     # fill first row with gap penalty (d) multiplied by pos first pos = 0
    for i in range(1, len(seq1)+1):
        scoreM.append([" 0"+","+str(Empty+Dash+Empty)])
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
                s=" 0"+","+str(Empty+Dash+Empty)
            else:
                s=str(max(s1, s2, s3, 0))+','+ maxof3tuple(s1 , s2 , s3)
            s=s.rjust(7)
            scoreM[i+1].append(s)
    return scoreM


def maxof3tuple(cell1 ,  cell2, cell3):
    lmax = max(cell1, cell2, cell3)
    if cell1 == cell2 == cell3:
        result = Empty+StAr+Empty   # i.e: ' * '
    else:
        if cell1 == lmax:
            if cell1 == cell2:
                result = Empty+DiAr+UpAr
            elif cell1 == cell3:
                result = LAr+DiAr+Empty
            else:
                result = Empty+DiAr+Empty   # from Diagonal: cell1 > cell2, cell3
        elif cell2 == lmax:
            if cell2 == cell3:
                result = LAr+Empty+UpAr
            else:
                result = Empty+Empty+UpAr
        else:
            result = LAr+Empty+Empty
    return result



def scoreM_pos(cell1 , cell2 , transitionmatrix , gappenalty):
    dkey = cell1+cell2
    if  cell1 == "-" or cell2=="-":
         return  gappenalty   # return the gap penalty 
    else:
         return transitionmatrix[dkey]  #return value from disctionary key


def smblosum(seqstr1, seqstr2):
    sm = {}
    matrix = bl.BLOSUM(50)
    s = seqstr1+seqstr2
    s = set(s)
    s = list(s)
    s = "".join(s)
    for j in s:
        for i in s:
            val = matrix[j][i]
            sm[i+j] = int(val)
    print(sm)
    return sm


def parseArgs():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('sq1', action='store', type=str, help='SWP Release')
    parser.add_argument('sq2', action='store', type=str, help='SWP diff file')
    parser.add_argument('gap', action='store', type=str, help='')
    args = parser.parse_args()
    return args
    
 
if __name__ == "__main__":
    args = parseArgs()
    print('Starting ...')
    print('Arguments:')
    print('\tsq1: ' + args.sq1)
    print('\tsq2: ' + args.sq2)
    print('\tgap: ' + args.gap)
    gap = (-1)*int(args.gap)
    
    transm = smblosum(args.sq1 , args.sq2)
    S = SmithWaterm(args.sq1 , args.sq2 , transm , gap)

    print("Results:\n") #
    print("Score:") #
    printMatrix(S)


