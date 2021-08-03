import mbfit
import sys

dim_settings = "dimer_settings.ini"
config = "config.ini"
ionPair = sys.argv[1]
mon_ids = ionPair.split("-")

mbnrg_fits_directory = "mb-nrg_fits_overTTM"
MBX_path = "/home/hagnew/codes/MBX-tmp"

mbfit.generate_MBX_files(dim_settings, config, mon_ids, 0,
                                     do_ttmnrg=True,
                                     MBX_HOME = MBX_path, version = "v1")


mbfit.generate_MBX_files(dim_settings, config, mon_ids, 9,
                                     do_ttmnrg=False, mbnrg_fits_path=mbnrg_fits_directory,  
                                     MBX_HOME = MBX_path, version = "v1")