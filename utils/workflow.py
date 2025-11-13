from abc import ABC, abstractmethod
import os
import rasterio
import numpy as np
import pandas as pd
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
from pyproj import Transformer

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
        self.lats = []
        self.lons = []
        self.results = []

    def initial_data(self):
        self.aim = (0, 0)
        self.src = None
        self.lats = [] # 所有經度
        self.lons = [] # 所有緯度
        self.results = []
        
    def tranform(self)-> tuple:
        transform = self.src.transform 
        self.logger.info(
            f"成功取得transform參數用以地理-像素轉換"
        )
        self.lats = np.zeros((self.src.height, self.src.width))
        self.lons = np.zeros((self.src.height, self.src.width))
        for row in range(self.src.height):
            for col in range(self.src.width):
                lon, lat = rasterio.transform.xy(transform, row, col)
                self.lats[row, col] = lat
                self.lons[row, col] = lon

        self.logger.info(
            f"成功產生每個像素的經緯度"
        )
    
    def read_file(self, path:str)-> None:
        self.logger.info(f"read tif file: {path}")
        self.src = rasterio.open(path)
        self.logger.info(
            f"""
                檔案名稱: {self.src.name}, 
                尺寸(width x height): {self.src.width} x {self.src.height}, 
                波段數量: {self.src.count}, 
                CRS: {self.src.crs}, 
                像素大小(transform): {self.src.transform}, 
                資料型態(dtype): {self.src.dtypes}, 
                影像範圍(bounds): {self.src.bounds}
            """
        )
            
    
    def choose_aim_point(self, lon, lat):
        self.logger.info(
            f"""
                目標經度: {lon}, 
                目標緯度: {lat},
            """
        )
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

        
    def estimate(self):
        self.logger.info(
            f"開始計算"
        )
        crs_src = self.src.crs
        crs_dst = 'EPSG:4326'  # WGS84經緯度座標系統
        transformer = Transformer.from_crs(crs_src, crs_dst, always_xy=True)
        for level in range(1, self.src.count+1):
            band_data = self.src.read(level)
            nonzero_indices = np.nonzero(band_data)
            # height, width = band_data.shape
            # rows, cols = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
            rows = nonzero_indices[0]
            cols = nonzero_indices[1]
            xs, ys = rasterio.transform.xy(self.src.transform, rows, cols)
            xs = np.array(xs)
            ys = np.array(ys)
    
            lon, lat = transformer.transform(xs, ys)
            self.logger.info(
                f"轉換成經緯度:{lon, lat}"
            )
            distances = np.vectorize(self.haversine)(lon,lat, self.aim[0], self.aim[1])
            min_idx = np.argmin(distances)
            # closest_point = (lon[min_idx], lat[min_idx])
            closest_distance_km = distances[min_idx]

            self.results.append({
                'level': level,
                'distance_km': closest_distance_km,
                'closest_lon': lon[min_idx],
                'closest_lat': lat[min_idx]
               
            })
                    

    def to_excel(self,output_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_path = os.path.join(output_path,f'output_{timestamp}.xlsx')
        df = pd.DataFrame(self.results)
        df.to_excel(excel_path, index=False, header=['level','distance_km','closest_lon','closest_lat'])

    def to_png(self,output_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(output_path,f'output_{timestamp}.png')
        _, ax = plt.subplots(figsize=(8, 8))
        ax.plot(self.aim[0], self.aim[1], 'ro', label='Target')
        
        for result in self.results:
            ax.plot(result['closest_lon'], result['closest_lat'], marker='x', label=f'Level {result['level']} closest')

        ax.legend()
        ax.set_title('Target and closest pixel positions per level')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        plt.savefig(img_path)

    def export(self, output_dir_path , type="excel"):
        self.src.close()
        if type == "excel":
            self.to_excel(output_dir_path)
        else:
            self.to_png(output_dir_path)