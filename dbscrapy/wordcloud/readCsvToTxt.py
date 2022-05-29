import jieba
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# 读取文件的文字， 返回词
def change(scrFile):
    with open(scrFile, 'r',encoding='utf-8') as f:
        wordsTest = ''
        for line in f.readlines():
            line = line.strip("\n")
            line_split = line.split(',')
            text = ''.join(line_split[4]) # 每行文字大合集
            words = jieba.lcut(text) # 精确分词
            wordsTest = wordsTest + "".join(words)
        return wordsTest

# 通过词生成词云 并展示
def generate_wordcount(text):
    d = path.dirname(__file__)
    alice_mask = np.array(Image.open(path.join("Images//alice_mask.png")))
    font_path = path.join(d, "font//msyh.ttf")
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(background_color="white",
                          max_words=2000,
                          mask=alice_mask,
                          stopwords=stopwords,
                          font_path=font_path,
                          )
    wordcloud.generate(text)

    wordcloud.to_file(path.join(d, r"词云/alice.png"))
    # 显示图像
    plt.imshow(wordcloud, interpolation='bilinear')
    # interpolation='bilinear' 表示插值方法为双线性插值
    plt.axis("off")# 关掉图像的坐标
    plt.show()

if __name__ == '__main__':
    text = change(r"../../结果文件/人工智能/人工智能.csv")
    generate_wordcount(text)
