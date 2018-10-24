import fire
import pandas as pd
from glob import glob

def create_manifest(dir, name):
    fns = sorted(glob(dir + '/*.jpeg'))
    s = pd.Series(fns, name='fn')
    s.to_csv(dir + name, header=True, index_label='id')

if __name__ == '__main__':
    fire.Fire(create_manifest)
