#!/usr/bin/env python

import numpy as np
from base import Experiment, FilteredRankingEval
from skge import TransE, PairwiseStochasticTrainer
from skge.param import init_nunif
import logging
import pdb

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('EX-KG')

class TransEEval(FilteredRankingEval):

    def prepare(self, mdl, p):
        pdb.set_trace()
        # Do the subject + predicate (add the embeddings of relations "P" to all entities)
        self.ER = mdl.E + mdl.R[p]

    def scores_o(self, mdl, s, p):
        pdb.set_trace()
        # Subtract embeddings of every entity from the "S"ubject
        return -np.sum(np.abs(self.ER[s] - mdl.E), axis=1)

    def scores_s(self, mdl, o, p):
        pdb.set_trace()
        # Subtract embeddings of the "O"bject from the S + P 
        return -np.sum(np.abs(self.ER - mdl.E[o]), axis=1)


class ExpTransE(Experiment):

    def __init__(self):
        super(ExpTransE, self).__init__()
        self.parser.add_argument('--ncomp', type=int, help='Number of latent components')
        self.evaluator = TransEEval

    def setup_trainer(self, sz, sampler):
        norm = True if self.args.norm == 'l1' else False
        model = TransE(sz, self.args.ncomp, l1=norm, init=self.args.init)
        #pdb.set_trace()
        log.info(" sz = %s  and init_nunif = %d" %( sz, init_nunif.counter))
        #pdb.set_trace()
        # Here the model is initialized (TransE())
        trainer = PairwiseStochasticTrainer(
            model,
            nbatches=self.args.nb,
            margin=self.args.margin,
            max_epochs=self.args.me,
            learning_rate=self.args.lr,
            samplef=sampler.sample,
            post_epoch=[self.callback]
        )
        return trainer

if __name__ == '__main__':
    ExpTransE().run()
