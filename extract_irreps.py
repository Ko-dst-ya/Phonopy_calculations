def extract_irreps(file_irreps,selected_modes=set(),freq_range=(0,np.inf),freq_units='inv_cm'):
    '''
    This funciton reads irreps.yaml file and gives phonon frequencies with desirable
    irreducible representations in a chosen frequency range
    
    :param file_irreps: name of irreps.yaml file
    :param selected_modes: set of labels to be extracted, e.g.: selected_modes={'Ag'}
    :param freq_range: tuple that stores minimum and maximum frequencies and the function will return only modes from this range
    :param freq_units: units of phonon frequencies in irreps.yaml file
    
    :returns: a tuple of only necessary frequencies (in terms of labels), corresponding labels and indecies of bands
    '''
    with open(file_irreps, 'r') as f:
        data_irreps = yaml.load(f, Loader=yaml.SafeLoader)
        
    modes = data_irreps['normal_modes']
    
    frequency = []
    irrep = []
    band_index = []
    
    # Gathering of all irreducible labels in selected_modes
    if not selected_modes:
        for mode in modes:
            label = mode['ir_label']
            selected_modes.add(label)
    
    for mode in modes:
        if freq_units == 'inv_cm':
            conv_THz_to_inv_cm = 33.35641 # 1 THz = 33.35641 cm^-1            
            freq = mode['frequency'] * conv_THz_to_inv_cm
        elif freq_units == 'THz':
            freq = mode['frequency']
        else:
            raise Exception("Error: Frequency units should be either \'inv_cm\' or \'THz' .");
        label = mode['ir_label']
        index = mode['band_indices']
        if label in selected_modes and freq > freq_range[0] and freq < freq_range[-1]:
            frequency.append(freq)
            irrep.append(label)
            band_index.append(index)
        
    return (frequency,irrep,band_index)
