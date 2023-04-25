import socket
from inspect import getsourcefile
from pathlib import Path

if socket.gethostname() == "gecko":
    ucr_archive_dir = Path("/media/m4_datasets/datasets/UCRArchive_2018")
    dataset_dir = ucr_archive_dir.parent
    figure_root_dir = Path("/media/tsagg_figs/")
else:
    raise ValueError(f"Unknown hostname: {socket.gethostname()}")


loc_data_dir = Path(getsourcefile(lambda: 0)).absolute().parent.parent / "loc_data"

# use the socket hosname to determine the path towards:
# * the m4 data
# * ucr archive data
# * the figures
# * the intermediate dataframes
