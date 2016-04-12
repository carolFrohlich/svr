import os
import glob
import nibabel as nb
import numpy as np
from sklearn.svm import SVR



#mask = '/home/caroline/Documents/projects/vienna_project/data/mask/invert_1.nii.gz'
#label = '/home/caroline/Documents/projects/vienna_project/data/participant004/OHSU_0050142_func_minimal_label_1.1D'


def load_dataset(dataset,roi):
    dirs = dataset.split('/')
    scan = dirs[-1].split('.')[0]
    participant = dirs[-2]

    data = np.array([])
    labels = np.array([])
    func = nb.load(dataset).get_data()
    func = np.reshape(func, (np.prod(func.shape[0:3]), func.shape[3]))

    mask = os.path.join(path,'mask','invert_'+str(roi)+'.nii.gz')
    mask = nb.load(mask).get_data()

    #mask data
    mask = np.reshape(mask, (np.prod(mask.shape[0:3]), 1))
    masked_func = func[np.where(mask != 0)[0], : ]

    #fix func so sklear can parse data
    masked_func = np.swapaxes(func,0,1)

    return masked_func

def load_train_data(dataset,roi):

    dirs = dataset.split('/')
    scan = dirs[-1].split('.')[0]
    participant = dirs[-2]

    label = os.path.join(path,participant,scan+'_label_'+str(roi)+'.1D')
    if not os.path.exists(label):
        return

    #load data
    label = np.loadtxt(label)
    masked_func = load_dataset(dataset,roi)
    
    return masked_func, label

def predict(dataset):
    all_ds = glob.glob(dataset+'*.nii.gz')
    for train in all_ds:
        dirs = train.split('/')
        scan1 = dirs[-1].split('.')[0]
        participant = dirs[-2]

        data, labels = load_train_data(train,1)
        clf = SVR(C=100.0, epsilon=0.001)
        clf.fit(data, labels)

        for test in all_ds:
            if test != train:
                dirs = test.split('/')
                scan2 = dirs[-1].split('.')[0]
                test_data = load_dataset(test,1)
                prediction = clf.predict(test_data)

                p_path = os.path.join(path,participant,scan1+'_'+scan2+'_prediction.1D')
                np.savetxt(p_path, prediction)

                print 'save', p_path


path = '/home/caroline/Documents/projects/vienna_project/data/'
dataset_paths = '/home/caroline/Documents/projects/vienna_project/datasets/'

all_datasets = glob.glob(dataset_paths+'participant*/')
for d in all_datasets:
    predict(d)