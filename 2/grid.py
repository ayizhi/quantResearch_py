#coding:utf-8
from __future__ import print_function
from pprint import pprint
from time import time
import logging

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline


# # Display progress logs on stdout
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s')


# ###############################################################################
# # Load some categories from the training set
# categories = [
#     'alt.atheism',
#     'talk.religion.misc',
# ]
# # Uncomment the following to do the analysis on all the categories
# #categories = None

# print("Loading 20 newsgroups dataset for categories:")
# print(categories)

# data = fetch_20newsgroups(subset='train', categories=categories)
# print("%d documents" % len(data.filenames))
# print("%d categories" % len(data.target_names))
# print()

###############################################################################
# 使用pipeline定义文本分类问题常见的工作流，包含向量化和一个简单的分类器
# pipeline = Pipeline([
#     ('vect', CountVectorizer()),
#     ('tfidf', TfidfTransformer()),
#     ('clf', SGDClassifier()),
# ])

# # 参数空间：
# # 定义了pipeline中各个模型的需要穷尽求解的参数空间，比如：clf__penalty': ('l2', 'elasticnet')
# # 表示SGDClassifier分类器的正则化选项为L2和elasticnet，训练时模型会分别使用这两个正则化方法来寻求最佳的方式
# parameters = {
#     'vect__max_df': (0.5, 0.75, 1.0),
#     #'vect__max_features': (None, 5000, 10000, 50000),
#     'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
#     #'tfidf__use_idf': (True, False),
#     #'tfidf__norm': ('l1', 'l2'),
#     'clf__alpha': (0.00001, 0.000001),
#     'clf__penalty': ('l2', 'elasticnet'),
#     #'clf__n_iter': (10, 50, 80),
# }

# if __name__ == "__main__":
categories = [
    'alt.atheism',
    'talk.religion.misc',
]
data = fetch_20newsgroups(subset='train', categories=categories)
print (data.data)
print (data.target)

    # # 通过GridSearchCV来寻求最佳参数空间
    # grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    # print("Performing grid search...")
    # print("pipeline:", [name for name, _ in pipeline.steps])
    # print("parameters:")
    # pprint(parameters)
    # t0 = time()

    # # 这里只需调用一次fit函数就可以了
    # grid_search.fit(data.data, data.target)
    # print("done in %0.3fs" % (time() - t0))
    # print()

    # # 输出best score
    # print("Best score: %0.3f" % grid_search.best_score_)
    # print("Best parameters set:")
    # # 输出最佳的分类器到底使用了怎样的参数
    # best_parameters = grid_search.best_estimator_.get_params()
    # for param_name in sorted(parameters.keys()):
    #     print("\t%s: %r" % (param_name, best_parameters[param_name]))