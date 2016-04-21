
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


	"""
		if (A,B) in edges:
			if (A,B) in edge_count.keys():
				edge_count[(A,B)]=2
				dart[(A,B)]=dart[(A,B)]+[C]
			else:
				edge_count[(A,B)]=1
				dart[(A,B)]=[C]

		if (B,A) in edges:
			if (B,A) in edge_count.keys():
				edge_count[(B,A)]=2
				dart[(B,A)]=dart[(B,A)]+[C]
			else:
				edge_count[(B,A)]=1
				dart[(B,A)]=[C]

		if (C,B) in edges:
			if (C,B) in edge_count.keys():
				edge_count[(C,B)]=2
				dart[(C,B)]=dart[(C,B)]+[A]
			else:
				edge_count[(C,B)]=1
				dart[(C,B)]=[A]

		if (B,C) in edges:
			if (B,C) in edge_count.keys():
				dart[(B,C)]=dart[(B,C)]+[A]
				edge_count[(B,C)]=2
			else:
				dart[(B,C)]=[A]
				edge_count[(B,C)]=1

		if (A,C) in edges:
			if (A,C) in edge_count.keys():
				dart[(A,C)]=dart[(A,C)]+[B]
				edge_count[(A,C)]=2
			else:
				dart[(A,C)]=[B]
				edge_count[(A,C)]=1

		if (C,A) in edges:
			if (C,A) in edge_count.keys():
				dart[(C,A)]=dart[(C,A)]+[B]
				edge_count[(C,A)]=2
			else:
				dart[(C,A)]=[B]
				edge_count[(C,A)]=1

	"""	
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
	#x,y =  numpy.array(numpy.random.standard_normal((2,15)))
	

	"""
	cens,edges,triangles,neig = triang.delaunay(x,y)
	edges=[tuple(edge) for edge in edges]
	triangles=[tuple(tri) for tri in triangles]
	"""
	"""
	#Show Initial Triangulation:
	
	x=numpy.array(x)
	y=numpy.array(y)
	for t in triangles:
 	# t[0], t[1], t[2] are the points indexes of the triangle
 		t_i = [t[0], t[1], t[2], t[0]]
 		pylab.plot(x[t_i],y[t_i])

	pylab.plot(x,y,'o')
	pylab.show()
	"""
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
	show_shape(boundary_edges,x,y)
	return inter_x,inter_y


def linear(inter_x,inter_y,threshold):

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
	show()
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
"""
if __name__ == '__main__':

	#Parameters for Characteristics-Shape Simplification:
	lam=0.3
	filename="AF.txt"

	#Read points from file
	x,y=read_points(filename)

	#Call Characteristic-Shape Simplification:
	inter_x,inter_y=chi(x,y,lam)
	
	#Parameters for Linear Simplification:
	threshold=0.999

	#Call Linear Simplification:
	new_x,new_y=linear(inter_x,inter_y,threshold)
"""

