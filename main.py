from utils import readYaml
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from BSplines import BSpline

def objective(x):

	error = 0
	for i,val in enumerate(frame_number):
		#print(i , BSpline(val,order,x[8:],x[0:8]),gazeX[i],(BSpline(val,order,x[8:],x[0:8]) - gazeX[i])**2 )
		error += (BSpline(val,order,x[8:],x[0:8]) - gazeX[i])**2 

	return error

def main():

	gazeFile = "./gaze_data/dos6_gaze.yml"
	gazeData = readYaml(gazeFile)

	nViewers = len(gazeData)

	#Plot gaze data for each user
	#TODO: make this optional to view + add plot names 
	for i in range(nViewers):
		
		x_coords = [float(j[0]) for j in gazeData[i]]
		y_coords = [float(j[1]) for j in gazeData[i]]

		plt.plot(x_coords,'.')

	#plt.show()

	global order, frame_number, gazeX


	order = 4;
	frame_number = [1,100,200,500]
	gazeX = [50,50,200,200]

	a = 0;b=1080; k1 = 100 ; width_retargettted = 720;

	cons = (

			#[alp,alp,alp,alp,beta,beta,beta,beta]
			#Control points 0-3 are same
			{'type': 'eq', 'fun': lambda x:  x[0]-x[1]},
			{'type': 'eq', 'fun': lambda x:  x[1]-x[2]},
			{'type': 'eq', 'fun': lambda x:  x[2]-x[3]},
			
			# Control points 4-7 are same
			{'type': 'eq', 'fun': lambda x:  x[4]-x[5]},
			{'type': 'eq', 'fun': lambda x:  x[5]-x[6]},
			{'type': 'eq', 'fun': lambda x:  x[6]-x[7]},

			# [a,a,a,a,lam,lam,mu,mu,b,b,b,b]
			#knots 8-11 are same a
	        {'type': 'eq', 'fun': lambda x:  x[8]-a},
	        {'type': 'eq', 'fun': lambda x:  x[8]-x[9]},
	        {'type': 'eq', 'fun': lambda x:  x[9]-x[10]},
	        {'type': 'eq', 'fun': lambda x:  x[10]-x[11]},

	        #knots 12-13 are same lam
	        {'type': 'eq', 'fun': lambda x:  x[12]-x[13]},

	        #knots 14-15 are same mu
	        {'type': 'eq', 'fun': lambda x:  x[14]-x[15]},

	        #knots 16-19 are same b
	        {'type': 'eq', 'fun': lambda x:  x[16]-b},
	        {'type': 'eq', 'fun': lambda x:  x[16]-x[17]},
	        {'type': 'eq', 'fun': lambda x:  x[17]-x[18]},
	        {'type': 'eq', 'fun': lambda x:  x[18]-x[19]},

	        # lam-a >=0
   	    	{'type': 'ineq', 'fun': lambda x:  x[12]-a},

    	    # k1+lam-mu >=0
    	    {'type': 'ineq', 'fun': lambda x:  k1+x[14]-x[12]},

    	    # b-mu >=0
    	    {'type': 'ineq', 'fun': lambda x:  b-x[14]},

    	    # alp-w/2-1 >=0
    	    {'type': 'ineq', 'fun': lambda x:  x[0] - width_retargettted/2 - 1},

    	    # beta-w/2-1 >=0
    	    {'type': 'ineq', 'fun': lambda x:  x[4] - width_retargettted/2 - 1},

    	    # width-w/2-a >=0
    	    {'type': 'ineq', 'fun': lambda x:  b - width_retargettted/2 - x[0] },

    	    # width-w/2-b >=0
    	    {'type': 'ineq', 'fun': lambda x:  b - width_retargettted/2 - x[4] },

    	    )

	alp = [b/2]*4
	beta = [b/2]*4
	knots = [50,a,a,a,a+100,a+100,a+50,a+50,b,b,b,b]

	x0 = alp+beta+knots
	bnds = [(0, b) for i in range(20)]
	bnds = tuple(bnds)

	#print(BSpline(60,order,x0[8:],x0[:8]))
	#print(BSpline(50,1,[1,50],[1]))

	opt_result  = minimize(objective,x0,method='SLSQP',constraints=cons,bounds=bnds)

	print(opt_result.x)

if __name__ == '__main__':
	main()