
import jieba
from pathlib import Path
from tensorflow.contrib import predictor
from functools import partial

import sys
import io
# 手动设置 stdout 为 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')



if len(sys.argv) < 2:
    print("Usage: python txt-serve.py <path_to_comments_file>")
    sys.exit(1)

COMMENTS_FILE = sys.argv[1]  # 从命令行获取文件路径

def predict(pred_fn, line):
    sentence = ' '.join(jieba.cut(line.strip(), cut_all=False, HMM=True))
    words = [w.encode() for w in sentence.strip().split()]
    nwords = len(words)
    predictions = pred_fn({'words': [words], 'nwords': [nwords]})
    return predictions

if __name__ == '__main__':
    export_dir = 'D:/java/vue01/chinese_sentiment-master/model/lstm/saved_model'
    subdirs = [x for x in Path(export_dir).iterdir() if x.is_dir() and 'temp' not in str(x)]
    latest = str(sorted(subdirs)[-1])
    predict_fn = partial(predict, predictor.from_saved_model(latest))

    with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                print(f"评论: {line}")
                prediction = predict_fn(line)
                print(f"预测结果: {prediction}")
                print("="*50)
