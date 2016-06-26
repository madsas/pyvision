run('add_paths.m');
addpath(genpath('/home/vision/Sasi/matlab/code/projects/electrical_stim/scripts'));

%PARAMETERS--------------------
dataPath = '/Volumes/Analysis/2016-04-21-6/data001/data001';
foo = strsplit(dataPath,'/');
saveName = ['eimat_' foo{4} '.mat'];

loadflg = 1;
if loadflg 
	%Read in data (probably only works on Mac)
	datarun  = load_data(dataPath);
	datarun  = load_neurons(datarun);
	datarun  = load_sta(datarun, 'load_sta', 'all');
	datarun  = load_params(datarun);
	datarun  = load_ei(datarun, 'all');
end

%get and reshape EI data
[allEIs, eimat, minVals, minElecs] = getEiData(datarun);
x = datarun.cell_ids;
save(saveName, 'allEIs', 'x')
