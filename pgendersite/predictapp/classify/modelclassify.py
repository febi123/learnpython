# Author: Matt Terry <matt.terry@gmail.com>
#
# License: BSD 3 clause
from __future__ import print_function

import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets.twenty_newsgroups import strip_newsgroup_footer
from sklearn.datasets.twenty_newsgroups import strip_newsgroup_quoting
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import psycopg2
import sys
from sklearn.externals import joblib
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FILENAME_MODELNAMA = "filename.pkl"
FILENAME_MODELNAMADANSUKU = "modelnamadansuku.pkl"

class ItemSelector(BaseEstimator, TransformerMixin):
    """For data grouped by feature, select subset of data at a provided key.

    The data is expected to be stored in a 2D data structure, where the first
    index is over features and the second is over samples.  i.e.

    >> len(data[key]) == n_samples

    Please note that this is the opposite convention to scikit-learn feature
    matrixes (where the first index corresponds to sample).

    ItemSelector only requires that the collection implement getitem
    (data[key]).  Examples include: a dict of lists, 2D numpy array, Pandas
    DataFrame, numpy record array, etc.

    >> data = {'a': [1, 5, 2, 5, 2, 8],
               'b': [9, 4, 1, 4, 1, 3]}
    >> ds = ItemSelector(key='a')
    >> data['a'] == ds.transform(data)

    ItemSelector is not designed to handle data grouped by sample.  (e.g. a
    list of dicts).  If your data is structured this way, consider a
    transformer along the lines of `sklearn.feature_extraction.DictVectorizer`.

    Parameters
    ----------
    key : hashable, required
        The key corresponding to the desired value in a mappable.
    """
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


class TextStats(BaseEstimator, TransformerMixin):
    """Extract features from each document for DictVectorizer"""

    def fit(self, x, y=None):
        return self

    def transform(self, posts):
        return [{'length': len(text),
                 'num_sentences': text.count('.')}
                for text in posts]


class CustomFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract the subject & body from a usenet post in a single pass.

    Takes a sequence of strings and produces a dict of sequences.  Keys are
    `subject` and `body`.
    """
    def fit(self, x, y=None):
        return self

    def transform(self, posts):
        features = np.recarray(shape=(len(posts),),
                               dtype=[('prefix1', object), ('lastletter', object)])
        for i, text in enumerate(posts):
            arrname = text.split()
            features['prefix1'][i] = arrname[0][0:2].lower() if len(arrname[0])>=2 else arrname[0].lower()
            features['lastletter'][i] = arrname[0][-2:].lower() if len(arrname[0])>=1 else arrname[0].lower()

        return features

class CustomFeatureExtractorByNameAndSuku(BaseEstimator, TransformerMixin):
    """Extract the subject & body from a usenet post in a single pass.

    Takes a sequence of strings and produces a dict of sequences.  Keys are
    `subject` and `body`.
    """
    def fit(self, x, y=None):
        return self

    def transform(self, posts):
        features = np.recarray(shape=(len(posts),),
                               dtype=[('prefix1', object), ('lastletter', object)
                                   # ,('prefix1_secondword', object), ('lastletter_secondword', object)
                                   , ('suku', object)])
        for i, thepar in enumerate(posts):
            arrname = thepar[0].split()
            secondword_name = "" if (len(arrname)<2 or arrname[1] is None or arrname[1] == "") else arrname[1].lower()
            suku = [""] if thepar[1] is None else thepar[1].split()
            features['prefix1'][i] = arrname[0][0:2].lower() if len(arrname[0]) >= 2 else arrname[0].lower()
            features['lastletter'][i] = arrname[0][-2:].lower() if len(arrname[0]) >= 1 else ""#arrname[0].lower()
            # features['prefix1_secondword'][i] = secondword_name[0:2] if len(secondword_name) >= 2 else secondword_name
            # features['lastletter_secondword'][i] = secondword_name[-2:] if len(secondword_name) >= 1 else ""#secondword_name
            features['suku'][i] = suku[0].lower()

        return features

class Genderclassify():
    C = 1.0
    pipeline = None
    pipelinenama = None
    pipelinenamaandsuku = None
    # ambil 1000 data untuk train dan 1000 data untuk test
    numbertakedata = 2436780
    numbertrain = 2431780
    numbertest = 5000

    def generatemodelbynameandsuku(self):
        self.pipeline = Pipeline([
            # Extract the subject & body
            ('myfeature', CustomFeatureExtractorByNameAndSuku()),

            # Use FeatureUnion to combine the features from subject and body
            ('union', FeatureUnion(
                transformer_list=[

                    # Pipeline for pulling features from the post's subject line
                    ('prefix1', Pipeline([
                        ('selector', ItemSelector(key='prefix1')),
                        ('tfidf', TfidfVectorizer()),
                    ])),
                    # Pipeline for pulling features from the post's subject line
                    ('lastletter', Pipeline([
                        ('selector', ItemSelector(key='lastletter')),
                        ('tfidf', TfidfVectorizer()),
                    ])),
                    # ('prefix1_secondword', Pipeline([
                    #     ('selector', ItemSelector(key='prefix1_secondword')),
                    #     ('tfidf', TfidfVectorizer()),
                    # ])),
                    # # Pipeline for pulling features from the post's subject line
                    # ('lastletter_secondword', Pipeline([
                    #     ('selector', ItemSelector(key='lastletter_secondword')),
                    #     ('tfidf', TfidfVectorizer()),
                    # ])),
                    # Pipeline for pulling features from the post's subject line
                    ('suku', Pipeline([
                        ('selector', ItemSelector(key='suku')),
                        ('tfidf', TfidfVectorizer()),
                    ])),

                ],

                # weight components in FeatureUnion
                transformer_weights={
                    'prefix1': 1.0,
                    'lastletter': 0.9,
                    # 'prefix1_secondword': 0.7,
                    # 'lastletter_secondword': 0.7,
                    'suku': 0.9,
                },
            )),

            # Use a SVC classifier on the combined features
            ('svc', SVC(
                # kernel='poly', degree=3, C=C
                # kernel = 'linear'
                kernel='rbf', gamma=0.7, C=self.C, probability=True
                # C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=True, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None, random_state=None
            )),
        ])


        con = None
        rows = None
        try:

            con = psycopg2.connect("dbname='genderid' user='postgres' password='root'")

            cur = con.cursor()
            cur.execute("SELECT nama, nama_suku,jk FROM data_art A LEFT JOIN m_suku B ON A.suku = B.kode_suku LIMIT " + str(self.numbertakedata))

            rows = cur.fetchall()




        except psycopg2.DatabaseError as e:
            print('Error %s' % e)
            sys.exit(1)


        finally:

            if con:
                con.close()

        import numpy as np
        train = np.array(rows[:self.numbertrain])
        test = np.array(rows[self.numbertest:])

        train_data = train[:, [0,1]]
        test_data = test[:, [0,1]]


        train_target = train[:, 2]
        test_target = test[:, 2]

        self.pipeline.fit(train_data, train_target)
        y = self.pipeline.predict(test_data)
        print(classification_report(y, test_target))

        # save model
        joblib.dump(self.pipeline, 'models/'+FILENAME_MODELNAMADANSUKU)

        docs_new = [['Anto', 'jawa'], ['Yani', 'jawa'], ['Nano', 'jawa'], ['Akmal', 'jawa'], ['Bagus', 'jawa']
            , ['Rahmi', 'jawa'], ['Amalia', 'jawa'], ['Aries', 'jawa'], ['Taufik', 'jawa'], ['Wahyu', 'jawa']
            , ['Adnan', 'jawa'], ['Steven', 'jawa'], ['Ricky', 'jawa']]
        # predicted = pipeline.predict(docs_new)
        predicted = self.pipeline.predict_proba(docs_new)

        for doc, category in zip(docs_new, predicted):
            print('%r - %r => %s' % (doc[0],(doc[1] if (doc[1] is None) is False else "") , category))

        return 'Success'

    def generatemodel(self):
        self.pipeline = Pipeline([
            # Extract the subject & body
            ('myfeature', CustomFeatureExtractor()),

            # Use FeatureUnion to combine the features from subject and body
            ('union', FeatureUnion(
                transformer_list=[

                    # Pipeline for pulling features from the post's subject line
                    ('prefix1', Pipeline([
                        ('selector', ItemSelector(key='prefix1')),
                        ('tfidf', TfidfVectorizer()),
                    ])),
                    # Pipeline for pulling features from the post's subject line
                    ('lastletter', Pipeline([
                        ('selector', ItemSelector(key='lastletter')),
                        ('tfidf', TfidfVectorizer()),
                    ])),

                    # # Pipeline for standard bag-of-words model for body
                    # ('body_bow', Pipeline([
                    #     ('selector', ItemSelector(key='body')),
                    #     ('tfidf', TfidfVectorizer()),
                    #     ('best', TruncatedSVD(n_components=50)),
                    # ])),
                    #
                    # # Pipeline for pulling ad hoc features from post's body
                    # ('body_stats', Pipeline([
                    #     ('selector', ItemSelector(key='body')),
                    #     ('stats', TextStats()),  # returns a list of dicts
                    #     ('vect', DictVectorizer()),  # list of dicts -> feature matrix
                    # ])),

                ],

                # weight components in FeatureUnion
                transformer_weights={
                    'prefix1': 1.0,
                    'lastletter': 0.9,
                    # 'subject': 0.8,
                    # 'body_bow': 0.5,
                    # 'body_stats': 1.0,
                },
            )),

            # Use a SVC classifier on the combined features
            ('svc', SVC(
                # kernel='poly', degree=3, C=C
                # kernel = 'linear'
                kernel='rbf', gamma=0.7, C=self.C, probability=True
                # C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=True, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None, random_state=None
            )),
        ])


        con = None
        rows = None
        try:

            con = psycopg2.connect("dbname='genderid' user='postgres' password='root'")

            cur = con.cursor()
            cur.execute("SELECT nama,jk FROM data_art LIMIT " + str(self.numbertakedata))

            rows = cur.fetchall()




        except psycopg2.DatabaseError as e:
            print('Error %s' % e)
            sys.exit(1)


        finally:

            if con:
                con.close()

        import numpy as np
        train = np.array(rows[:self.numbertrain])
        test = np.array(rows[self.numbertest:])

        train_data = train[:, 0]
        test_data = test[:, 0]

        train_target = train[:, 1]
        test_target = test[:, 1]

        # for (i, a) in enumerate(train):
        #     print(train_data[i] + " " + train_target[i])

        # # limit the list of categories to make running this example faster.
        # categories = ['alt.atheism', 'talk.religion.misc']
        # train = fetch_20newsgroups(random_state=1,
        #                            subset='train',
        #                            categories=categories,
        #                            )
        # test = fetch_20newsgroups(random_state=1,
        #                           subset='test',
        #                           categories=categories,
        #                           )

        self.pipeline.fit(train_data, train_target)
        y = self.pipeline.predict(test_data)
        print(classification_report(y, test_target))

        # save model
        joblib.dump(self.pipeline, 'models/filename.pkl')

        docs_new = ['Anto', 'Yani', 'Nano', 'Akmal', 'Bagus', 'Rahmi', 'Amalia', 'Aries', 'Taufik', 'Wahyu', 'Adnan',
                    'Steven', 'Ricky']
        # predicted = pipeline.predict(docs_new)
        predicted = self.pipeline.predict_proba(docs_new)

        for doc, category in zip(docs_new, predicted):
            print('%r => %s' % (doc, category))

        return 'Success'

    def predict(self, names, suku=''):
        print('start------------------------------')
        if suku is None or suku == "":
            return self.predictnama([names])

        print(names)
        print(suku)
        return self.predictnamaandsuku([[names, suku]])

    def predictnama(self, names):
        print('start nama------------------------------')
        if self.pipelinenama is None:
            self.pipelinenama = joblib.load(os.path.join(BASE_DIR, 'models/'+FILENAME_MODELNAMA))
        # docs_new = ['Anto', 'Yani', 'Nano', 'Akmal', 'Bagus', 'Rahmi', 'Amalia', 'Aries', 'Taufik', 'Wahyu', 'Adnan',
        #             'Steven', 'Ricky']
        predicted = self.pipelinenama.predict_proba(names)
        # prob = pipeline.predict_proba(docs_new)

        return predicted

    def predictnamaandsuku(self, namesukuarray):
        print('start suku------------------------------')
        if self.pipelinenamaandsuku is None:
            self.pipelinenamaandsuku = joblib.load(os.path.join(BASE_DIR, 'models/'+FILENAME_MODELNAMADANSUKU))
        # docs_new = ['Anto', 'Yani', 'Nano', 'Akmal', 'Bagus', 'Rahmi', 'Amalia', 'Aries', 'Taufik', 'Wahyu', 'Adnan',
        #             'Steven', 'Ricky']
        predicted = self.pipelinenamaandsuku.predict_proba(namesukuarray)
        # prob = pipeline.predict_proba(docs_new)

        return predicted

# gc = Genderclassify()
# gc.generatemodelbynameandsuku()