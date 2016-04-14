fname = "dataset.txt"
f = open(fname, "rb")
temp = f.readlines()
f.close()
dataset = []
for data in temp:
    dataset.append(data.replace('\r\n',''))

mess = []
all_result = []
all_result_decrypt = []
for data in range(0,len(dataset),3):
    print dataset[data]
    print dataset[data+1]
    print dataset[data+2]
