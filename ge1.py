def name_and_values(pos):
    """ Get name and values list for a protein
        Return: a list of protein and values
    """

    prompt = "Enter name for "+pos  + " protein "
    protein = input(prompt)
    values = []
    for i in (1, 2):
        print("Get value {}:".format(str(i)))
        while True:
            try:
                num = int(input())
                if  num > 0:
                    print("You entered: {}".format(num))
                    values.append(num)
                    break
                else:
                    print("entry should be positive ")
            except ValueError:
                print("Please enter a valid integer > 0 ")
    return [protein, values]


if __name__ == '__main__':
    L = name_and_values("First")
    print("First List is {}".format(L))
    L1 = L[1]
    print("Values for fist are {}".format(L1))
    L = name_and_values("Second")
    print("Second List is {}".format(L))
    L2 = L[1]
    print("Values for second are {}".format(L2))
    print("join values of the two lists L1 and L2 into a new L3 List")
    L3 = L1 + L2
    print("Values for joined L1 and L2 are {}".format(L3))
    if any(item == 10 for item in L3):
        print("Found 10 in at least one pos")
    else:
        print("Nothing found")
    # another way for the above    
    for ind, item in enumerate(L3):
        if item == 10:
           print("Found 10 at pos {}".format(ind))
    L = name_and_values("Third")
    L3 = L3 + L[1]
    print("The new list - all values of the lists joined: {}".format(L3))
    L3 = L3[2:]
    print("The new list of values without the first list is: {}".format(L3))
    # one way to reverse the list using slice end to start with step -1
    # print("The new list without the first list reversed is: {}".format(L3[::-1]))
    # or we can reverse the list in place using list.reverse()
    L3.reverse()
    print("The new list of values without the first list reversed is: {}".format(L3))


