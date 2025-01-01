from pathlib import Path
import os
import jieba


def build_data_file(directory, samples_path, label, mode_str):
    for sample_path in samples_path:
        try:
            # 尝试以 utf-8 编码打开文件
            with Path('{}/{}'.format(directory, sample_path)).open(encoding='utf-8') as f:
                words = [' '.join(jieba.cut(line.strip(), cut_all=False, HMM=True)) for line in f if line.strip() != '']
        except UnicodeDecodeError:
            try:
                # 如果 utf-8 失败，尝试 gbk 编码
                with Path('{}/{}'.format(directory, sample_path)).open(encoding='gbk') as f:
                    words = [' '.join(jieba.cut(line.strip(), cut_all=False, HMM=True)) for line in f if
                             line.strip() != '']
            except UnicodeDecodeError:
                # 如果两种编码都失败，跳过该文件或者使用其他方式处理
                print(f"Cannot decode file {sample_path} with utf-8 or gbk encoding.")
                continue

        # 写入处理后的词语
        with Path('{}.words.txt'.format(mode_str)).open('a', encoding='utf-8') as g:
            g.write('{}\n'.format(' '.join(words)))
        with Path('{}.labels.txt'.format(mode_str)).open('a', encoding='utf-8') as h:
            h.write('{}\n'.format(label))


if __name__ == '__main__':
    pos_dir = Path('raw_data/fix_pos')
    neg_dir = Path('raw_data/fix_neg')
    pos_samples = os.listdir(pos_dir)
    neg_samples = os.listdir(neg_dir)
    num_pos = len(pos_samples)
    num_neg = len(neg_samples)
    build_data_file(pos_dir, pos_samples[0:(num_pos - num_pos // 5)], 'POS', 'train')
    build_data_file(pos_dir, pos_samples[(num_pos - num_pos // 5):], 'POS', 'eval')
    build_data_file(neg_dir, neg_samples[0:(num_neg - num_neg // 5)], 'NEG', 'train')
    build_data_file(neg_dir, neg_samples[(num_neg - num_neg // 5):], 'NEG', 'eval')
