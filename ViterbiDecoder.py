#! /usr/bin/env python
# title           : ViterbiDecoder.py
# description     : This class implements a viterbi decoder. Its input is a trellis instance.
# author          : Felix Arnold
# python_version  : 3.5.2


class ViterbiDecoder(object):

    def __init__(self, trellis):
        self.state = 0
        self.trellis = trellis

    def decode(self, encoded_rx, n_data):

        trellis = self.trellis
        n_stages = n_data + trellis.K - 1

        # forward state metric calculation
        sm_vec = [0] + [-10] * (trellis.Ns - 1)  # init state metric vector
        decisions = []
        for i in range(0, n_stages):  # for each stage
            decisions_stage = []
            sm_vec_new = []
            llr = encoded_rx[trellis.r * i:trellis.r * (i + 1)]
            for j in range(trellis.Ns):  # for each state
                branches = trellis.get_prev_branches(j)
                sums = []
                for k in range(2):  # for each branch
                    branch_metric = 0
                    for l in range(trellis.r):  # for each encoded bit
                        if trellis.get_enc_bits(branches[k])[l] == 1:
                            branch_metric = branch_metric + llr[l]  # add
                    sums.append(sm_vec[trellis.get_prev_state(branches[k])] + branch_metric)
                decision = int(sums[1] > sums[0])  # compare
                sm_vec_new.append(sums[decision])  # select
                decisions_stage.append(decision)
            sm_vec = list(sm_vec_new)
            decisions.append(decisions_stage)

        # traceback
        state = 0  # start state #sm_vec.index(max(sm_vec))
        data_r = []
        for i in reversed(range(n_stages)):  # loop over all stages backwards
            decision = decisions[i][state]
            # if i < n_data:  # remove zero termination
            #    data_r = [trellis.get_prev_dat(state)] + data_r
            branch_taken = trellis.get_prev_branch(state, decision)
            if i < n_data:  # remove zero termination
                data_r = [trellis.get_dat(branch_taken)] + data_r
            state = trellis.get_prev_state(branch_taken)

        return data_r
