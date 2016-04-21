from Polygon import *
import pylab
import glob

filelist=glob.glob("Results_final/*.txt")
#Check Population:
pfile=open("glp15ag.txt","r")
pop_dict=[]
ncols=8640
nrows=3432
for i in range(nrows):
	pline=pfile.readline().strip()
	plist=pline.split(" ")
	pop_dict.append(plist)
pfile.close()

def check_pop(point):
	lat=point[1]
	long=point[0]
	nrows=len(pop_dict)
	ncols=len(pop_dict[0])
	col=int((long+180)*24)
	#print lat,lon
	row=int(nrows-(lat+58)*24)
	if col>=ncols:
		col=col%ncols
	if row>=nrows: return 0.0
	#print row,col
	#print nrows
	return pop_dict[row][col]

for file_name in filelist:

	file=open(file_name,"r")
	line=file.readline()
	poly_list=[]

	points=line.split(";")
	if points==[""]: continue
	
	cur_points=[]
	for point in points:
		if point=="": continue
		lat=float(point.split(":")[0].strip())
		lon=float(point.split(":")[1].strip())
		cat=int(point.split(":")[2].strip())
		cur_points.append([lat,lon])
		if cat==4:
			poly_list.append(cur_points)
			cur_points=[]
	

	best_point=(-1110,-1110)
	peak_dense=-1
	for poly in poly_list:
		#print poly
		

		i_poly=Polygon(poly)
		fill_points=[]


		maxlat=-1000000
		minlat=1000000
		maxlon=-1000000
		minlon=1000000
		for point in poly:
			lat=point[0]
			lon=point[1]
			if lat>maxlat: maxlat=lat
			if lat<minlat: minlat=lat
			if lon>maxlon: maxlon=lon
			if lon<minlon: minlon=lon
		lat_values=[minlat+1.0/24*i for i in range(int((maxlat-minlat)*24))]
		lon_values=[minlon+1.0/24*i for i in range(int((maxlon-minlon)*24))]

		for lat in lat_values:
			for lon in lon_values:
				if i_poly.isInside(lat,lon):
					fill_points.append((lat,lon))

		if len(fill_points)==0: continue

		for point in fill_points:
			dens=float(check_pop(point))
			#print dens
			#print point,dens,peak_dense,best_point
			if dens>peak_dense:
				peak_dense=dens
				best_point=point
		"""
		x=[p[0] for p in fill_points]
		y=[p[1] for p in fill_points]
		pylab.plot(x,y,"*")
		pylab.show()
		"""
	#print best_point,file_name,peak_dense
	new=open("Country_bestpoint.txt","a")
	new.write("%s: %f, %f, %f\n" %(file_name,best_point[1],best_point[0],peak_dense))
	new.close()
