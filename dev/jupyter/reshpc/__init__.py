from .assets import MACHINE, NEWT_BASE_URL, REQUESTS_SESSION
from .ats_interface import ATSWidget
from .ats_runner import ATSRunner
from .nersc_interface import NerscInterface
from .nersc_login import login, _LoginUtility

# Perfrom the login on import
login()
