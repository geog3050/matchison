#Obtain input from user and convert string to list
userlist = input("Please type the list of numbers you would like to examine in brackets and separate with commas (i.e. [1,2,3,]) then press enter: ")
checklist = eval(userlist)

#Create an empty list and add values from the user-generated list to it, but only if the same value has not previously been added.
#This creates a new list with the same numbers as the user-generated list in the same order, but without duplicates (regardless of if duplicates were present).
wodup = []
for i in checklist:
        if i not in wodup:
            wodup.append(i)

#Compare the length of the original user-generated list to the length of the list created without duplicates.
#If the lists are not of equal length, there were duplicates in the original; otherwise, there were no duplicates in the original.
#If there were duplicates in the original, the user is given the choice to print the modified list which has no duplicates.
if len(checklist) != len(wodup):
        choice = input("The list provided contains duplicate values. Would you like to remove the duplicates from your list? (Enter Y or N)")
        if choice == "Y":
                print("All duplicates have been removed: ", wodup)
                print("Duplicate check complete.")
        else: print("Duplicate check complete.")

else:
        print("The list provided does not contain duplicate values.")
        print("Duplicate check complete.")
