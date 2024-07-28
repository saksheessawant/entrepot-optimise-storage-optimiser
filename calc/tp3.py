from ortools.linear_solver import pywraplp


def create_data_model():
    """Create the data for the example."""
    data = {}
    weights = [48, 30, 42, 36, 36, 42, 42, 36, 24, 30, 30, 36, 36,98,90,10]
    values = [10, 30, 25, 50, 35, 15, 40, 30, 35, 45, 10, 30, 25,40,45,30]
    data['weights'] = weights
    data['values'] = values
    data['items'] = list(range(len(weights)))
    data['num_items'] = len(weights)
    num_bins = 125
    data['bins'] = list(range(num_bins))
    data['bin_capacities'] = [100 for i in range(126)] #[A0-C0-R0,A0-C0-R1...]
    return data



def main():
    data = create_data_model()

    nbin=[]
    for a in range(1,6):
        for c in range(1,6):
            for r in range(1,6):
                s=''
                s+='A'+str(a)+'-C'+str(c)+'-R'+str(r)
                nbin.append(s)
    #print(data['bin_capacities'])

    ll=list(zip(data['bin_capacities'],nbin))
    #print(ll)

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    print("nbin",nbin)

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    objective = solver.Objective()

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        df={}
        #print('Total packed value:', objective.Value())
        total_weight = 0
        for j in data['bins']:
            subd={}
            bin_weight = 0
            bin_value = 0
            subd['bin']=nbin[j]
            #print('Bin ', nbin[j], '\n')
            t=[]
            for i in data['items']:       
                if x[i, j].solution_value() > 0:
                    t.append(i)
                    #print('Item', i, '- weight:', data['weights'][i], ' value:',data['values'][i])
                    bin_weight += data['weights'][i]
                    bin_value += data['values'][i]
            subd['items']=t
            subd['packed wt']=bin_weight
            subd['packed val']=bin_value
            #print('Packed bin weight:', bin_weight)
            #print('Packed bin value:', bin_value)
            #print()
            total_weight += bin_weight
            if(bin_weight!=0):
                df[j+1]=subd
        #print('Total packed weight:', total_weight)
        df[0]=[int(objective.Value()),total_weight]
        print("==================================================================",df)        
    else:
        print('The problem does not have an optimal solution.')
    
if __name__ == '__main__':
    main()
