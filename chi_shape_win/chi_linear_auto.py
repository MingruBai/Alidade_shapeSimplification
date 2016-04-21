
import pylab
import numpy
import heapq
import collections
from scipy import stats
from pylab import *
from scipy.spatial import Delaunay
from Polygon import *

def show_shape(boundary_edges,x,y):
	for edge in boundary_edges:
		source=edge[0]
		target=edge[1]
		xs=[x[source],x[target]]
		ys=[y[source],y[target]]
		pylab.plot(xs,ys,color="blue")
	pylab.plot(x,y,'o')
	title("After Chi")
	pylab.show()

#initial calculation to find boundary edges:
def count_boundary_edges(triangles,edges):
	boundary_edges=[]
	edge_count=collections.Counter()
	dart={}

	for edge in edges:
		dart[edge]=[]

	for tri in triangles:
		for s in tri:
			for t in tri:
				if s!=t and (s,t) in edges:
					c=[p for p in tri if p!=s and p!=t]
					edge_count[(s,t)]+=1
					dart[(s,t)]+=c

	for edge in edge_count.keys():
		if edge_count[edge]==1:
			boundary_edges.append(edge)
	
	return boundary_edges,dart

#initial calculation to find boundary points:
def count_boundary_points(num,boundary_edges):
	boundary_points=[]
	for i in range(num):
		for edge in boundary_edges:
			if i in edge and i not in boundary_points:
				boundary_points.append(i)	
	return boundary_points

#Check if polygon is regular if edge is removed:
def is_regular(boundary_points,dart,edge):
	for third in dart[edge]:	
		if third not in boundary_points:
			return True
	return False

def get_length(edge,x,y):
	source=edge[0]
	target=edge[1]
	sx=x[source]
	sy=y[source]
	tx=x[target]
	ty=y[target]
	length=((sx-tx)**2+(sy-ty)**2)**0.5
	return length

def pass_points(boundary_points,x,y):
	x_list=[]
	y_list=[]
	for i in range(len(boundary_points)):
		point=boundary_points[i]
		vx=x[point]
		vy=y[point]
		x_list.append(vx)
		y_list.append(vy)
	return x_list,y_list

def chi(x,y,lam):

	#Initialize points and triangulation:
	points=numpy.array([(x[i],y[i]) for i in range(len(x))])
	triangles=Delaunay(points).simplices
	edges=[]

	for t in triangles:
		if len(t)==3:
			A=t[0]
			B=t[1]
			C=t[2]
			if (A,B) not in edges and (B,A) not in edges: edges.append((A,B))
			if (A,C) not in edges and (C,A) not in edges: edges.append((A,C))
			if (C,B) not in edges and (B,C) not in edges: edges.append((B,C))

	#Get max and min length:
	max_len=0
	min_len=1000000
	for edge in edges:
		l=get_length(edge,x,y)
		if l>max_len:
			max_len=l
		if l<min_len:
			min_len=l

	l=lam*(max_len-min_len)+min_len


	#Get initial boundary:
	boundary_edges,dart=count_boundary_edges(triangles,edges)
	boundary_points=count_boundary_points(len(x),boundary_edges)

	#Constuction priority queue:
	boundary_edges_heapq=[(-get_length(edge,x,y),edge) for edge in boundary_edges]
	heapq.heapify(boundary_edges_heapq)

	#Shaving
	while boundary_edges_heapq!=[]:
		cur_tuple=heapq.heappop(boundary_edges_heapq)
		cur_len=cur_tuple[0]
		cur_edge=cur_tuple[1]
		if abs(cur_len)>=l and is_regular(boundary_points,dart,cur_edge):

			edges.remove(cur_edge)
			boundary_edges.remove(cur_edge)

			cur_source=cur_edge[0]
			cur_target=cur_edge[1]
			add_list=[]
			for third in dart[cur_edge]:
				if third not in boundary_points:
					if (third,cur_source) in edges:
						add_list.append((third,cur_source))
						boundary_points.append(third)
					if (cur_source,third) in edges:
						add_list.append((cur_source,third))
						boundary_points.append(third)
					if (third,cur_target) in edges:
						add_list.append((third,cur_target))
						boundary_points.append(third)
					if (cur_target,third) in edges:
						add_list.append((cur_target,third))
						boundary_points.append(third)
			boundary_edges=boundary_edges+add_list
			for to_add in add_list:
				heapq.heappush(boundary_edges_heapq,(-get_length(to_add,x,y),to_add))
	boundary_points=sorted(list(set(boundary_points)))
	inter_x,inter_y=pass_points(boundary_points,x,y)
	#show_shape(boundary_edges,x,y)
	return inter_x,inter_y

def pre(x_points,y_points):
	l=0.5
	px=x_points[0]
	py=y_points[0]
	i=1
	while i<len(x_points):
		x=x_points[i]
		y=y_points[i]
		dis=((x-px)**2+(y-py)**2)**0.5
		if dis>=l:
			num=int(dis/l)
			x_add_list=[]
			y_add_list=[]
			x_interval=(x-px)*1.0/num
			y_interval=(y-py)*1.0/num
			for n in range(1,num):
				x_add_list.append(float(px+n*x_interval))
				y_add_list.append(float(py+n*y_interval))
			x_points=x_points[0:i]+x_add_list+x_points[i:]
			y_points=y_points[0:i]+y_add_list+y_points[i:]
			i=i+num-1

		i=i+1
		px=x
		py=y
	return x_points,y_points
		



