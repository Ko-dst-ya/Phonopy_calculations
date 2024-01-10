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
