import random

list = []
num = 0

while num < 1000:
    flag = 0
    dict = {}
    k = random.randint(1, 10)
    v = random.randint(1, 150)
    for map in list:
        if map.get(k) == v:
            flag = 1
            break
    if flag == 1:
        continue
    dict[k] = v
    list.append(dict)
    num = num + 1
    msg = str(k) + "::" + str(v) + "::" + str(random.randint(1, 5))
    print(msg)
