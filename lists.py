#making a list


x = [4,3,4,6,6,2,2,7,3]

x.append(2)
#appends
x.insert(2,99)
x.remove(2)

print(x[5])
#printing arrays blah blah blah

#slicing arrays

print(x[2:4])
#last element is non inclusive

print(x[-2])
#second to last element

print(x.count(6))

x.sort()
#can also sorts lists of strings alphabetically

print(x)

#multidimensional lists

x = [[5,9],[2,1],[8,7],[1,9]]

print(x[2][0])
#etc etc
