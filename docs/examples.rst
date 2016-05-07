
############
Youtube Examples
############

Here are some videos that are made by MkMov. If you've got an awesome video of netCDF output you've made with MkMov, get in touch and we'll add it to the site! If you do sent in a video, please also send the command you used to make it and a caption, describing  what you've plotted.

------------------------------------
mom5_010 Accent
------------------------------------

Daily SSH from MOM5 0.10 degree global simulation CORENYF forcing, Accent colourmap.

.. raw:: html

    <iframe width="480" height="385" src="https://www.youtube.com/embed/HRmYEOloEjI" frameborder="0" allowfullscreen></iframe>
    

Video was made with....
::
    python mkmov.py 2d --lmask -1e34 --lmask2 0 --lmaskfld --cmap Accent --min -2 --max 2 --x xt --y yt -o /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movieout/mom01v4_ssh_maskgd.mov SSH /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/mom10.ssh_daily.yr*.nc

------------------------------------
mom5_010 Paired
------------------------------------

Daily SSH from MOM5 0.10 degree global simulation CORENYF forcing, Paired colourmap.

.. raw:: html

    <iframe width="480" height="385" src="https://www.youtube.com/embed/AnhczYNSeaE" frameborder="0" allowfullscreen></iframe>

Video was made with....
::
    python mkmov.py 2d --lmask -1e34 --lmask2 0 --lmaskfld --cmap Paired --min -2 --max 2 --x xt --y yt -o /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movieout/mom01v4_ssh_maskgd_Paired.mov SSH /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/mom10.ssh_daily.yr*.nc

------------------------------------
mom5_010_3year_bias_seismic 
------------------------------------

Daily SSH anomalies (from 10 year mean) MOM5 0.10 degree global simulation CORENYF forcing

.. raw:: html

    <iframe width="480" height="385" src="https://www.youtube.com/embed/D31F1TMV40E" frameborder="0" allowfullscreen></iframe>

Video was made with....
::
    #Due to the size of these files, they were made in a few steps…
    #to create the anomaly files
    python mkmov.py 2d --bias time --x xt --y yt -o /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movout2/biastest.mov SSH /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/mom10.ssh_daily.yr10.nc
    python mkmov.py 2d --bias time --x xt --y yt -o /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movout2/biastest_yr11.mov SSH /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/mom10.ssh_daily.yr11.nc
    python mkmov.py 2d --bias time --x xt --y yt -o /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movout2/biastest_yr12.mov SSH /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/mom10.ssh_daily.yr12.nc

    #then to create one movie from the output bias files
    python mkmov.py 2d --lmask -1e34 --lmask2 0 --lmaskfld --x xt --y yt --min -0.8 --max 0.8  --cmap seismic -o /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movout2/ps_mom01v4_3year_bias_gdlmask.mov SSH /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movout2/mkmovTEMPFOL4_biastest/difffiles/mom10.ssh_daily.yr10_diff_00000.nc  /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movout2/mkmovTEMPFOL4_biastest_yr11/difffiles/mom10.ssh_daily.yr11_diff_00000.nc /srv/ccrc/data42/z3457920/RawData/ps_mom01v4/movout2/mkmovTEMPFOL4_biastest_yr12/difffiles/mom10.ssh_daily.yr12_diff_00000.nc

------------------------------------
1_TROPAC01-TRC001_5d_sossheig_Dark2
------------------------------------

.. raw:: html
    
    <iframe width="480" height="385" src="https://www.youtube.com/embed/Ureena85cOU" frameborder="0" allowfullscreen></iframe>

Video was made with....
::
    python mkmov.py 2d sossheig --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_sossheig_Dark2.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/4a.log &


------------------------------------
ORCA025.L75-MJM95-S Accent 
------------------------------------

.. raw:: html
    
    <iframe width="480" height="385" src="https://www.youtube.com/embed/m_fUF21dYd0" frameborder="0" allowfullscreen></iframe>

