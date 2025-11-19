import os
import glob
import logging
from dotenv import load_dotenv
load_dotenv()

class Obj:
    """
        Abstract Object
    """

app = Obj()

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

LOG_DIRPATH = os.getenv('LOG_DIRPATH')  if os.getenv('LOG_DIRPATH')  else  os.path.join(ROOT_PATH, 'logs')
os.makedirs(LOG_DIRPATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIRPATH, 'activity.log')
logging.basicConfig(
    level=logging.INFO, # 設定日誌級別
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', # 設定格式
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode='a'), # 寫入到 'logs/app.log'
        logging.StreamHandler() # 同時也輸出到終端機
    ]
)

logger = logging.getLogger()
TIFF_PATHS = []
if tif_dir := os.getenv('TIF_DIRPATH'):
    TIFF_PATHS = glob.glob(os.path.join(tif_dir, '*.tif')) + glob.glob(os.path.join(tif_dir, '*.tiff'))
    
WORKFLOWS = {
    "tif": {
        "path":"utils.workflow",
        "name":"WorkflowTIF"
    }
}

OUTPUT_DIR = os.getenv('OUTPUT_DIR')  if os.getenv('OUTPUT_DIR')  else  os.path.join(ROOT_PATH, 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

VALIDATE_DIST_KM = os.getenv('VALIDATE_DIST_KM')  if os.getenv('VALIDATE_DIST_KM')  else 0.1
FIND_MATCH_ONLY = os.getenv('FIND_MATCH_ONLY')  if os.getenv('FIND_MATCH_ONLY')  else False

TARGET_SPOT_LON = os.getenv('TARGET_SPOT_LON')  if os.getenv('TARGET_SPOT_LON')  else 121.858688
TARGET_SPOT_LAT = os.getenv('TARGET_SPOT_LAT')  if os.getenv('TARGET_SPOT_LAT')  else 24.920176