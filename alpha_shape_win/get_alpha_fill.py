
from sys import *
from CGAL.Alpha_shapes_2 import *
from CGAL.Triangulations_2 import Delaunay_triangulation_2
from matplotlib import collections as mc
from CGAL.Kernel import *
from math import *
from pylab import *
import matplotlib.pyplot as plt
from Polygon import *

def Point_2_str(self):
    return "Point_2"+str((self.x(), self.y()))
# now we turn it into a member function
Point_2.__str__ = Point_2_str

def show_alpha_values(AS):
	print "Alpha spectrum"
	for alpha_value in AS.alpha:
		print alpha_value

			
def test_Alpha_shapes_2(points,alpha):	
	verbose = True
	
	list_of_points = points
		
	
	a=Alpha_shape_2()
	a.set_mode(Alpha_shape_2.Mode.REGULARIZED)
	a.make_alpha_shape(list_of_points)
	a.set_alpha(float(alpha))
	alpha_shape_edges = []
	alpha_shape_vertices = []
	for it in a.alpha_shape_edges:
		alpha_shape_edges.append(a.segment(it))
		
	for it in a.alpha_shape_vertices:
		alpha_shape_vertices.append(it)

	

	print "alpha_shape_edges"	
	print len(alpha_shape_edges)
	print "alpha_shape_vertices"	
	print len(alpha_shape_vertices)
	print "Optimal alpha: " 
	print a.find_optimal_alpha(2).next()
	_showAlphaShape(list_of_points, alpha_shape_edges)
	return alpha_shape_edges
	
# 	show_alpha_values(a)
def _showAlphaShape(points,edges):

    # draw cluster points
    x = [pt.x() for pt in points]
    y = [pt.y() for pt in points]
    plt.plot(x,y,"*")
    

    lines=[[(edge.source().x(),edge.source().y()),(edge.target().x(),edge.target().y())] for edge in edges]
    for x,y in lines:
    	plt.plot([x[0],y[0]],[x[1],y[1]],color="black")
    plt.autoscale(True)
    plt.show()


if __name__ == '__main__':
	f=open("formatted_country_shape_10.txt","r")
	points=[]
	country=""
	alpha_edges=[]

	while True:
		instr=raw_input("What now?")
		if instr=="n":
			line=f.readline().strip()
			list=line.split(":")

			if list==[""]:
				print "*** New Country! ***"
				line=f.readline().strip()
				list=line.split(":")

			country=list[0].strip()
			raw_points=list[1].strip().split(";")
			points=[(float(raw_point.split(",")[0].strip()),float(raw_point.split(",")[1].strip())) for raw_point in raw_points if raw_point!=""]
			print ("*** Point loaded for country %s. ***" %country)
			print ("Number of points is: ")
			print len(points)
			i_poly=Polygon(points)
			fill_points=[]


			maxlat=-1000000
			minlat=1000000
			maxlon=-1000000
			minlon=1000000

			density=100
			for point in points:
				lat=point[0]
				lon=point[1]
				if lat>maxlat: maxlat=lat
				if lat<minlat: minlat=lat
				if lon>maxlon: maxlon=lon
				if lon<minlon: minlon=lon
			lat_values=[minlat+(maxlat-minlat)*1.0/density*i for i in range(density+1)]
			lon_values=[minlon+(maxlon-minlon)*1.0/density*i for i in range(density+1)]
			#print lat_values,lon_values
			for lat in lat_values:
				for lon in lon_values:
					if i_poly.isInside(lat,lon):
						fill_points.append((lat,lon))

			points=points+fill_points
			points=[Point_2(point[0],point[1]) for point in points]


		elif instr=="a":
			alpha=raw_input("Enter an alpha value: ")
			try:
				test=float(alpha)
			except ValueError:
				print "Invalid input for alpha value."
				continue
			alpha_faces=test_Alpha_shapes_2(points,alpha)
			alpha_edges=[["%s:%s:" %(face.source().x(),face.source().y()),"%s:%s:" %(face.target().x(),face.target().y())] for face in alpha_faces]

		elif instr=="save":
			new=open("Results/%s.txt" %country,"a")
			first_edge=alpha_edges[0]
			first_source=first_edge[0]
			source=first_source
			target=first_edge[1]

			while True:
				if target==first_source:
					new.write(source+"1;")
					new.write(target+"1;")
					new.write(target+"4;")
					break
				if source==first_source:
					new.write(source+"0;")
				else:
					new.write(source+"1;")

				for edge in alpha_edges:
					if target in edge and target==edge[0]:
						source=target
						target=edge[1]
						break
			new.close()
			print "Shape written to file."




		elif instr=="j":
			destination=raw_input("Which country?")
			while True:
				line=f.readline().strip()
				if destination in line:
					list=line.split(":")
					country=list[0].strip()
					raw_points=list[1].strip().split(";")
					points=[Point_2(float(raw_point.split(",")[0].strip()),float(raw_point.split(",")[1].strip())) for raw_point in raw_points if raw_point!=""]
					print ("*** Point loaded for country %s. ***" %country)
					print ("Number of points is: ")
					print len(points)
					break
	f.close()