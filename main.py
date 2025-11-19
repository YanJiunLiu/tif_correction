import os
from utils.decorators import workflow
from configs.settings import (
    app, 
    TIFF_PATHS, 
    OUTPUT_DIR, 
    TARGET_SPOT_LON,
    TARGET_SPOT_LAT,
    VALIDATE_DIST_KM, 
    FIND_MATCH_ONLY
)
from utils.distutil import strtobool

@workflow('tif')
def run_tif(app):
    print(f"Starting TIF workflow processing...{TIFF_PATHS}")
    for tif_path in TIFF_PATHS:
        filename = os.path.splitext(os.path.basename(tif_path))[0]
        app.workflow.initial_data()
        app.workflow.choose_aim_point(lon=float(TARGET_SPOT_LON),lat=float(TARGET_SPOT_LAT))
        app.workflow.read_file(path=tif_path)
        app.workflow.estimate(validate_distance_km=float(VALIDATE_DIST_KM),find_match_only=strtobool(FIND_MATCH_ONLY))
        app.workflow.export(filename=filename, output_dir_path=OUTPUT_DIR, type='excel')
        app.workflow.close()
    return

if __name__ == "__main__":
    run_tif(app=app)