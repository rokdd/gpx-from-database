



from gpx_from_database import *
from importlib import import_module
import os

try:
    from settings import *
except ImportError:
	print("You should copy defaultSettings.py to settings.py and adapt to your needs")
	os.abort()

if __name__=="__main__":
	timestamp_start=datetime.today()
	timestamp_end=datetime.today()
	timestamp_start=datetime(2022,1,21)
	timestamp_end=datetime(2022,1,23)


	core.plan(CONFIG)
	core.job_export_total(timestamp_start,timestamp_end)
	core.job_export_daily(timestamp_start,timestamp_end)
	core.run()