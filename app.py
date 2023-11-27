from flask import Flask, render_template, request, jsonify
import faiss
import numpy as np

app = Flask(__name__)

# テストデータとFaissインデックスの作成
test_data = [
    [1.0, 5.0, 3.0, 0.0, 2.0, 3.0, 5.0, 3.0, 4.0, 0.0, 1.0, 1.0, 3.0, 5.0, 4.0, 5.0, 4.0, 5.0, 3.0, 1.0],
    [4.0, 5.0, 3.0, 1.0, 2.0, 3.0, 5.0, 3.0, 4.0, 0.0, 1.0, 5.0, 4.0, 5.0, 3.0, 4.0, 0.0, 5.0, 5.0, 4.0],
    [2.0, 1.0, 0.0, 3.0, 4.0, 0.0, 1.0, 4.0, 3.0, 5.0, 3.0, 4.0, 0.0, 1.0, 1.0, 3.0, 5.0, 1.0, 1.0, 0.0],
    [5.0, 3.0, 4.0, 0.0, 1.0, 5.0, 4.0, 5.0, 3.0, 4.0, 5.0, 3.0, 0.0, 2.0, 3.0, 5.0, 3.0, 4.0, 0.0, 1.0],
    [4.0, 5.0, 3.0, 4.0, 5.0, 3.0, 1.0, 0.0, 3.0, 4.0, 0.0, 5.0, 3.0, 4.0, 0.0, 1.0, 3.0, 5.0, 1.0, 1.0],
    [1.0, 5.0, 3.0, 0.0, 2.0, 3.0, 5.0, 3.0, 4.0, 0.0, 1.0, 1.0, 3.0, 5.0, 4.0, 5.0, 4.0, 5.0, 3.0, 0.0],
]

dimension = len(test_data[0])  # ベクトルの次元数
index = faiss.IndexFlatL2(dimension)
index.add(np.array(test_data, dtype=np.float32))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find_nearest', methods=['POST'])
def find_nearest():
    # フォームからユーザーのベクトルを取得
    user_vector_str = request.form['user_vector']
    user_vector = [float(x.strip()) for x in user_vector_str.split(',')]

    # 最近傍のベクトルを検索
    _, indices = index.search(np.array([user_vector], dtype=np.float32), k=2)

    # 結果の値だけを取り出す
    nearest_values = [test_data[i] for i in indices[0]]

    # 結果をJSONで返す
    return jsonify({'user_vector': user_vector, 'nearest_values': nearest_values})

if __name__ == '__main__':
    app.run(debug=True)