def linear(inter_x,inter_y,threshold):
	return inter_x,inter_y
	
	plot_x=[]
	plot_y=[]
	cur_x=[]
	cur_y=[]
	for i in range(len(inter_x)):
		x=inter_x[i]
		y=inter_y[i]
		cur_x.append(float(x))
		cur_y.append(float(y))
		if len(cur_x)>2:
			cor,p=stats.pearsonr(cur_x,cur_y)
			if abs(cor)<threshold:
				plot_x.append(cur_x[0])
				plot_y.append(cur_y[0])
				plot_x.append(cur_x[-2])
				plot_y.append(cur_y[-2])
				cur_x=[cur_x[-1]]
				cur_y=[cur_y[-1]]
	plot_x.append(cur_x[0])
	plot_y.append(cur_y[0])

	plot(plot_x+[plot_x[0]],plot_y+[plot_y[0]],"-o")
	title("After Linear")
	#show()
	return plot_x,plot_y
	

def read_points(filename):
	sfile=open(filename,"r")
	line=sfile.readline().strip()
	slist=line.split(";")
	x=[]
	y=[]
	for point in slist:
		sub_list=point.split(":")
		if point=="":continue
		x.append(float(sub_list[0]))
		y.append(float(sub_list[1]))
	return x,y

def check_pop(pop_dict,point):
	lat=point[0]
	long=point[1]
	nrows=len(pop_dict)
	ncols=len(pop_dict[0])
	col=int((long+180)*24)
	row=int(nrows-(lat+58)*24)
	if col>=ncols or row>=nrows:
		return 0.0
	return pop_dict[row][col]

if __name__ == '__main__':
	f=open("formatted_country_shape_10.txt","r")
	x_points=[]
	y_points=[]
	new_x=[]
	new_y=[]
	country=""
	lam=0.05
	threshold=0.999

	i_area=0
	c_area=0
	l_area=0
	c_poly=Polygon([(0,0)])
	l_poly=Polygon([(0,0)])

	i_country_dict={}
	f_country_dict={}

	i_area_dict={}
	f_area_dict={}


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

	lam_list=[]

	while True:

		fline=f.readline().strip()
		flist=fline.split(":")

		if flist==[""]:

			stat=file("Results/stat.txt","a")
			if country in i_country_dict.keys() and country in f_country_dict.keys():
				stat.write("%s | %d | %d | %f | %f | " %(country,i_country_dict[country],f_country_dict[country],i_area_dict[country],f_area_dict[country]))
				for i in range(len(lam_list)):
					stat.write("%f" %lam_list[i])
					stat.write(";")
				stat.write("\n")
			stat.close()

			lam_list=[]
			#print "*** New Country! ***"
			
			fline=f.readline().strip()
			flist=fline.split(":")
			if flist==[""]:break

		country=flist[0].strip()
		raw_points=flist[1].strip().split(";")

		x_points=[float(raw_point.split(",")[0]) for raw_point in raw_points if raw_point!=""]
		y_points=[float(raw_point.split(",")[1]) for raw_point in raw_points if raw_point!=""]
		i_poly=Polygon([[x_points[i],y_points[i]] for i in range(len(x_points))])
		i_area=i_poly.area()
		print ("*** Point loaded for country %s." %(country))

		x_points,y_points=pre(x_points,y_points)

		
		
		if country in i_country_dict.keys():
			i_country_dict[country]=i_country_dict[country]+len(x_points)
			i_area_dict[country]=i_area_dict[country]+i_area
		else:
			i_country_dict[country]=len(x_points)
			i_area_dict[country]=i_area

		
		if len(x_points)<20: 
			print "Dropped for too small."
			continue
			
		if len(x_points)<50: 
			center=i_poly.center()
			if check_pop(pop_dict,center)<1.0:
				print "Dropped for too few people."
				continue

		
		inter_x,inter_y=chi(x_points,y_points,lam)
		new_x,new_y=linear(inter_x,inter_y,threshold)
		l_area=Polygon([[new_x[i],new_y[i]] for i in range(len(new_x))]).area()

		i_lam=lam
		if len(x_points)>=5000: 
			num_thres=500
		elif len(x_points)>=500: 
			num_thres=200
		else: 
			num_thres=50
		
		while (len(new_x)>num_thres):
			lam=lam+0.01
			if lam>1: break
			inter_x,inter_y=chi(x_points,y_points,lam)
			new_x,new_y=linear(inter_x,inter_y,threshold)
			l_area=Polygon([[new_x[i],new_y[i]] for i in range(len(new_x))]).area()
		lam_list.append(lam)
		lam=i_lam
		


		if country in f_country_dict.keys():
			f_country_dict[country]=f_country_dict[country]+len(new_x)
			f_area_dict[country]=f_area_dict[country]+l_area
		else:
			f_country_dict[country]=len(new_y)
			f_area_dict[country]=l_area


		new=open("Results/%s.txt" %country,"a")
		for i in range(len(new_x)):
			vx=new_x[i]
			vy=new_y[i]
			if i==0:
				new.write("%f:%f:0;" %(vx,vy))
			else:
				new.write("%f:%f:1;" %(vx,vy))
		new.write("%f:%f:1;" %(new_x[0],new_y[0]))
		new.write("%f:%f:4;" %(new_x[0],new_y[0]))
		new.close()
		#print "Shape written to file."


		
	f.close()