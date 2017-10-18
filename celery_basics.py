from collections import Counter

from celery import Celery

# Create Celery app
from scipy.spatial.distance import cosine

app = Celery("pycon", backend='rpc://', logging="info", broker='amqp://')
app.conf.update(CELERY_ACCEPT_CONTENT=['pickle', 'json'])

'''
Create a basic add task which has two input parameters and return the sum of parameters
'''

import logging


@app.task(name='pycon.add')
def add(*args):
    logging.info(args)
    return sum(args)


@app.task(name='pycon.make_pi')
def make_pi(num_calcs):
    logging.info(num_calcs)
    pi = 0.0
    for k in xrange(num_calcs):
        pi += 4 * ((-1) ** k / ((2.0 * k) + 1))
    return pi


@app.task(ignore_results=True)
def apply_function(func, data):
    logging.info(data)
    return func(data)


@app.task()
def apply_counter(df):
    import pickle
    df = pickle.loads(df)
    logging.info(str(df.shape))
    return pickle.dumps(df.summary.apply(lambda x: Counter(str(x).split(" "))).values.sum())

cosine