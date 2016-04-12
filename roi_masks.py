#read mask with nibabel

#foreach roi, 
#   deep copy mask
#   zero all numbers except roi id
#   change number to 1
#   save
import nibabel as nb
from scipy import ndimage
import numpy as np
from copy import deepcopy
import os
import sys


#mask_file = '/home/caroline/Documents/projects/vienna_project/data/ADHD200_parcellate_200.nii.gz'

#for each roi, creates a inverted mask, 
#all voxels are on except the voxels from that mask
#the roi is dilated 2 voxels
def inverted_masks(mask_file):
    path = '/'.join(mask_file.split('/')[:-1])

    mask = nb.load(mask_file)
    data = mask.get_data()
    labels = np.unique(data)[1:]

    for l in labels:
        dil_roi = deepcopy(data)
        inverse_mask = deepcopy(data)

        dil_roi[dil_roi != l] = 0
        dil_roi = ndimage.binary_dilation(dil_roi, iterations=2)

        inverse_mask[inverse_mask != 0] = 444
        inverse_mask = inverse_mask + dil_roi
        inverse_mask[inverse_mask != 444] = 0

        img = nb.Nifti1Image(inverse_mask, mask.affine, header = mask.get_header())

        nb.save(img, os.path.join(path,'invert_'+str(l)+'.nii.gz'))


if __name__ == "__main__":
   inverted_masks(sys.argv[1])
