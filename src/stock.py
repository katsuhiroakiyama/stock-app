# 必要なモジュールのインポート
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.metrics import classification_report
#import XGBClassifier #おかしい場所？
import matplotlib.pyplot as plt
import joblib

#データの取得
df= pd.read_csv('src/stock invest1.csv') #ファイルの読み込みをどうするのか


# 入力変数と出力変数に切り分け
x = df.drop('Target', axis = 1).values
t = df['Target'].values

# 学習用データとテスト用データに分割
from sklearn.model_selection import train_test_split
x_train, x_test, t_train, t_test =train_test_split(x, t, test_size=0.3, random_state=0)

# サポートベクトルマシンのインスタンス化を作成
model = svm.LinearSVC()
#model = XGBClassifier(n_estimators=50)

# 学習と推論
model.fit(x_train, t_train)
pred = model.predict(x_test)

# 予測精度を確認
print(classification_report(t_test, pred)) #変更が必要

#　学習済みモデルを保存
joblib.dump(model, "src/stock.pkl", compress= True) #iris.pklのファイルの保存法と併せて確認が必要