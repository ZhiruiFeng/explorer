import sys
if __name__ == "__main__":
    name = "USA-road-t.BAY.gr"
    print(name)
    with open(name) as f:
        line = f.readline()
        flag = 0
        l = line.strip().split()
        store = 0
        cnt = 0
        while line:
            cnt += 1
            sys.stdout.write("\r {}".format(cnt))
            if l[0] == 'a':
                if flag == 0:
                    flag = 1
                    store = l[3]
                else:
                    flag = 0
                    if store != l[3]:
                        print("find unequal, at line:{}".format(cnt))
                        print("pre: {}, now {}".format(store, l[3]))
                        break
            line = f.readline()
        print("all equal")
    """
    ##########
    name = "USA-road-d.NY.gr"
    print(name)
    with open(name) as f:
        line = f.readline()
        flag = 0
        l = line.strip().split()
        store = 0
        cnt = 0
        while line:
            cnt += 1
            sys.stdout.write("\r {}".format(cnt))
            if l[0] == 'a':
                if flag == 0:
                    flag = 1
                    store = l[3]
                else:
                    flag = 0
                    if store != l[3]:
                        print("find unequal, at line:{}".format(cnt))
                        print("pre: {}, now {}".format(store, l[3]))
                        break
            line = f.readline()
        print("all equal")
    ###############
    name = "rome99.road"
    print(name)
    with open(name) as f:
        line = f.readline()
        pair = {}
        for i in range(1,3354):
            pair[i]={}
        l = line.strip().split()
        while line:
            if l[0] == 'a':
                pair[int(l[1])][int(l[2])] = int(l[3])
            line = f.readline()
            l = line.strip().split()
        print(pair[3352])
        cnt = 0
        for i in range(1,3354):
            sys.stdout.write("\r {}".format(i))
            for j in range(1,3354):
                if j in pair[i]:
                    if i in pair[j]:
                        if pair[i][j] != pair[j][i]:
                            cnt += 1
                    else:
                        cnt += 1
                else:
                    if i in pair[j]:
                        cnt += 1
        print("unequal pairs:{}".format(cnt))
    """
