
#!/bin/python3
# 

count = int(input().strip())
words = []
for j in range(count):
    words.append(input().strip())
    
dd = {}
for wd in words:
    ct = dd.get(wd)
    if ct:
        dd[wd] = ct+1
    else:
        dd[wd] = 1

print(len(dd))
for wd in words:
    print(dd.get(wd), ' ', end='')
print()

