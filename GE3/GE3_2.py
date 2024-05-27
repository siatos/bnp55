import argparse
import numpy as np
import pandas as pd
import math
from math import log

calc_sequences = ["AAGCAT", "GCTAAA", "TATCAA"]
total_score = [0, 0, 0]

def parseArgs():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('dataseq', action='store', type=str, help='')
    parser.add_argument('rows', action='store', type=str, help='')
    parser.add_argument('calc_seq', action='store', default=0, type=int, help='')
    args = parser.parse_args()
    return args

def populate_p_matrix(datam, r, c, pddf, tp="PWM"):
    # 
    status=True
    for j in range(c):
        sum_elements = [0, 0, 0, 0]
        for i in range(r):
            if datam[i, j] == seq_elements[0]:
                sum_elements[0] = sum_elements[0]+1
            elif datam[i, j] == seq_elements[1]:
                sum_elements[1] = sum_elements[1]+1
            elif datam[i, j] == seq_elements[2]:
                sum_elements[2] = sum_elements[2]+1
            elif datam[i, j] == seq_elements[3]:
                sum_elements[3] = sum_elements[3]+1
            else:
                print("{} {} {} - check your data for error:".format(i, j, datam[i, j]))
                status=False
        if tp == "PFM":
            pddf.iloc[0, j] = sum_elements[0]
            pddf.iloc[1, j] = sum_elements[1]
            pddf.iloc[2, j] = sum_elements[2]
            pddf.iloc[3, j] = sum_elements[3]
        elif tp == "PPM":
            pddf.iloc[0, j] = sum_elements[0] / r
            pddf.iloc[1, j] = sum_elements[1] / r
            pddf.iloc[2, j] = sum_elements[2] / r
            pddf.iloc[3, j] = sum_elements[3] / r
        else:
            try:
               pddf.iloc[0, j] = log((sum_elements[0] / r)/0.25)
            except ValueError:
               pddf.iloc[0, j] = -np.inf
            try:
               pddf.iloc[1, j] = log((sum_elements[1] / r)/0.25)
            except ValueError:
               pddf.iloc[1, j] = -np.inf
            try:
               pddf.iloc[2, j] = log((sum_elements[2] / r)/0.25)
            except ValueError:
               pddf.iloc[2, j] = -np.inf
            try:
               pddf.iloc[3, j] = log((sum_elements[3] / r)/0.25)
            except ValueError:
               pddf.iloc[3, j] = -np.inf
    print("======> tp={}".format(tp))
    print(pddf)
    return status, pddf

def find_score(pddf, cbase, pos):
    score = 0
    for c in pddf.index.values:
        if c == cbase:
            # print("Pos: {} Letter: {} score: {}".format(pos, c, pddf.at[c, 'pos'+str(pos)]))
            score = pddf.at[c, 'pos'+str(pos)]
            break
        else:
            continue
    return score

def calculate_score(seq2check, pddf):
    total_score = 0
    for j in range(len(seq2check)):
       pos = j+1
       item = seq2check[j]
       # print(item)
       score = find_score(pddf, item, pos)
       # print(score)
       total_score = total_score + score
    return total_score




if __name__ == "__main__":
    args = parseArgs()
    print('Starting ...')
    print('Arguments:')
    print('\tdata seq: ' + args.dataseq)
    print('\trows: ' + args.rows)
  
    # Initialize parameters
    no_rows = int(args.rows)
    no_columns = 6
    data = args.dataseq
    no_columns = int(len(data)/no_rows)
    print("we will split dataseq of {} chars in {} rows of {} chars each".format(len(data), no_rows, no_columns))
    print("")
    seq_elements = ["A", "G", "C", "T"]
    sum_elements = [0, 0, 0, 0]
    # Create the data matrix
    print("create the data matrix: {}x{}".format(no_rows, no_columns))
    data2 = np.empty((no_rows, no_columns), dtype=str)
    print("")
    for i in range(no_rows):
        x = data[(i * no_columns):((i + 1) * no_columns)]
        data2[i, :] = list(x)
    print(data2)
    print("")
    # Create PWM matrix
    p_matrix = np.zeros((4, no_columns))

    # Set row and column names for PWM matrix use panda dataframe
    p_df = pd.DataFrame(p_matrix, index=seq_elements, columns=[f"pos{j}" for j in range(1, no_columns + 1)])

    # Populate PPM matrix
    status, p_df_pfm = populate_p_matrix(data2, no_rows, no_columns, p_df, "PFM")
    print("")
    # Populate PPM matrix
    status, p_df_ppm = populate_p_matrix(data2, no_rows, no_columns, p_df, "PPM")
    print("")

    if args.calc_seq == 1:
        for i in range(len(calc_sequences)):
            total_score[i] = calculate_score(calc_sequences[i], p_df_pfm)

    # Populate PWM matrix
    status, p_df_pwm = populate_p_matrix(data2, no_rows, no_columns, p_df)
    print("")

    if args.calc_seq == 1:
        for i in range(len(calc_sequences)):
            print("sequence: {} total score: {}".format(calc_sequences[i], total_score[i]))


