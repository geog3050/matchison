climate = input("Please input the climate (in lowercase) and then press enter: ")
temp_string = input("Please input all temperature measurements for this climate as a list enclosed in brackets (i.e. [24.7, 44, 76]): ")
temp_float = eval(temp_string)
print("climate: ", climate)
print("temperatures: ", temp_float)
if climate == "tropical":
	for i in temp_float:
		if i <= 30:
			print("F")
		else: print("U")
elif climate == "continental":
	for i in temp_float:
		if i <= 25:
			print("F")
		else: print("U")
else:
	for i in temp_float:
		if i<= 18:
			print("F")
		else: print("U")
