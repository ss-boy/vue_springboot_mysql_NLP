from collections import Counter
from pathlib import Path

MIN_COUNT = 1

if __name__ == '__main__':
    def words(name):
        return '{}.words.txt'.format(name)


    print('Build vocab words')
    counter_words = Counter()
    for n in ['train', 'eval']:
        try:
            # 尝试以 utf-8 编码打开文件
            with Path(words(n)).open(encoding='utf-8') as f:
                for line in f:
                    counter_words.update(line.strip().split())
        except UnicodeDecodeError:
            try:
                # 如果 utf-8 解码失败，尝试 gbk 编码
                with Path(words(n)).open(encoding='gbk') as f:
                    for line in f:
                        counter_words.update(line.strip().split())
            except UnicodeDecodeError:
                # 如果两种编码都失败，跳过该文件或采取其他处理措施
                print(f"Cannot decode file {words(n)} with utf-8 or gbk encoding.")
                continue

    vocab_words = {w for w, c in counter_words.items() if c >= MIN_COUNT}

    with Path('vocab.words.txt').open('w', encoding='utf-8') as f:
        for w in sorted(list(vocab_words)):
            f.write('{}\n'.format(w))
    print('Done. Kept {} out of {}'.format(
        len(vocab_words), len(counter_words)))


    def labels(name):
        return '{}.labels.txt'.format(name)


    print('Build labels')
    doc_tags = set()
    try:
        # 尝试以 utf-8 编码打开文件
        with Path(labels('train')).open(encoding='utf-8') as f:
            for line in f:
                doc_tags.add(line.strip())
    except UnicodeDecodeError:
        try:
            # 如果 utf-8 解码失败，尝试 gbk 编码
            with Path(labels('train')).open(encoding='gbk') as f:
                for line in f:
                    doc_tags.add(line.strip())
        except UnicodeDecodeError:
            # 如果两种编码都失败，跳过该文件或采取其他处理措施
            print(f"Cannot decode file {labels('train')} with utf-8 or gbk encoding.")

    with Path('vocab.labels.txt').open('w', encoding='utf-8') as f:
        for t in sorted(list(doc_tags)):
            f.write('{}\n'.format(t))
    print('- done. Found {} labels.'.format(len(doc_tags)))
