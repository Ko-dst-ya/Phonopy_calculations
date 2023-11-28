eps_folder = parent + 'eps/'
os.chdir(eps_folder)

files = (file for file in os.listdir(eps_folder) 
    if os.path.isfile(os.path.join(eps_folder, file)))

raman_vasp = []

# Gathering vasp files for epsilon calcs
for file in files:
    if file[-4:] == 'vasp':
        raman_vasp.append(file)

# Make dirs 0***_00*
for file in raman_vasp:
    raman_poscar_filename = file.split('.')
    band_index = raman_poscar_filename[1]
    displ = raman_poscar_filename[2]
    
    if not os.path.exists(f'{band_index}_{displ}/'):
        os.mkdir(f'{band_index}_{displ}/')

# Scattering of all Raman-POSCAR.0***.00*.vasp files
# to 0***_00* folders with renaming to just POSCAR
os.chdir(eps_folder)

for file in raman_vasp:
    raman_poscar_filename = file.split('.')
    band_index = raman_poscar_filename[1]
    displ = raman_poscar_filename[2]
    
    if os.path.exists(file):
        shutil.move(file, f'{band_index}_{displ}/POSCAR')

os.chdir(eps_folder)

for file in raman_vasp:
    raman_poscar_filename = file.split('.')
    band_index = raman_poscar_filename[1]
    displ = raman_poscar_filename[2]
    
    shutil.copy('INCAR', f'{band_index}_{displ}/')
    shutil.copy('jobscript', f'{band_index}_{displ}/')
    shutil.copy('POTCAR', f'{band_index}_{displ}/')
    
    os.chdir(f'{band_index}_{displ}/')

    with open('jobscript', 'r') as job:
        old = job.read()
    new = old.replace('#SBATCH -J eps_calc', f'#SBATCH -J {band_index}.{displ}')
    with open('jobscript', 'w') as job:
        job.write(new)
    
    os.chdir(eps_folder)


# Sbatch block 
os.chdir(eps_folder)

for file in raman_vasp:
    raman_poscar_filename = file.split('.')
    band_index = raman_poscar_filename[1]
    displ = raman_poscar_filename[2]
   
    os.chdir(f'{band_index}_{displ}/')
    
    os.system('sbatch jobscript')
    os.chdir(eps_folder)
