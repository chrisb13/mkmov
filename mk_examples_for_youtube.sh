set -x
source activate root
#python mkmov.py votemper --lmask 0 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_votemper.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/1.log &

#python mkmov.py sossheig --lmask 0  --clev 50 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_sossheig.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/2.log &

#python mkmov.py votemper --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_votemper_Dark2.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/3.log &



#python mkmov.py sossheig --lmask 0 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_sossheig_Set3.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/4.log &

#python mkmov.py sossheig --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_sossheig_Dark2.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/4a.log &

#python mkmov.py sossheig --lmask 0 --cmap Paired -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_sossheig_Paired.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/4a.log &

#python mkmov.py zos --min -1 --max 1 --lmask 0 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_zos_Set3.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/5.log &

#python mkmov.py zos --min -1 --max 1 --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_zos_Dark2.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/6.log &

#python mkmov.py zos --min -1 --max 1 --lmask 0  -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_zos.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/7.log &

#python mkmov.py tos --lmask 0  -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_tos.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/8.log &

#python mkmov.py tos --lmask 0 --cmap Set3  -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_tos_Set3.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/9.log &

#python mkmov.py tos --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_tos_Dark2.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/10.log &

#python mkmov.py zos  --min -1 --max 1 --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_cordex24_AGRIF-ERAI09_1d_grid_T_2D_zos_Dark2.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_AGRIF_ERAI09/*/1_cordex24_AGRIF-ERAI09_1d_*grid_T_2D.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/11.log &

#python mkmov.py zos --min -1 --max 1 --lmask 0 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_cordex24_AGRIF-ERAI09_1d_grid_T_2D_zos_Set3.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_AGRIF_ERAI09/*/1_cordex24_AGRIF-ERAI09_1d_*grid_T_2D.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/12.log &

#python mkmov.py zos --min -1 --max 1 --lmask 0 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_cordex24_AGRIF-ERAI09_1d_grid_T_2D_zos.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_AGRIF_ERAI09/*/1_cordex24_AGRIF-ERAI09_1d_*grid_T_2D.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/13.log &

#python mkmov.py adt --lmask -214748 -o /srv/ccrc/data42/z3457920/mkmovmovies4/AVISOdt_global_allsat_madt.mov /srv/ccrc/data42/z3457920/RawData/AVISO/RawData/dt_global_allsat_madt/ftp.aviso.altimetry.fr/global/delayed-time/grids/madt/all-sat-merged/h/*/*.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/14.log &

#python mkmov.py adt --lmask -214748 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/AVISOdt_global_allsat_madt_Set3.mov /srv/ccrc/data42/z3457920/RawData/AVISO/RawData/dt_global_allsat_madt/ftp.aviso.altimetry.fr/global/delayed-time/grids/madt/all-sat-merged/h/*/*.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/15.log &

#python mkmov.py adt --lmask -214748 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/AVISOdt_global_allsat_madt_Dark2.mov /srv/ccrc/data42/z3457920/RawData/AVISO/RawData/dt_global_allsat_madt/ftp.aviso.altimetry.fr/global/delayed-time/grids/madt/all-sat-merged/h/*/*.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/16.log &

python mkmov.py  sossheig --cmap Set3 --lmask 0 --min -2.2 --max 1.5 -o /srv/ccrc/data42/z3457920/mkmovmovies4/orca025_Set3.mov /srv/ccrc/data22/z3381502/ORCA025.L75-MJM95-S/*_gridT.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/17.log &
python mkmov.py  sossheig --cmap Dark2 --lmask 0 --min -2.2 --max 1.5 -o /srv/ccrc/data42/z3457920/mkmovmovies4/orca025_Dark2.mov /srv/ccrc/data22/z3381502/ORCA025.L75-MJM95-S/*_gridT.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/18.log &
python mkmov.py  sossheig --cmap Accent --lmask 0 --min -2.2 --max 1.5 -o /srv/ccrc/data42/z3457920/mkmovmovies4/orca025_Accent.mov /srv/ccrc/data22/z3381502/ORCA025.L75-MJM95-S/*_gridT.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/19.log &
