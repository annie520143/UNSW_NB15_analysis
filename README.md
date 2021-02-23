
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
    3. 若要改變進入神經網路的特徵，至`preprocessing.py`第10行，修改`imp_features`陣列。
    4. 執行`main_dnn.py`，同步進行training和testing
    
2. ### RNN
    

# 檔案及函式描述
1. ##### `./method_dl/main_dnn.py`
    1. ` CategoryOneHot(label, opt)` : 
    2. `ProcessData(datapath, opt)` : 對trainPath跟testPath的csv檔做前處理，會呼叫到`preprocessing.py`裡的函式
    3. `info()` : 印出此次訓練的model的path, 存在哪個.h5檔
    
2. ##### `./method_dl/preprecessing.py`
    1. `SeperateAttackLabel(packets)` : UNSW Dataset中每筆資料的標籤有二，一為0/1(非攻擊或攻擊)、另一為字串型態(哪一種類的攻擊)，此函式將標籤從Dataset中移除，另獨立為兩個Array，並將字串型態的標籤轉為數字0-9。此函式具有三個回傳值，除去標籤後的Dataset、只分0/1的標籤Array、依據攻擊種類分為0-9的標籤Array
    3. `FeatureOneHot(packets)` :
    4. `GetImp(packets)` : 
    5. `FeatureScaling(packets)` :
    6. `TransDatatype(packets)` :
    7. `NpFillna(packets)` :
