climate = input("Please input the climate (in lowercase) and then press enter: ")
temp_string = input("Please input all temperature measurements for this climate as a list enclosed in brackets (i.e. [24.7, 44, 76]): ")
temp_float = eval(temp_string)
print(climate)
print(temp_float)
def folding(climate,temp_float):
        threshold = 18
        if climate == "tropical":
                threshold = 30
        elif climate == "continental":
                threshold = 25

        for temp in temp_float:
                if temp <= threshold:
                        print("F")
                else:
                        print("U")
