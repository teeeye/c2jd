"""
从训练集中取数据
"""

import sys
sys.path.append('..')
from utils.macros import *
import pickle
import random
import numpy as np


class Sampler:
    def __init__(self, batch_size=BATCH_SIZE, data_path=TRAIN_PATH):
        seed = random.randint(0, 1000)
        print("Sampler initiating with seed: %d" % seed)
        random.seed(seed)
        self.batch_size = batch_size
        _current_data_index = 0  # DATA_PATH 共八个文件, 目前只用第一个文件
        with open(data_path % _current_data_index, 'rb') as data_file:
            data = pickle.load(data_file)

        # 将 DataFrame 转化为 np.array 且 batch_size 为第二维度
        summary = []
        description = []
        label = []
        for _, row in data.iterrows():
            summary.append(row['candidate_summary'])
            description.append(row['job_description'])
            label.append(row['label'])
        self.summary = self.zero_pad(summary)
        self.description = self.zero_pad(description)
        self.label = np.array(label)
        print("Sampler initiated!")

    def zero_pad(self, inputs):
        result = np.zeros((len(inputs), PAD_SIZE, EMBED_DIM))
        for index, input in enumerate(inputs):
            for i in range(min(PAD_SIZE, len(input))):
                result[index, i] = input[i]
        return result.astype(np.int64)

    def next_batch(self):
        start = random.randint(0, len(self.summary)-self.batch_size)
        return self.summary[start:start+self.batch_size], \
            self.description[start:start+self.batch_size], \
            self.label[start:start+self.batch_size]


if __name__ == '__main__':
    s = Sampler(batch_size=16)
    print(s.next_batch())
