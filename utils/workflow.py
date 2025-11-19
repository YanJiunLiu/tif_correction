from abc import ABC, abstractmethod
import os
import rasterio
import numpy as np
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt

class Base(ABC):
    def __init__(self, logger):
        self.logger = logger

    @abstractmethod
    def read_file(self,*args, **kwargs):
        raise NotImplementedError(f"def {self.read_tif.__name__} is not implemented.")


    @abstractmethod
    def estimate(self,*args, **kwargs):
        raise NotImplementedError(f"def {self.estimate.__name__} is not implemented.")

    @abstractmethod
    def export(self,*args, **kwargs):
        raise NotImplementedError(f"def {self.export.__name__} is not implemented.")
    
class WorkflowTIF(Base):
    """
        TIF File Level Distance Analysis
    """


    def __init__(self, logger):
        super().__init__(logger)
        self.aim = (0, 0)
        self.src = None
        self.results = {
            "validated_spot":[],
            "match_spot":[],
        }
        self.stop = False

    def initial_data(self):
        self.logger.info(
            f"""初始化TIF檔案處理流程"""
        )
        self.aim = (0, 0)
        self.src = None
        self.results = {
            "validated_spot":[],
            "match_spot":[],
        }
        self.stop = False
        
    def read_file(self, path:str)-> None:
        self.src = rasterio.open(path)
        self.logger.info(
            f"""讀取TIF檔案資訊:
                檔案名稱: {self.src.name}, 
                尺寸(width x height): {self.src.width} x {self.src.height}, 
                波段數量: {self.src.count}, 
                CRS: {self.src.crs}, 
                影像範圍(bounds): {self.src.bounds}
            """
        )
            
    
    def choose_aim_point(self, lon, lat):
        self.logger.info(
            f"""鎖定目標座標: 經度: {lon}, 緯度: {lat}""")
        self.aim = (lon, lat)
    
    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        # 將角度轉弧度
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
        # 差異
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        # haversine公式
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        # 地球半徑 (km)
        R = 6371
        return R * c

        
    def estimate(self, validate_distance_km=0.1, find_match_only=False):
        self.logger.info(
            f"""開始計算"""
        )
        self.stop = find_match_only
        for level in range(1, self.src.count+1):
            band_data = self.src.read(level)   
            stop = False
            for row in tqdm(range(band_data.shape[0]), desc=f"Processing level {level}"):
                for col in range(band_data.shape[1]):  
                    color = band_data[row, col]
                    # 過濾無效值
                    if self.src.nodata == 0 or self.src.nodata is not None:
                        if color == self.src.nodata: # 跳過無效值
                            continue
                    else:
                        if color < 100: # 跳過無效值
                            continue
                    lon, lat = rasterio.transform.xy(self.src.transform, row, col) # 取得像素中心點的座標
                    lon_min, lat_max = rasterio.transform.xy(self.src.transform, row, col, offset='ul') # 取得像素左上角座標
                    pixel_width = abs(self.src.transform.a)
                    pixel_height = abs(self.src.transform.e)
                    # 取得像素左上角座標
                    lon_max = lon_min + pixel_width 
                    lat_min = lat_max - pixel_height
                    dist = self.haversine(lon, lat, self.aim[0], self.aim[1])
                    if (lon_min <= self.aim[0] <= lon_max) and (lat_min <=  self.aim[1]  <= lat_max):
                        self.results['validated_spot'].append((level, dist, lon, lat, lon_max, lon_min, lat_max, lat_min, "Match", color))
                        self.results['match_spot'].append((level, dist, lon, lat, lon_max, lon_min, lat_max, lat_min, "Match", color))
                        if self.stop:
                            self.results['validated_spot'] = [] # release memory
                            stop = True
                            break      
                    else:
                        if dist < validate_distance_km:
                            self.results['validated_spot'].append((level, dist, lon, lat, lon_max, lon_min, lat_max, lat_min, "Close", color))
                if stop:
                    break
        self.logger.info(
            f"""所有層級處理完成
            符合範圍條件點數:{len(self.results['validated_spot'])},
            """
        )
                    

    def to_excel(self,filename, output_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_path = os.path.join(output_path,f'{filename}_{timestamp}.xlsx')
        if self.stop:
            if not self.results['match_spot']:
                self.logger.warning("無符合條件的結果，無法匯出Excel檔案")
                return
            df = pd.DataFrame(self.results['match_spot'])
        else:
            if not self.results['validated_spot']:
                self.logger.warning("無符合條件的結果，無法匯出Excel檔案")
                return
            df = pd.DataFrame(self.results['validated_spot'])
        df.to_excel(excel_path, index=False, header=['level','distance_km','lon','lat', 'lon_max','lon_min','lat_max','lat_min', 'status', 'color'])


    def export(self, filename, output_dir_path , type="excel"):
        if type == "excel":
            self.logger.info(f"匯出Excel檔案至 {output_dir_path}")
            self.to_excel(filename, output_dir_path)
       
            
    def close(self):
        if self.src:
            self.src.close()
            self.logger.info("已關閉tif檔案資源")