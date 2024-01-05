from typing import Union
from dslogs.log_entry.pdp_ctre_data import PdpCtreData
from dslogs.log_entry.pdp_rev_pdh_data import PdpRevPdhData

PdpData = Union[PdpCtreData, PdpRevPdhData]
