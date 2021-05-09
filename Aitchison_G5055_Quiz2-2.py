#Get user input for list to be examined in string form.
mystr = input("Please type the list of numbers you would like to examine in brackets and separate with commas (i.e. [1,2,3,]) then press enter: ")

#String input turned to list.
mylist = eval(mystr)

#Sort list and print the next to last element, which thanks to sorting will be the second largest number.
mylist.sort()
print(mylist[len(mylist)-2])
