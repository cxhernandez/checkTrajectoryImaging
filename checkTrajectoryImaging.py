#!/usr/bin/python

import mdtraj as md
import numpy as np
import glob,optparse,os

formats=['arc','binpos','lh5','dcd','hdf5','lh5','mdcrd','netcdf','openmmxml','pdb','prmtop','registry','trr','xtc']

def getIndices(idx,n_atoms):
    x=[]
    if idx is ':':
        return range(n_atoms)
    for i in idx.split(','):
        y = i.split(':')
        if len(y)==1:
            x.append(int(i))
        else:
            x.extend(range(int(y[0]),int(y[1])+1))
    return x

def run(dir,top,ext,err,idx):
    ref = md.load(top)
    atoms= getIndices(idx,ref.n_atoms)
    for i in glob.glob(dir+'/*.'+ext):
        traj= md.load(i,top=top)
        r=md.rmsd(target=traj, reference=ref,atom_indices=atoms)
        p=np.divide(np.abs(r[1:]-r[:-1]),r[:-1])>err
        if True in p:
            print i
        
def parse_cmdln():
    parser=optparse.OptionParser()
    parser.add_option('-d','--directory',dest='dir',type='string', default='.',help='Path to directory containing trajectories')
    parser.add_option('-f','--format',dest='ext',type='string',help='Trajectory format: '+ ', '.join(formats)+'.')
    parser.add_option('-t','--topology',dest='top',type='string',help='Topology file')
    parser.add_option('-e','--error',dest='err',type='float',help='Percent error tolerance', default=0.1)
    parser.add_option('-i','--atom_indices',dest='idx',type='string',help='String list of 0-indexed atomic indices to verify. Selection algebra: use '':'' for ranges and '','' to concatenate ranges', default=':')
    (options, args) = parser.parse_args()
    if not options.top:
        parser.error('Topology file not given.')
    if not options.ext:
        parser.error('Trajectory format not given.')
    if options.ext.lower() not in formats:
        parser.error('%s is not a recognized trajectory format. See help for a full list of acceptable formats.' % options.ext)
    return (options, args)


if __name__ == "__main__":
    (options,args)=parse_cmdln()
    run(options.dir,options.top,options.ext,options.err,options.idx)
