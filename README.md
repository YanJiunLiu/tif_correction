# TIF File Level Distance Analysis

此專案為使用 Python 分析 TIF 影像檔案的工具，功能包括：
1. 打開指定的 TIF 檔案（使用 rasterio）
2. 分析影像中的不同顏色等級（level）
3. 根據外部傳入的目標點列表，計算每個 level 的最近距離
4. 輸出含有 level、顏色與最近距離的 Excel 檔案
5. 輸出標示最近距離點位的 JPEG 影像檔

## 環境需求

請安裝以下 Python 套件：

套件列表包括：
- rasterio：讀取和操作地理空間影像檔
- numpy：數值運算
- pandas：資料表操作與 Excel 輸出
- opencv-python：圖像處理與標註
- openpyxl：Excel 文件讀寫支援

## 使用說明

1. 準備好輸入的 TIF 檔案，例如 `input.tif`。
2. 修改程式碼中 `target_points_img_coords` 變數，填入你的目標地點座標（影像內座標系）。
3. 執行主程式，將會在同目錄產生：
   - `output.xlsx`：記錄每個 level 的顏色與最近距離
   - `output.jpg`：標示距離目標點最近的像素點位影像
   
## 程式碼範例

詳細程式碼請參考主程式檔案。

---

若目標地點使用地理座標 (經緯度)，請利用 `rasterio` 的 `transform` 進行座標轉換後再計算距離。

## 聯絡

有任何問題歡迎提出討論。
