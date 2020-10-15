import sys
#import argparse

id_string=[]
name=[]
surname=[]
age_string=[]

for i in range (0,int(sys.argv[1])):
    idn, n, s, a = input("ID Name Surname Age\n").split()
    id_string.append(idn)
    name.append(n)
    surname.append(s)
    age_string.append(a)
    
    
id_no=[int(j) for j in id_string]
age=[int(j) for j in age_string]

personList=[name, surname, age]

print(str(personList))

#Kisi ozelliklerinin oldugu tuple
people=[]
for i, j, k in zip(name,surname,age):
    people.append((i,j,k))


print(str(people))

#ID tuple hali
id_tup=tuple(id_no)

dictionary=dict(zip(id_tup, people))
print(dictionary)
