def boarders_for_epsilon(vasprun_file):
    '''
    Find boarders for density-density and current-current 
    frequency dependent dielectric function
    inside a given vasprun.xml file
    Boarders mean the starting and ending number of lines
    for frequency dependent epsilon. In other words
    
    The first line is followed by <set>:
    
    <set>
    <r>     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000     0.0000 </r>
    
    The </set> is followed by the last line:
    
    <r>    40.4672     0.0001     0.0001     0.0001    -0.0000     0.0000     0.0000 </r>
     </set>

    
    vasprun_file - string name of vasprun.xml file
    '''
    boarders = {'real': {'dd':[0,0],
                         'cc':[0,0]},
                'imag': {'dd':[0,0],
                         'cc':[0,0]}}
    
    count = 0

    with open(vasprun_file,'r') as f:
        for line in f:
            count +=1 

            if 'density-density' in line:
                kind_of_approximation = 'dd'
            elif 'current-current' in line:
                kind_of_approximation = 'cc'

            for part_of_eps in ['real','imag']:
                if f'<{part_of_eps}>' in line:
                    boarders[part_of_eps][kind_of_approximation][0] = count+10
                elif f'</{part_of_eps}>' in line:
                    boarders[part_of_eps][kind_of_approximation][-1] = count-2
    
    return boarders


def read_epsilon(file):
  '''
  file -- vasprun.xml file containing real and imaginary parts of epsilon of hv
  '''
    with open(file,'r') as f:
        epsilon = f.readlines()
    epsilon = [e.split() for e in epsilon]

    hv, eps_of_hv = [0 for _ in range(len(epsilon))], [[] for _ in range(len(epsilon))]
    for i,e_eps in enumerate(epsilon):
        hv[i] = float(e_eps[1])
        eps_of_hv[i] = [float(elem) for elem in e_eps[2:-1]]

    diel_function = []
    for eps in eps_of_hv:
        diel_function.append((eps[0]+eps[1]+eps[2])/3)
        
    return hv, diel_function
