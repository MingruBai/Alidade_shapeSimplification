import glob


formatted=open("formatted_country_shape_10.txt","w")

filelist=glob.glob("*.txt")
for country_file_name in filelist:
	if "_" in country_file_name: continue
	cur_file=open(country_file_name,"r")
	country_name=country_file_name.split(".")[0]
	while True:
		cur_line=cur_file.readline().strip()
		points=cur_line.split(";")
		if points==[""]: break
		for point in points:

			lat=point.split(":")[0].strip()
			lon=point.split(":")[1].strip()
			cat=int(point.split(":")[2].strip())
			if cat==0:
				formatted.write("\n%s: " %country_name)
			formatted.write("%s, %s; " %(lat,lon))
		formatted.write("\n")
	cur_file.close()
formatted.close()

