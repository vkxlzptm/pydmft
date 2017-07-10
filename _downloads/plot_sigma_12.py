# -*- coding: utf-8 -*-
r"""
======================================
The change of Sigma_12
======================================

"""

# Created Mon Mar  7 01:14:02 2016
# Author: Óscar Nájera

from __future__ import division, absolute_import, print_function

from math import log, ceil
import numpy as np
import matplotlib.pyplot as plt
import dmft.dimer as dimer
from dmft import ipt_imag
import dmft.common as gf


def ipt_u_tp(tprange, u_int, beta):

    tau, w_n = gf.tau_wn_setup(dict(BETA=beta, N_MATSUBARA=2**11))
    giw_d, giw_o = dimer.gf_met(w_n, 0., tprange[0], 0.5, 0.)

    giw_d, giw_o, loops = dimer.ipt_dmft_loop(
        beta, u_int + 3, tprange[0], giw_d, giw_o, tau, w_n, 1e-10)
    sigma = []

    for tp in tprange:
        giw_d, giw_o, loops = dimer.ipt_dmft_loop(
            beta, u_int, tp, giw_d, giw_o, tau, w_n, 1e-10)
        g0iw_d, g0iw_o = dimer.self_consistency(
            1j * w_n, 1j * giw_d.imag, giw_o.real, 0., tp, 0.25)
        siw_d, siw_o = ipt_imag.dimer_sigma(
            u_int, tp, g0iw_d, g0iw_o, tau, w_n)
        sigma.append(siw_o.real)

    return np.array(sigma)


tprange = np.arange(0.1, 1, 0.1)
BETA = 512.
tau, w_n = gf.tau_wn_setup(dict(BETA=BETA, N_MATSUBARA=2**11))
sigma = ipt_u_tp(tprange, 3, BETA)
plt.plot(w_n, sigma.T)
plt.show()
le = [np.polyfit(w_n[:2], s[:2], 1)[1] for s in sigma]
plt.plot(tprange, sigma[:, 0])
plt.plot(tprange, le + tprange)
plt.show()