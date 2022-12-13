import pandas as pd


class ChineseSortAndFormat:
    def __init__(self):
        self.score_df = pd.read_csv(r'score.csv', encoding='gbk', keep_default_na=False)
        self.word_frequency_df = pd.read_csv(r'list.csv', encoding='gbk', header=None,
                                             names=['汉字', '拼音', '笔画'], keep_default_na=False)
        self.pinyin_dict = {}
        self.stroke_dict = {}
        self.score_pinyin_list = []
        self.score_stroke_list = []
        self.txt = open(r'红楼梦.txt', 'r', encoding='utf-8').read()
        self.count_dict = {}
        for i in self.word_frequency_df['汉字']:
            self.count_dict[i] = self.txt.count(i)
        self.count_word_list = [self.count_dict[i] for i in self.word_frequency_df['汉字']]
        self.word_frequency_df['词频'] = self.count_word_list
        for i in range(len(self.word_frequency_df['汉字'])):
            self.pinyin_dict[self.word_frequency_df['汉字'][i]] = self.word_frequency_df['拼音'][i]
            self.stroke_dict[self.word_frequency_df['汉字'][i]] = self.word_frequency_df['笔画'][i]
        for i in self.score_df['姓名']:
            this_pinyin = []
            this_stroke = 0
            for j in i:
                this_pinyin.append(self.pinyin_dict[j])
                this_stroke += self.stroke_dict[j]
            self.score_pinyin_list.append(''.join(this_pinyin))
            self.score_stroke_list.append(this_stroke)
        self.score_df['拼音'] = self.score_pinyin_list
        self.score_df['笔画'] = self.score_stroke_list

    def sort_by_pinyin(self, chinese_list):
        pinyin_dict = {}
        for i in chinese_list:
            this_pinyin = []
            for j in i:
                this_pinyin.append(self.pinyin_dict[j])
            pinyin_dict[i] = ''.join(this_pinyin)
        chinese_list.sort(key=lambda x: pinyin_dict[x])
        return chinese_list

    def sort_by_stroke(self, chinese_list):
        stroke_dict = {}
        for i in chinese_list:
            this_stroke = 0
            for j in i:
                this_stroke += self.stroke_dict[j]
            stroke_dict[i] = this_stroke
        chinese_list.sort(key=lambda x: stroke_dict[x])
        return chinese_list

    def is_chinese(self, word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def chinese_format(self, x):
        length_letter = 0
        length = len(x)
        for i in x:
            if self.is_chinese(i):
                pass
            else:
                length_letter += 1
        return '{:^{}}'.format(x, length+length_letter)


if __name__ == '__main__':
    chinese_sorter = ChineseSortAndFormat()
    # print(chinese_sorter.sort_by_pinyin(chinese_sorter.score_df['姓名'].tolist()))
    # print(chinese_sorter.sort_by_stroke(chinese_sorter.score_df['姓名'].tolist()))
    chinese_sorter.word_frequency_df['汉字'] = chinese_sorter.word_frequency_df.apply(lambda x: chinese_sorter.chinese_format
    (x['汉字']), axis=1)
    word_by_pinyin_df = chinese_sorter.word_frequency_df[chinese_sorter.word_frequency_df['词频'] != 0]
    word_chinese_list = word_by_pinyin_df['汉字'].tolist()
    word_chinese_list_by_pinyin = chinese_sorter.sort_by_pinyin(word_chinese_list)
    word_pinyin_list = [chinese_sorter.pinyin_dict[i] for i in word_chinese_list_by_pinyin]
    word_stroke_list = [chinese_sorter.stroke_dict[i] for i in word_chinese_list_by_pinyin]
    word_by_pinyin_df['汉字'] = word_chinese_list_by_pinyin
    word_by_pinyin_df['拼音'] = word_pinyin_list
    word_by_pinyin_df['笔画'] = word_stroke_list
    word_by_pinyin_df.to_csv(r'红楼梦字频表按拼音排序.csv', index=False, encoding='gbk')
    word_by_stroke_df = chinese_sorter.word_frequency_df[chinese_sorter.word_frequency_df['词频'] != 0]
    word_chinese_list = word_by_stroke_df['汉字'].tolist()
    word_chinese_list_by_stroke = chinese_sorter.sort_by_stroke(word_chinese_list)
    word_pinyin_list = [chinese_sorter.pinyin_dict[i] for i in word_chinese_list_by_stroke]
    word_stroke_list = [chinese_sorter.stroke_dict[i] for i in word_chinese_list_by_stroke]
    word_by_stroke_df['汉字'] = word_chinese_list_by_stroke
    word_by_stroke_df['拼音'] = word_pinyin_list
    word_by_stroke_df['笔画'] = word_stroke_list
    word_by_stroke_df.to_csv(r'红楼梦字频表按笔画排序.csv', index=False, encoding='gbk')
    word_by_frequency_df = chinese_sorter.word_frequency_df[chinese_sorter.word_frequency_df['词频'] != 0]
    word_by_frequency_df = word_by_frequency_df.sort_values(by=['词频'])
    word_by_frequency_df.to_csv(r'红楼梦字频表按频次排序.csv', index=False, encoding='gbk')
    chinese_sorter.score_df['姓名'] = chinese_sorter.score_df.apply(
        lambda x: chinese_sorter.chinese_format(x['姓名']), axis=1)
    score_by_score_df = chinese_sorter.score_df
    score_by_score_df = score_by_score_df.sort_values(by=['一', '二', '三', '四'])
    score_by_score_df = score_by_score_df.drop(columns=['拼音', '笔画'])
    score_by_score_df.to_csv(r'成绩表按成绩排序.csv', index=False, encoding='gbk')
    score_by_pinyin_df = chinese_sorter.score_df
    score_by_pinyin_df = score_by_pinyin_df.sort_values(by=['拼音'])
    score_by_pinyin_df = score_by_pinyin_df.drop(columns=['拼音', '笔画'])
    score_by_pinyin_df.to_csv(r'成绩表按拼音排序.csv', index=False, encoding='gbk')
    score_by_stroke_df = chinese_sorter.score_df
    score_by_stroke_df = score_by_stroke_df.sort_values(by=['笔画'])
    score_by_stroke_df = score_by_stroke_df.drop(columns=['拼音', '笔画'])
    score_by_stroke_df.to_csv(r'成绩表按笔画排序.csv', index=False, encoding='gbk')