Video was made with....
::
    python mkmov.py 2d  sossheig --cmap Accent --lmask 0 --min -2.2 --max 1.5 -o /srv/ccrc/data42/z3457920/mkmovmovies4/orca025_Accent.mov /srv/ccrc/data22/z3381502/ORCA025.L75-MJM95-S/*_gridT.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/19.log &

------------------------------------
ORCA025.L75-MJM95-S Dark2
------------------------------------

.. raw:: html
    
    <iframe width="480" height="385" src="https://www.youtube.com/embed/MoC3sUUflko" frameborder="0" allowfullscreen></iframe>

    
Video was made with....
::
    python mkmov.py 2d  sossheig --cmap Dark2 --lmask 0 --min -2.2 --max 1.5 -o /srv/ccrc/data42/z3457920/mkmovmovies4/orca025_Dark2.mov /srv/ccrc/data22/z3381502/ORCA025.L75-MJM95-S/*_gridT.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/18.log &

------------------------------------
ORCA025.L75-MJM95-S Set3
------------------------------------

.. raw:: html
    
    <iframe width="480" height="385" src="https://www.youtube.com/embed/-sNs6zReikk" frameborder="0" allowfullscreen></iframe>
    
Video was made with....
::
    python mkmov.py 2d  sossheig --cmap Set3 --lmask 0 --min -2.2 --max 1.5 -o /srv/ccrc/data42/z3457920/mkmovmovies4/orca025_Set3.mov /srv/ccrc/data22/z3381502/ORCA025.L75-MJM95-S/*_gridT.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/17.log &

--------------------------------------------
MOM6
--------------------------------------------

.. raw:: html
    
    <iframe width="480" height="385" src="https://www.youtube.com/embed/h5UHYOtzci8" frameborder="0" allowfullscreen></iframe>
    
Video was made with....
::
    python mkmov.py 2d PV --fps 10 --fighgt 2.5 --figwth 14  -o  /home/chris/mount_win/mom6/outs/newdim.mov /home/chris/mount_win/mom6/ave_prog__*.nc

--------------------------------------------
cordex24 ERAI01 1d grid T 2D zos
--------------------------------------------
NEMO 0.25 degree CORDEX, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://www.youtube.com/embed/tbzIl54c2Ys" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d zos --min -1 --max 1 --lmask 0  -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_zos.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/7.log &
  
--------------------------------------------
AVISOdt global allsat madt
--------------------------------------------
AVISO global allsat madt, output is daily and variable is adt.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/Ai2bW3ID2tU" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d adt --lmask -214748 -o /srv/ccrc/data42/z3457920/mkmovmovies4/AVISOdt_global_allsat_madt.mov /srv/ccrc/data42/z3457920/RawData/AVISO/RawData/dt_global_allsat_madt/ftp.aviso.altimetry.fr/global/delayed-time/grids/madt/all-sat-merged/h/*/*.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/14.log &
  
--------------------------------------------
1 cordex24 AGRIF ERAI09 1d grid T 2D zos
--------------------------------------------
NEMO AGRIF 0.08 degree with daily output, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/DNgha-PJnYM" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d zos --min -1 --max 1 --lmask 0 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_cordex24_AGRIF-ERAI09_1d_grid_T_2D_zos.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_AGRIF_ERAI09/*/1_cordex24_AGRIF-ERAI09_1d_*grid_T_2D.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/13.log &
  
--------------------------------------------
AVISOdt global allsat madt Set3
--------------------------------------------
AVISO global allsat madt, output is daily and variable is adt.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/JEMj05o-KA4" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d adt --lmask -214748 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/AVISOdt_global_allsat_madt_Set3.mov /srv/ccrc/data42/z3457920/RawData/AVISO/RawData/dt_global_allsat_madt/ftp.aviso.altimetry.fr/global/delayed-time/grids/madt/all-sat-merged/h/*/*.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/15.log &
  
--------------------------------------------
cordex24 ERAI01 1d grid T 2D zos Set3
--------------------------------------------
NEMO 0.25 degree CORDEX domain with daily output, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/zjAF1Uig0rI" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d zos --min -1 --max 1 --lmask 0 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_zos_Set3.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/5.log &
  