if __name__ == '__main__':
	f=open("formatted_adjust.txt","r")
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


	while True:

		instr=raw_input("What now?")
		if instr=="n":
			fline=f.readline().strip()
			flist=fline.split(":")

			if flist==[""]:
				print "*** New Country! ***"
				fline=f.readline().strip()
				flist=fline.split(":")

			country=flist[0].strip()
			raw_points=flist[1].strip().split(";")

			x_points=[float(raw_point.split(",")[0]) for raw_point in raw_points if raw_point!=""]
			y_points=[float(raw_point.split(",")[1]) for raw_point in raw_points if raw_point!=""]
			i_area=Polygon([[x_points[i],y_points[i]] for i in range(len(x_points))]).area()
			print ("*** Point loaded for country %s. %d points. Area is %f.***" %(country,len(x_points),i_area))

			inter_x,inter_y=chi(x_points,y_points,lam)
			c_poly=Polygon([[inter_x[i],inter_y[i]] for i in range(len(inter_x))])
			c_area=c_poly.area()
			c_gain=-(i_area-c_area)*1.0/c_area*100.0
			print ("*** Now has %d points after Chi and an area of %f. Increased by %f percent.***" %(len(inter_x),c_area,c_gain))

			new_x,new_y=linear(inter_x,inter_y,threshold)
			l_poly=Polygon([[new_x[i],new_y[i]] for i in range(len(new_x))])
			l_area=l_poly.area()
			l_gain=(l_area-c_area)*1.0/c_area*100.0	

			cut=(c_poly-(c_poly&l_poly)).area()
			cut_percent=cut*1.0/c_area*100.0

			print ("*** Now has %d points after Linear and an area of %f. Further increased by %f percent. Cut-off is %f percent***" %(len(new_x),l_area,l_gain,cut_percent))

		elif instr=="l":
			lam_input=raw_input("Enter a lambda value: ")
			try:
				test=float(lam_input)
			except ValueError:
				print "Invalid input for lambda value."
				continue
			if float(lam_input)<0 or float(lam_input)>1:
				print "Invalid input for lambda value."
				continue
			lam=float(lam_input)

			inter_x,inter_y=chi(x_points,y_points,lam)
			c_poly=Polygon([[inter_x[i],inter_y[i]] for i in range(len(inter_x))])
			c_area=c_poly.area()
			c_gain=-(i_area-c_area)*1.0/c_area*100.0
			print ("*** Now has %d points after Chi and an area of %f. Increased by %f percent.***" %(len(inter_x),c_area,c_gain))

			new_x,new_y=linear(inter_x,inter_y,threshold)
			l_poly=Polygon([[new_x[i],new_y[i]] for i in range(len(new_x))])
			l_area=l_poly.area()
			l_gain=(l_area-c_area)*1.0/c_area*100.0	

			cut=(c_poly-(c_poly&l_poly)).area()
			cut_percent=cut*1.0/c_area*100.0

			print ("*** Now has %d points after Linear and an area of %f. Further increased by %f percent. Cut-off is %f percent***" %(len(new_x),l_area,l_gain,cut_percent))

		elif instr=="t":
			t_input=raw_input("Enter a threshold value: ")
			try:
				test=float(t_input)
			except ValueError:
				print "Invalid input for threshold value."
				continue
			if float(t_input)<0 or float(t_input)>1:
				print "Invalid input for threshold value."
				continue
			threshold=float(t_input)

			inter_x,inter_y=chi(x_points,y_points,lam)
			c_poly=Polygon([[inter_x[i],inter_y[i]] for i in range(len(inter_x))])
			c_area=c_poly.area()
			c_gain=-(i_area-c_area)*1.0/c_area*100.0
			print ("*** Now has %d points after Chi and an area of %f. Increased by %f percent.***" %(len(inter_x),c_area,c_gain))

			new_x,new_y=linear(inter_x,inter_y,threshold)
			l_poly=Polygon([[new_x[i],new_y[i]] for i in range(len(new_x))])
			l_area=l_poly.area()
			l_gain=(l_area-c_area)*1.0/c_area*100.0	

			cut=(c_poly-(c_poly&l_poly)).area()
			cut_percent=cut*1.0/c_area*100.0

			print ("*** Now has %d points after Linear and an area of %f. Further increased by %f percent. Cut-off is %f percent***" %(len(new_x),l_area,l_gain,cut_percent))

		elif instr=="s":
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
			print "Shape written to file."


		elif instr=="j":
			destination=raw_input("Which country?")
			while True:
				fline=f.readline().strip()
				if destination in fline:
					flist=fline.split(":")
					country=flist[0].strip()
					raw_points=flist[1].strip().split(";")
					x_points=[float(raw_point.split(",")[0]) for raw_point in raw_points if raw_point!=""]
					y_points=[float(raw_point.split(",")[1]) for raw_point in raw_points if raw_point!=""]
					i_area=Polygon([[x_points[i],y_points[i]] for i in range(len(x_points))]).area()
					print ("*** Point loaded for country %s. %d points.***" %(country,len(x_points)))

					inter_x,inter_y=chi(x_points,y_points,lam)
					c_poly=Polygon([[inter_x[i],inter_y[i]] for i in range(len(inter_x))])
					c_area=c_poly.area()
					c_gain=-(i_area-c_area)*1.0/c_area*100.0
					print ("*** Now has %d points after Chi and an area of %f. Increased by %f percent.***" %(len(inter_x),c_area,c_gain))

					new_x,new_y=linear(inter_x,inter_y,threshold)
					l_poly=Polygon([[new_x[i],new_y[i]] for i in range(len(new_x))])
					l_area=l_poly.area()
					l_gain=(l_area-c_area)*1.0/c_area*100.0	
					cut=(c_poly-(c_poly&l_poly)).area()
					cut_percent=cut*1.0/c_area*100.0

					print ("*** Now has %d points after Linear and an area of %f. Further increased by %f percent. Cut-off is %f percent***" %(len(new_x),l_area,l_gain,cut_percent))
					
					break

		elif instr=="p":
			print "lamda=", lam
			print "threshold=", threshold
	f.close()