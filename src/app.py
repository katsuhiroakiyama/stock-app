# 必要なモジュールのインポート
import joblib
from flask import Flask, request, render_template
from wtforms import Form, FloatField, validators, SubmitField
import numpy as np


# 学習済みモデルをもとに推論する関数
def predict(x):
    #　学習済みモデル(stock.pkl)を読み込み
    model = joblib.load('stock.pkl') #ファイル名が変わる src/を削除
    x = x.reshape(1,-1) #xをreshapeで２次元ベクトルにする。
    stock_predict = model.predict(x)
    return stock_predict

#推論したラベルから花の名前を返す関数
def getName(label):
    if label == 0:
        return "上昇率 150%以上"
    elif label == 1:
        return "上昇率 100~149%"
    elif label == 2:
        return "上昇率 99~50%"
    elif label == 3:
        return "上昇率 25~49%"
    elif label == 4:
        return "上昇率 0~24%"
    elif label == 5:
        return "下落率 0~-15%"
    elif label == 6:
        return "下落率 -16~-30%"
    elif label == 7:
        return "下落率 -31~-50%"
    elif label == 8:
        return "下落率 -51~-99%"
    
    else:
        return "Error"

# Flaskのインスタンス化を作成
app = Flask(__name__, static_folder='./templates/img')


# 入力フォームの設定を行うクラス
class StockPredictionForm(Form):
    Uriage = FloatField("売上変化率(-100~600%)",
                    [validators. InputRequired(),
                    validators.NumberRange(min=-100, max=600, message="-100~600の数値を入力してください")]
                    )
    PER = FloatField("PER変化率(-70~200%)",
                    [validators. InputRequired(),
                    validators.NumberRange(min=-70, max=200, message="-70~200の数値を入力してください")]
                    )
    Rieki = FloatField("経常利益変化率(-500~4200%)",
                    [validators. InputRequired(),
                    validators.NumberRange(min=-500, max=4200, message="-500~4200の数値を入力してください")]
                    )   
    #HTML側に表示するsbmitボタンの設定
    submit = SubmitField("判定")



# URLにアクセスがあった場合の挙動
# 入力フォームから数値を受け取る　→　推論　→　判定結果を結果表示用のHTMLファイル（reslut.html)に送る
@app.route('/', methods=['GET','POST'])
def predicts():
    # フォームの設定IrisFormクラスをインスタンス化
    stockpredictionform = StockPredictionForm(request.form)
    #POST メソッドの定義
    if request.method == 'POST':
        # 条件に当てはまる場合
        if stockpredictionform.validate() == False:
            return render_template('index.html', forms = stockpredictionform)
        # 条件に当てはまらない場合、推論を実行
        else:
            VarUriage = float(request.form["Uriage"])
            VarPER = float(request.form["PER"])
            VarRieki = float(request.form["Rieki"])
            #入力された値をndarrayに変換して推論
            x = np.array([VarUriage,VarPER,VarRieki])
            pred = predict(x)
            stockprediction_=getName(pred)
            return render_template('result.html', stockprediction=stockprediction_)
    # GET メソッドの定義
    elif request.method == 'GET':
         return render_template('index.html', forms = stockpredictionform)

# アプリケーションの実行
if __name__=="__main__":
    app.run(debug=True)


