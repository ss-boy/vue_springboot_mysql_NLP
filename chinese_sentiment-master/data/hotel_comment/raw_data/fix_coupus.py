import os
import codecs

POS = os.path.join(os.getcwd(), 'pos')
NEG = os.path.join(os.getcwd(), 'neg')
FIX_POS = os.path.join(os.getcwd(), 'fix_pos')
FIX_NEG = os.path.join(os.getcwd(), 'fix_neg')


def fix_corpus(dir_s, dir_t):
    for item in os.listdir(dir_s):
        with open(os.path.join(dir_s, item), 'r', encoding='gb2312', errors='ignore') as f:
            s = f.read()  # 直接读取为字符串，不需要decode
        # 如果gb2312编码失败，可以尝试其他编码
        if not s:
            with open(os.path.join(dir_s, item), 'r', encoding='gbk', errors='ignore') as f:
                s = f.read()
        with codecs.open(os.path.join(dir_t, item), 'w', encoding='utf8') as ff:
            ff.write(s)


if __name__ == "__main__":
    if not os.path.isdir(FIX_POS):
        os.mkdir(FIX_POS)
    if not os.path.isdir(FIX_NEG):
        os.mkdir(FIX_NEG)
    fix_corpus(POS, FIX_POS)
    fix_corpus(NEG, FIX_NEG)
