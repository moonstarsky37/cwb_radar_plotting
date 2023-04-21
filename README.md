# CWB_RADAR_Plotting
將雷達資料-雷達整合回波資料依照中央氣象局的呈現，由於色碼是用顏色編輯器確認的，所以不一定會和此網頁完全相同。
https://www.cwb.gov.tw/V8/C/W/OBS_Radar.html

* 資料格式:zip 或 json
  * 此content之欄位內的格點資料以逗號分隔之浮點數值，每一個數值以科學記號格式記錄，代表不同經緯度上之雷達回波值，單位為dBZ；其中資料無效值為-99，雷達觀測範圍外或經資料品管流程移除之資料則以-999表示。經向及緯向解析度均為0.0125度，每10分鐘更新1筆資料。左下角第一點之座標為東經115.0、北緯18.0，依序先由西向東、再由南往北遞增。使用之座標系統為TWD67。

* 轉換後結果
![](https://i.imgur.com/EUKK5LT.png) ![](https://i.imgur.com/jYgV7j8.png)



* Data Source: https://opendata.cwb.gov.tw/dataset/observation/O-A0059-001