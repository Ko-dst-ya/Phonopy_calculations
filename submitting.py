def scatter_input_files(folders,curdir=None,files=['INCAR','POTCAR','jobscript']):
    """
    This function aims to scatter files you are interested in
    to folders with displaced structures.

    :param folders: list of folders
    :param files: list of input file names to be scattered
    :param curdir: directory contains folders with displacements
    
    :returns: noting
    """
    if curdir is not None:
        os.chdir(curdir)
        
    incar_file, potcar_file, jobscript_file = None, None, None
    poscar_file, kpoints_file = None, None
    
    # Gathering filenames
    for file in files:
        if file == 'INCAR':
            incar_file = file
        elif file == 'POTCAR':
            potcar_file = file
        elif file == 'jobscript':
            jobscript_file = file
        elif file[:7] == 'POSCAR-':
            poscar_file = file
        elif file == 'KPOINTS':
            kpoints_file = file
    
    for folder in folders:
        shutil.copy(incar_file,folder)
        shutil.copy(potcar_file,folder)
        shutil.copy(jobscript_file,folder)
        
        if kpoints_file:
            shutil.copy(kpoints_file,folder)
            
        if poscar_file:
            shutil.move(poscar_file,folder+'/POSCAR')
            
    
        os.chdir(folder)
        
        with open(jobscript_file, 'r') as job:
            old = job.read()
        new = old.replace('#SBATCH -J jobname',f'#SBATCH -J {folder}')
        with open(jobscript_file, 'w') as job:
            job.write(new)
            
        os.chdir(curdir)


def rename_jobs(folders,curdir=None,jobscript_file='jobscript'):
    """
    This function replaces name of a particular job lacated in `folders`
    with the number of this folder (it is implicitly assumed that all 
    folders are enumerated with unique number)
    
    :param folders: list of folders where jobname should to be modified
    :param curdir: name of current dir
    :param jobname: name of shell job file

    :returns: nothing
    """
    if curdir is not None:
        os.chdir(curdir)
        
    
    for folder in folders:
        os.chdir(folder)
        
        with open(jobscript_file, 'r') as job:
            old = job.read()
        new = old.replace('#SBATCH -J 1',f'#SBATCH -J {folder}')
        with open(jobscript_file, 'w') as job:
            job.write(new)
            
        os.chdir(curdir)


def sbatch_jobs(folders,curdir=os.getcwd(),jobscript_file='jobscript'):
    """
    This function aims to submit a pack of jobs located in `folders` 
    that are loacated in `curdir`
    
    :param folders: folders where jobscript will be submitted
    :param curdir: dir you are interested in (where subfolders is placed)
    :param jobscript_file: name of shell job file

    :returns: nothing
    """
    os.chdir(curdir)
        
    for folder in folders:
        os.chdir(folder)
        os.system(f'sbatch {jobscript_file}')
        os.chdir(curdir)
    
