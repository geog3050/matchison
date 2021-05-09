#Get user inputs for the string to be searched and the string character to search for.
lookat = input("Please type the string variable (i.e. a sentence of words) you would like to examine, then press enter: ")
letter = input("Please type the letter you would like to search for in the prior string variable, then press enter (search is case sensitive): ")

#Search first string for instance of the search character entered, and print "Yes" or "No" depending on outcome.
if letter in lookat:
        print("Yes")
else: print("No")
