
file=open("shapeIndex.txt","r")
hint_dic={}
while True:
	line=file.readline().strip()
	if len(line)<2: break
	hint=line.split()[0].strip()
	index=line.split()[1].strip()
	hint_dic[index]=hint

file.close()


file=open("Result_bestpoint_first.txt","r")
new=open("hint+bestpoint.txt","w")
while True:
	line=file.readline()
	index=line.split(":")[0].strip()
	if index not in hint_dic.keys(): continue
	hint=hint_dic[index]
	new.write("%s, %s" %(hint,line))
file.close()
new.close()