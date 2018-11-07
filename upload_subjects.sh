#!/usr/bin/env bash


python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region1_DJF_Aqua Region1_DJF_Aqua &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region1_DJF_Terra Region1_DJF_Terra &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region1_MAM_Aqua Region1_MAM_Aqua &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region1_MAM_Terra Region1_MAM_Terra &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region2_DJF_Aqua Region2_DJF_Aqua &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region2_DJF_Terra Region2_DJF_Terra &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region3_DJF_Aqua Region3_DJF_Aqua &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region3_DJF_Terra Region3_DJF_Terra &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region3_SON_Aqua Region3_SON_Aqua &&
python create_manifest.py /project/meteo/work/S.Rasp/cloud-classification/Region3_SON_Terra Region3_SON_Terra

panoptes subject-set create 7699 'Region1_DJF_Aqua' &&
panoptes subject-set create 7699 'Region1_DJF_Terra' &&
panoptes subject-set create 7699 'Region1_MAM_Aqua' &&
panoptes subject-set create 7699 'Region1_MAM_Terra' &&
panoptes subject-set create 7699 'Region2_DJF_Aqua' &&
panoptes subject-set create 7699 'Region2_DJF_Terra' &&
panoptes subject-set create 7699 'Region3_DJF_Aqua' &&
panoptes subject-set create 7699 'Region3_DJF_Terra' &&
panoptes subject-set create 7699 'Region3_SON_Aqua' &&
panoptes subject-set create 7699 'Region3_SON_Terra'


panoptes subject-set upload-subjects 60811 /project/meteo/work/S.Rasp/cloud-classification/Region1_DJF_Aqua/Region1_DJF_Aqua.csv &&
panoptes subject-set upload-subjects 60812 /project/meteo/work/S.Rasp/cloud-classification/Region1_DJF_Terra/Region1_DJF_Terra.csv &&
panoptes subject-set upload-subjects 60813 /project/meteo/work/S.Rasp/cloud-classification/Region1_MAM_Aqua/Region1_MAM_Aqua.csv &&
panoptes subject-set upload-subjects 60814 /project/meteo/work/S.Rasp/cloud-classification/Region1_MAM_Terra/Region1_MAM_Terra.csv &&
panoptes subject-set upload-subjects 60815 /project/meteo/work/S.Rasp/cloud-classification/Region2_DJF_Aqua/Region2_DJF_Aqua.csv &&
panoptes subject-set upload-subjects 60816 /project/meteo/work/S.Rasp/cloud-classification/Region2_DJF_Terra/Region2_DJF_Terra.csv &&
panoptes subject-set upload-subjects 60817 /project/meteo/work/S.Rasp/cloud-classification/Region3_DJF_Aqua/Region3_DJF_Aqua.csv &&
panoptes subject-set upload-subjects 60818 /project/meteo/work/S.Rasp/cloud-classification/Region3_DJF_Terra/Region3_DJF_Terra.csv &&
panoptes subject-set upload-subjects 60819 /project/meteo/work/S.Rasp/cloud-classification/Region3_SON_Aqua/Region3_SON_Aqua.csv &&
panoptes subject-set upload-subjects 60820 /project/meteo/work/S.Rasp/cloud-classification/Region3_SON_Terra/Region3_SON_Terra.csv