--------------------------------------------
AVISOdt global allsat madt Dark2
--------------------------------------------
AVISO global allsat madt, output is daily and variable is adt.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/MGmun26XrDg" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d adt --lmask -214748 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/AVISOdt_global_allsat_madt_Dark2.mov /srv/ccrc/data42/z3457920/RawData/AVISO/RawData/dt_global_allsat_madt/ftp.aviso.altimetry.fr/global/delayed-time/grids/madt/all-sat-merged/h/*/*.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/16.log &
  
--------------------------------------------
cordex24 ERAI01 1d grid T 2D zos Dark2
--------------------------------------------
NEMO 0.25 degree CORDEX domain with daily output, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/hyMENGrVUUM" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d zos --min -1 --max 1 --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_zos_Dark2.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/6.log &

  
--------------------------------------------
1 cordex24 AGRIF ERAI09 1d grid T 2D zos Set3
--------------------------------------------
NEMO AGRIF 0.08 degree with daily output, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/cxUNvOdoZTY" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d zos --min -1 --max 1 --lmask 0 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_cordex24_AGRIF-ERAI09_1d_grid_T_2D_zos_Set3.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_AGRIF_ERAI09/*/1_cordex24_AGRIF-ERAI09_1d_*grid_T_2D.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/12.log &
  
--------------------------------------------
cordex24 ERAI01 1d grid T 2D tos
--------------------------------------------
NEMO 0.25 degree CORDEX domain with daily output, variable is temperature.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/lmFzKkF-GDo" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d tos --lmask 0  -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_tos.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/8.log &

--------------------------------------------
cordex24 ERAI01 1d grid T 2D tos Set3
--------------------------------------------
NEMO 0.25 degree CORDEX domain with daily output, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/VqpElu3tMqQ" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d tos --lmask 0 --cmap Set3  -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_tos_Set3.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/9.log &
  
-----------------------------------------------
1 cordex24 AGRIF ERAI09 1d grid T 2D zos Dark2
-----------------------------------------------
NEMO AGRIF 0.08 degree with daily output, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/g5ZHcE35kHk" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d zos  --min -1 --max 1 --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_cordex24_AGRIF-ERAI09_1d_grid_T_2D_zos_Dark2.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_AGRIF_ERAI09/*/1_cordex24_AGRIF-ERAI09_1d_*grid_T_2D.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/11.log &
  
--------------------------------------------
1 TROPAC01 TRC001 5d sossheig Paired
--------------------------------------------
NEMO 0.10 degree with deaily output, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/gWwbvX5yC8U" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d sossheig --lmask 0 --cmap Paired -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_sossheig_Paired.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/4a.log &
  
--------------------------------------------
1 TROPAC01 TRC001 5d sossheig Set3
--------------------------------------------
NEMO 0.10 degree with deaily output, variable is sea surface height.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/SL8rtyvU2ZY" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d sossheig --lmask 0 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/1_TROPAC01-TRC001_5d_sossheig_Set3.mov /srv/ccrc/data42/z3457920/RawData/NEMO/TROPAC01-TRC001/perday/1_TROPAC01-TRC001_5d_*T.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/4.log &
  
--------------------------------------------
cordex24 ERAI01 1d grid T 2D tos Dark2
--------------------------------------------
NEMO 0.25 degree CORDEX domain with daily output, variable is temperature.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/2hKAN4wh51k" frameborder="0" allowfullscreen></iframe>

Single line command this video was made with:
::
    python mkmov.py 2d tos --lmask 0 --cmap Dark2 -o /srv/ccrc/data42/z3457920/mkmovmovies4/cordex24-ERAI01_1d_grid_T_2D_tos_Dark2.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc &> /srv/ccrc/data42/z3457920/mkmovmovies4/10.log &

--------------------------------------------
Acknowledgements
--------------------------------------------
The altimeter products were produced by Ssalto/Duacs and distributed by Aviso with support from Cnes.

TROPAC01 was developed in the ocean modelling group of GEOMAR, Kiel (Germany) with support by the DFG project SFB754 and integrated at the North-German Supercomputing Alliance (HLRN).
