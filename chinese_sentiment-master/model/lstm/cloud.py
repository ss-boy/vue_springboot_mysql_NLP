import jieba.posseg as pseg  # 导入 posseg 模块进行词性标注
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import sys

# 读取文本内容
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# 对文本进行分词并保留名词
def segment_text(text):
    words = pseg.cut(text)
    nouns = [word for word, flag in words if flag.startswith('n')]
    return nouns

# 统计词频
def get_word_frequency(words):
    counter = Counter(words)
    return counter

# 生成词云图并保存
def generate_wordcloud(word_freq, output_path):
    wordcloud = WordCloud(
        font_path='C:/Windows/Fonts/simsun.ttc',  # 设置中文字体路径
        background_color='white',
        width=1000,
        height=800
    ).generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_path)  # 保存到指定路径
    plt.close()

# 主程序入口
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cloud.py <input_file_path> <output_image_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]  # 输入文本文件路径
    output_image_path = sys.argv[2]  # 输出图片路径

    text = read_text(input_file_path)
    words = segment_text(text)
    word_freq = get_word_frequency(words)
    generate_wordcloud(word_freq, output_image_path)

    print(f"Word cloud saved to {output_image_path}")
