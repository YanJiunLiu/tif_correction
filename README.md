# TIF File Level Distance Analysis

此專案為使用 Python 分析 TIF 影像檔案的工具，功能包括：
1. 打開指定的 TIF 檔案（使用 rasterio）
2. 分析影像中的不同顏色等級（level）
3. 根據外部傳入的目標點列表，計算每個 level 中所有在驗證範圍內的點位
4. 輸出含有 level、顏色與距離的 Excel 檔案


## 環境需求

請安裝以下 Python 套件：

套件列表包括：
- rasterio：讀取和操作地理空間影像檔
- numpy：數值運算
- pandas：資料表操作與 Excel 輸出
- opencv-python：圖像處理與標註
- openpyxl：Excel 文件讀寫支援

## 使用說明

1. 下載專案 `git clone https://github.com/YanJiunLiu/tif_correction.git` 
2. 設定好環境 範例 (使用uv管理): 
   ```
      1. Windows 環境
         a) 到uv官網下載
         b) uv venv 313_window --python 3.13
         c) 啟動環境
         d) uv pip install -r requirement.txt
      2. linux (Ubuntu / MacOS)環境
         a)  wget -qO- https://astral.sh/uv/install.sh | sh
         b) source $HOME/.local/bin/env
         c) 啟動環境
         d) uv pip install -r requirement.txt
   ```
3. 到tiff correction 目錄下
4. 設定.env
   ```
      # Linux下的路徑範例
      # TIF_DIRPATH="/mnt/c/Users/user/workspace/itri/tif_correction/tif"

      # Windows下的路徑範例
      TIF_DIRPATH= "C:\\Users\\user\\workspace\\itri\\tif_correction\\tif"

      # Linux下的路徑範例
      # OUTPUT_DIR="/mnt/c/Users/user/workspace/itri/tif_correction/output"

      # Windows下的路徑範例
      OUTPUT_DIR= "C:\\Users\\user\\workspace\\itri\\tif_correction\\output"

      # Linux下的路徑範例
      # LOG_DIR="/mnt/c/Users/user/workspace/itri/tif_correction/logs"

      # Windows下的路徑範例
      LOG_DIR= "C:\\Users\\user\\workspace\\itri\\tif_correction\\logs"

      # 驗證距離閾值，單位：公里
      VALIDATE_DIST_KM = 0.1

      # 是否僅查找匹配點
      FIND_MATCH_ONLY = False

      # 目標位點 (經度)
      TARGET_SPOT_LON=121.858688
      
      # 目標位點 (緯度)
      TARGET_SPOT_LAT=24.920176

   ```  
5. 執行 python main.py



