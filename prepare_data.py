from CPAC.alff.alff import get_zscore
import glob
import shutil
import subprocess
import os

def zscore(dataset, roi):
    dirs = dataset.split('/')
    scan = dirs[-1].split('.')[0]
    participant = dirs[-2]

    #calculate z-score
    wf = get_zscore()
    wf.base_dir = working_dir
    wf.inputs.inputspec.input_file = dataset
    wf.inputs.inputspec.mask_file = mask+str(roi)+'.nii.gz'
    wf.run()

    #put z score file on the right place
    z_file = glob.glob(os.path.join(working_dir,'z_score','z_score','*.nii.gz'))[0]
    z_file_dir = os.path.join(outputs,participant)
    if not os.path.exists(z_file_dir):
        os.mkdir(z_file_dir, 0755 )

    os.rename(z_file,os.path.join(z_file_dir,scan+'_zscore_'+str(roi)+'.nii.gz'))
    shutil.rmtree(working_dir)


def calc_zscores(data_dir):
    all_nii = glob.glob(data_dir+'/*/*.nii.gz')

    for dataset in all_nii:
        for i in range(1,200):
            zscore(dataset,i)



def label(dataset,mask,roi):
    # 3dmaskave 
    #-mask data/mask/cc200.nii.gz 
    #-quiet 
    #-mrange 2 2 
    #data/participant004/OHSU_0050143_func_minimal_zscore_1.nii.gz 
    #> out_test.1D
    
    dirs = dataset.split('/')
    scan = dirs[-1].split('zscore')[0]
    participant = dirs[-2]

    afni = subprocess.Popen(["3dmaskave","-quiet","-mask",mask, "-mrange", str(roi), str(roi),dataset],stdout=subprocess.PIPE)
    output = afni.communicate()[0]

    l_name = os.path.join(outputs,participant,scan+'label_'+str(roi)+'.1D')
    with open(l_name,'w') as l_file:
        l_file.write(output)


def calc_labels(data_dir):
    all_nii = glob.glob(data_dir+'/*/*zscore*.nii.gz')
    mask = pwd + 'data/mask/cc200.nii.gz'

    for dataset in all_nii:
        for i in range(1,200):
            label(dataset,mask,i)


pwd = '/home/caroline/Documents/projects/vienna_project/'
mask = pwd+'data/mask/invert_'
working_dir = pwd+'data/working/'
outputs = pwd+'data/'

calc_zscores(pwd+'datasets')
calc_labels(outputs)