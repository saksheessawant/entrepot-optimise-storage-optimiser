from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from ortools.linear_solver import pywraplp
import joblib
import pandas as pd
import numpy as np
from .models import VaccantRacks

from itertools import product
vc=[{'category':'A','rackname':'A1-B1-C1','capacity':100},{'category':'B','rackname':'A1-B1-C2','capacity':100}] 

def home1(request):
	return render(request,'calc/home.html')

def home(request):
	df={}
	if request.method=="POST":
		all_vaccantracknames=VaccantRacks.objects.all()
		for i in all_vaccantracknames:
			print(i.category)
		
		# a0=int(request.POST['digit-1'])
		# b0=int(request.POST['digit-2'])
		# c0=int(request.POST['digit-3'])
		# a1=int(request.POST['digit-4'])
		# b1=int(request.POST['digit-5'])
		# c1=int(request.POST['digit-6'])
		name=int(request.POST['name'])
		weights=request.POST['weights']
		

		model=pd.read_pickle('lr_model.pickle')
		weights=list(map(int,weights.split()))
		n=[]
		n.append(name)

		l1=list(product(n, weights))
		print(l1)
		values =str(model.predict(l1))
		print("es",values[1:-1])
		values=values[1:-1]
		print(values)
		values=list(map(float,values.split()))
		if name==0:
			name='Phone'
		elif name==1:
			name='Chairs'
		else:
			name='Kurti'

		A=['Phone', 'Books', 'Printers', 'Electric tiffins']
		B=['Accessories', 'Chairs', 'Electronic Games', 'Hankerchief', 'Shoes', 'Trousers']
		C=['Furnishings', 'Kurti', 'Pillows', 'Shirt', 'Spoons', 'Tables', 'Waterbottles']
		pname=request.POST['name']
		if name in A:
			racks=[i.rackname for i in all_vaccantracknames if i.category=='A']
			print('A rack',racks)
		elif name in B:
			racks=[i.rackname for i in all_vaccantracknames if i.category=='B']
			print('B rack',racks)
		else:
			racks=[i.rackname for i in all_vaccantracknames if i.category=='C']
			print('C rack',racks)
	
		#values=list(map(int,values.split()))
		
		data = {}
		#weights = [48, 30, 42, 36, 36, 42, 42, 36, 24, 30, 30, 36, 36,98,90,10]
		#values = [10, 30, 25, 50, 35, 15, 40, 30, 35, 45, 10, 30, 25,40,45,30]
		data['weights'] = weights
		data['values'] = values
		print(data['weights'],data['values'])
		data['items'] = list(range(len(weights)))
		data['num_items'] = len(weights)
		num_bins = len(racks)
		data['bins'] = list(range(num_bins))
		data['bin_capacities']=[int(i.capacity) for i in all_vaccantracknames if i.rackname in racks]
		
		nbin=[]
		
		nbin=racks#[str(i.rackname) for i in all_vaccantracknames]
		
		ll=list(zip(data['bin_capacities'],nbin))
		print("ll values",ll)
		solver = pywraplp.Solver.CreateSolver('SCIP')
		#print("nbin",nbin)
		x = {}
		for i in data['items']:
			for j in data['bins']:
				x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))
		#print(x)

		for i in data['items']:
			solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
		for j in data['bins']:
			solver.Add(
				sum(x[(i, j)] * data['weights'][i]
					for i in data['items']) <= data['bin_capacities'][j])
		objective = solver.Objective()
		for i in data['items']:
			for j in data['bins']:
				objective.SetCoefficient(x[(i, j)], data['values'][i])
		objective.SetMaximization()
		status = solver.Solve()
		if status == pywraplp.Solver.OPTIMAL:
			df={}
			total_weight = 0
			for j in data['bins']:
				subd={}
				bin_weight = 0
				bin_value = 0
				subd['bin']=nbin[j]
				#print('Bin ', nbin[j], '\n')
				t=[]
				for i in data['items']:
					#print(x[i,j].solution_value(),"xxxx")
					if x[i, j].solution_value() > 0:
						t.append(i)
						print('Item', i, '- weight:', data['weights'][i], ' value:',data['values'][i])
						bin_weight += data['weights'][i]
						bin_value += data['values'][i]
				subd['items']=t
				subd['packedwt']=bin_weight
				subd['packedval']=bin_value
				#print('Packed bin weight:', bin_weight)
				#print('Packed bin value:', bin_value)
				#print()
				total_weight += bin_weight
				if(bin_weight!=0):
					df[j+1]=subd
			#df[0]=[int(objective.Value()),total_weight]
		#content={'total_prof':int(objective.Value()),'total_weight':total_weight}     
		# for i in df.values():
		# 	r=VaccantRacks.objects.get(rackname=i['bins'])
		# 	cap=r.capacity-bin_weight
		# 	VaccantRacks.objects.filter(rackname=i['bins']).update(capacity=cap)
		print(df)
		print("=========")
		
		for i in df.values():
			t = VaccantRacks.objects.get(rackname=i['bin'])
			print(t.capacity,"TTTT",i['packedwt'])
			t.capacity =t.capacity-i['packedwt']
			t.save()
		
		
		  # change field
			



	text="This is my text"
	# a=10
	# b=10
	# a=a+b
	content={
	 't':text,
	 'cal':10,
	}

	return render(request,'calc/index.html',{'d0':df,'d1':content,'d2':['sas','asda','asfd']})






def index(request):
	if request.method=="POST":
		weight=request.POST['weights']
	return HttpResponse("d")

"""def button(request):
	return render(request,'calc/index.html')
def output(request):
	data=requests.get("https://www.google.com/")
	print(data.text)
	data=data.text
	return render(request,'calc/index.html',{'data':data})
def external(request):
	inp= request.POST.get('param')
	out= run([sys.executable,'C://Te proj//entripot//calc//tp.py',inp,"args1","args2"],shell=False,stdout=PIPE)
	print(out)
	return render(request,'calc/index.html',{'data1':out.stdout})
def button(request):
	return render(request,'calc/index.html')
def output(request):
	data=requests.get("https://www.google.com/")
	print(data.text)
	data=data.text
	return render(request,'calc/index.html',{'data':data})"""

