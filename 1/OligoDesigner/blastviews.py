import numpy as np

str1="AGCTCTTACA"
str2="CGCTCATTCA"
str3="CGCGCATTCA"

list1=list(str1)
list2=list(str2)
list3=list(str3)

listx=np.column_stack((list1,list2,list3))
#print(listx)
for lx in listx:
    i2=""
    listqc=[]
    for i in ''.join(lx):
        if i not in i2:
            i2+=i
#    print(i2)
    listqc.append(i2)
    for lq in listqc:
        listjb=[]
        if ''.join(sorted(lq))=='AC':
            lq='M'
        if ''.join(sorted(lq))=='GT':
            lq='K'
        if ''.join(sorted(lq))=='CT':
            lq='Y'
        if ''.join(sorted(lq))=='AT':
            lq='W'
        if ''.join(sorted(lq))=='AG':
            lq='R'
        if ''.join(sorted(lq))=='ACT':
            lq='H'
        if ''.join(sorted(lq))=='CGT':
            lq='B' 
        if ''.join(sorted(lq))=='ACG':
            lq='V'
        if ''.join(sorted(lq))=='AGT':
            lq='D'    
        if ''.join(sorted(lq))=='ACGT':
            lq='N'
        listjb.append(lq)
            
        print(listjb)