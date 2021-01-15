with open('a.txt','w') as f:
    for i in range(1,1000):
        print('data ' + str(i) + " ",sep='',file=f)