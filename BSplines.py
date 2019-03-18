
def Bezier(t,idx,order,knots):


	if(order == 1):

		if(t >= knots[idx] and t< knots[idx+1]):
			return 1;
		else:
			return 0

	Bz = Bezier(t,idx,order-1,knots)

	if( Bz==0 or knots[idx]==knots[idx+1]):
		part1 = 0
	else:
		part1 = (t - knots[idx])*Bz/(knots[idx+1]-knots[idx])

	Bz = Bezier(t,idx+1,order-1,knots)

	if(Bz == 0 or knots[idx+order+1]==knots[idx+1]):
		part2 = 0
	else:
		part2 = (knots[idx+order+1] - t )*Bz/(knots[idx+order+1]-knots[idx+1]) 

	return part1 + part2

def BSpline(t,order,knots,control_points):

	nK = len(knots)
	nCP = len(control_points)

	if nK != nCP+ order:
		print("Error in number of parameters nK:%d , nCP: %d, order:%d "%(nK,nCP,order))

	knots.sort()

	idx = -1

	for i,val in enumerate(knots):
		if(t<val):
			idx = i-1
			break
	
	if idx == -1:
		return 0;
	if(idx >= len(control_points)):
		curve_segmentQ=0
	else:
		for i in range(order):
			#print(idx,i,idx-i)
			curve_segmentQ = control_points[idx-i]*Bezier(t,idx-i,order,knots)

	return curve_segmentQ

if __name__ == '__main__':
	main()