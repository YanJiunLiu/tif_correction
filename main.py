import os
from utils.decorators import workflow
from configs.settings import app, TIFF_PATHS, OUTPUT_DIR

@workflow('tif')
def run_tif(app):
    for tif_path in TIFF_PATHS:
        filename = os.path.splitext(os.path.basename(tif_path))[0]
        app.workflow.initial_data()
        app.workflow.choose_aim_point(lon=121.858688,lat=24.920176)
        app.workflow.read_file(path=tif_path)
        app.workflow.estimate()
        app.workflow.export(filename=filename, output_dir_path=OUTPUT_DIR, type='excel')
        app.workflow.export(filename=filename, output_dir_path=OUTPUT_DIR, type='png')
    return

if __name__ == "__main__":
    run_tif(app=app)