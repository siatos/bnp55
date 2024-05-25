from constants import * 
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



def NeedlWunsch(seq1 , seq2 , transm , d):
    # d is the penalty gap
    scoreM = [['0,S'.rjust(4)]]         # score matrix a list of lists


    for i in range(1, len(seq2)+1):
        # initialize gap row
        scoreM[0].append((str(d*i)+','+LAr).rjust(4))     # fill first row with gap penalty (d) multiplied by pos first pos = 0
    for i in range(1, len(seq1)+1):
        scoreM.append([str(d*i)+","+UpAr])
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
            s=str(max(s1, s2, s3))+','+ maxof3tuple(s1 , s2 , s3)
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
    ls = list(set(s))
    print(ls)
    for j in ls:
        for i in ls:
           val = matrix[j][i]
           sm[i+j] = int(val)
    print(sm)
    return sm


def parseArgs():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('sq1', action='store', type=str, help='')
    parser.add_argument('sq2', action='store', type=str, help='')
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

    S = NeedlWunsch(args.sq1 , args.sq2 , transm , gap)

    #transm = smblosum(args.sq1 , args.sq2)
    #S = SmithWaterm(args.sq1 , args.sq2 , transm , gap)


    print("Results:\n") #
    print("Score:") #
    printMatrix(S)

