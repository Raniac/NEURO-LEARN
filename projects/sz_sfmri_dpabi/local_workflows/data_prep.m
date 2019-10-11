%Calculate the regional gray matter volume by the specific atlas (e.g.,
%AAL-90 or AAL-1024)
clear;
% current_dir=pwd;
% input_dir=[current_dir '/Test'];
% Input should be resliced. Input dir follow the order: ALFF, ReHo, GMV.
input_dir={'H:\kly_data\task_191010\Resliced\Reslice_ALFF_FunImgARCWS',...
    'H:\kly_data\task_191010\Resliced\Reslice_ReHo_FunImgARCW',...
    'H:\kly_data\task_191010\Resliced\Reslice_mwc1'};
FC_dir='H:\kly_data\task_191010\Analysis\Results\ROISignals_FunImgARCWSF'; % extract DC:用ARCWSF,文件要用ROICorrelation_FisherZ开头的
ID_len = 10; % how many chars is the ID str
save_name = 'H:\kly_data\task_191010\ARGD_90.csv';

% extract ALFF, ReHo, GMV
res = [];
for fea = 1:length(input_dir)
    filelist_input=dir( [input_dir{fea} '\' '*.nii']);
    numFiles=size(filelist_input,1);  %include two directories '.' and '..'
    
    % AAL-90
    V90 = spm_vol(['H:\brain_soft\ROI\AAL_PANDA_2MM\AAL_Contract_90_2MM.nii']);
    Data90 = spm_read_vols(V90);
    T=reshape(Data90,91*109*91,1);   %voxelsize=[2 2 2]
    T2=unique(T);   %T2(1)=0; T2(2-1025)--> the values of 1024-AAL regions
    nAAL=size(T2,1)-1;
    
    % %AAL-1024
    % V1024 = spm_vol(['I:\WuStudy_SZ_151014\151109_T1_ROI\00_Cal_RGMV\AAL_PANDA_2MM\' 'AAL_Contract_1024_2MM_7.nii']);
    % Data1024 = spm_read_vols(V1024);
    % T=reshape(Data1024,91*109*91,1);   %voxelsize=[2 2 2]
    % T2=unique(T);   %T2(1)=0; T2(2-1025)--> the values of 1024-AAL regions
    % nAAL=size(T2,1)-1;
    
    for iFile=1:numFiles
        
        Result.FileName(iFile,1)= {filelist_input(iFile,1).name};
        
        inputFile=[input_dir{fea} '\' filelist_input(iFile,1).name];
        Input=spm_read_vols(spm_vol(inputFile));
        
        for i=1:nAAL
            record=['Current subject is ' num2str(iFile) '; current ROI is ' num2str(i) '!']
            
            ROI=zeros(91,109,91);
            
            %AAL-90
            %           ROI(find(Data90==T2(i+1))) = 1;
            ROI(find(Data90==i)) = 1;
            Result.size_ROI(i, iFile)=size(find(ROI),1);
            
            %AAL-1024
            % %           ROI(find(Data1024==T2(i+1))) = 1;
            %            ROI(find(Data1024==i)) = 1;
            %            Result.size_ROI(i, iFile)=size(find(ROI),1);
            
            rgmv = ROI .* Input;
            Result.size_rgmv(i, iFile)=size(find(rgmv),1);    %whether 151 voxels (each ROI in AAL-1024) left in the ROI of the input image
            Result.RGMV(i, iFile)= sum(rgmv(find(rgmv)))/size(find(ROI),1);
        end;
    end;
    rgmv = Result.RGMV';
    res = [res, rgmv];
end
FileName = Result.FileName;


% extract DC
file_list=dir([FC_dir '/ROICorrelation_FisherZ_*.mat']);
num_dir=size(file_list,1);

for i=1:num_dir
    if size(file_list(i,1).name,2)>2
        work_file = [FC_dir '/' file_list(i,1).name];
        load(work_file);
        mat = abs(ROICorrelation_FisherZ);
        mat = mat(1:90,1:90);  %AAL Altas in dpabi is 116 ROIs
        for j=1:length(mat)  %set diagonal to 0 because all diagonal equal to 'inf'
            mat(j,j)=0;
        end
        for k=1:length(mat)
            DC(i,k)=sum(mat(k,:));
        end
    end
end
res = [res, DC];
res = [zeros(length(FileName),2)*nan, res]; % two nan rows for label and score

% build the table
%index
index ={};
for i = 1:numFiles
    index{i,1} = num2str(i);
end
ID = {};
for i = 1:length(FileName)
    ID{i,1} = FileName{i}(1:ID_len);
end
Tid = table(ID,...
    'VariableNames',{'ID'},...
    'RowNames' ,index);

ROI_num = length(mat);
variable={'LABEL_GROUP' 'LABEL_SCORE'};
for i = 1:ROI_num
    variable{2 + i} = ['ALFF_' int2str(i)];
end
for i = 1:ROI_num
    variable{2 + ROI_num + i} = ['ReHo_' int2str(i)];
end
for i = 1:ROI_num
    variable{2 + ROI_num*2 + i} = ['GMV_' int2str(i)];
end
for i = 1:ROI_num
    variable{2 + ROI_num*3 + i} = ['DC_' int2str(i)];
end
Tfea = array2table(res,...
    'VariableNames',variable,...
    'RowNames' ,index);
T = join(Tid,Tfea,'Keys','Row');
writetable(T,save_name,'Delimiter',',')
