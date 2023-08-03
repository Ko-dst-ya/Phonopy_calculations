def extract_irreps(file_irreps,selected_modes=set(),freq_range=(0,np.inf)):
    '''
        file_irreps -- name of irreps.yaml file
        selected_modes -- set of labels to be extracted, e.g.: selected_modes={'Ag'}
        freq_range -- tuple that stores minimum and maximum frequencies and the function will return only modes from this range
    
    return: a tuple of only necessary frequencies (in terms of labels) and corresponding labels
    '''
    conv_THz_to_inv_cm = 33.35641 # 1 THz = 33.35641 cm^-1
    
    with open(file_irreps, 'r') as f:
        data_irreps = yaml.load(f, Loader=yaml.SafeLoader)
        
    modes = data_irreps['normal_modes']
    
    frequency = []
    irrep = []
    
    # Gathering of all irreducible labels in selected_modes
    if not selected_modes:
        for mode in modes:
            label = mode['ir_label']
            selected_modes.add(label)
    
    for mode in modes:
        freq = mode['frequency'] * conv_THz_to_inv_cm
        label = mode['ir_label']
        if label in selected_modes and freq > freq_range[0] and freq < freq_range[-1]:
            frequency.append(freq)
            irrep.append(label)
        
    return (frequency,irrep)
