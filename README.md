
# 執行方式
1. ### DNN
    1. 開啟`./method_dl/main_dnn.py`
    2. 更改76-80行的四個參數  
    ```
       trainPath : 訓練用csv檔案
       testPath : 測試用csv檔案
       opt : (label/attack_cat)二擇一，代表輸出為只區分正常異常流量、或能區分所有種類之攻擊
       usedModel : 先前訓練好之model、或要將訓練結果儲存的檔案
    ```
    3. 執行`main_dnn.py`，同步進行training和testing
    
2. ### RNN
    

# 檔案及函式描述
1. ##### `./method_dl/main_dnn.py`
    1. ` CategoryOneHot(label, opt)` : 
    2. `ProcessData(datapath, opt)` : 對trainPath跟testPath的csv檔做前處理，會呼叫到`preprocessing.py`裡的函式
    
2. ##### `./method_dl/preprecessing.py`
    1. 
