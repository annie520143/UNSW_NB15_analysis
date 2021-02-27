
# 執行方式
1. ### DNN
    1. 開啟`./method_dl/main_dnn.py`
    2. 更改76-86行的7個參數  
    ```
       trainPath : 訓練用csv檔案
       testPath : 測試用csv檔案
       opt : (label/attack_cat)二擇一，代表輸出為只區分正常異常流量、或能區分所有種類之攻擊
       newModelName : 此次訓練結果要儲存的檔案名稱
       reTrain : (True/False)二擇一，代表是否要重新訓練並儲存結果。
       usedModelPath : 若 reTrain == True，則此參數為此次的model; 若 reTrain == False，則此參數為先前已訓練好、欲使用的model。
       imp_feature : 決定要進入神經網路的特徵
    ```
    3. 執行`main_dnn.py`，同步進行training和testing
    
2. ### RNN
    

# 檔案及函式描述
1. ### DNN
    1. ##### `./method_dl/main_dnn.py`
        1. `CategoryOneHot(label, opt)` : 把類別數字轉成One-Hot編碼的格式。  
        *eg: 若在opt == label 之下的1會編碼成 [0, 1]; 若在opt == attack_cat之下的1會編碼成 [0, 1, 0, 0 ,0, 0, 0, 0 ,0, 0]*
        2. `ProcessData(datapath, opt)` : 對trainPath跟testPath的csv檔做前處理，會呼叫到`preprocessing.py`裡的函式。
        3. `info()` : 印出此次訓練的model的path, 存在哪個.h5檔。
        
    2. ##### `./method_dl/preprecessing.py`
        1. `SeperateAttackLabel(packets)` : UNSW Dataset中每筆資料的標籤有二，一為0/1(非攻擊或攻擊)、另一為字串型態(哪一種類的攻擊)，此函式將標籤從Dataset中移除，另獨立為兩個Array，並將字串型態的標籤轉為數字0-9。此函式具有三個回傳值，除去標籤後的Dataset、只分0/1的標籤Array、依據攻擊種類分為0-9的標籤Array。
        3. `FeatureOneHot(packets)` : 將三種類別參數(`proto`、`states`、`service`)做oneHotEncoding。
        5. `GetImp(packets)` : 依據`main_dnn.py`中的`imp_features`選出進入神經網路的特徵。
        6. `TransDatatype(packets)` : 將Dataset轉化成可以正規化處理的格式。
        7. `FeatureScaling(packets)` : 將所有特徵正規化。
        8. `NpFillna(packets)` : 缺失值填0。

    3. ##### `./method_dl/method_dnn.py`
        1. `simpleDNN(feature_dim, units, atv, loss)` : DNN模型，於`main_dnn.py`中呼叫。
        2. `simpleDNN_dropout(feature_dim, atv, loss, output_dim)` : 含dropout的DNN模型，於`main_dnn.py`中呼叫。
        3. `matricsDNN(predict, actual, method, dim)` : 印出confusion matrix
        4. `detailAccuracyDNN(predict, actual, method, dim)` : 印出每個類別實際的預測準確率

2. ### RNN
