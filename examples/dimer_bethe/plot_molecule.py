# -*- coding: utf-8 -*-
"""
===================================
Isolated molecule spectral function
===================================

For the case of contact interaction in the di-atomic molecule case
spectral function are evaluated by means of the Lehmann representation
"""
# author: Óscar Nájera

from __future__ import division, absolute_import, print_function
from dmft.common import matsubara_freq, gw_invfouriertrans
import dmft.RKKY_dimer as rt
from itertools import product
import slaveparticles.quantum.operators as op
import matplotlib.pyplot as plt
import numpy as np


def plot_real_gf(eig_e, eig_v, oper_pair, c_v, names):
    _, axw = plt.subplots(2, sharex=True)
    w = np.linspace(-1.5, 1.5, 500) + 1j*1e-2
    gfs = [op.gf_lehmann(eig_e, eig_v, c.T, beta, w, d) for c, d in oper_pair]
    for gw, color, name in zip(gfs, c_v, names):
        axw[0].plot(w.real, gw.real, color, label=r'${}$'.format(name))
        axw[1].plot(w.real, -1*gw.imag/np.pi, color)
        axw[0].legend()
        axw[0].set_title(r'Real Frequencies Green functions, $\beta={}$'.format(beta))
        axw[0].set_ylabel(r'$\Re e G(\omega)$')
        axw[1].set_ylabel(r'$A(\omega)$')
        axw[1].set_xlabel(r'$\omega$')


def plot_matsubara_gf(eig_e, eig_v, oper_pair, c_v, names):
    gwp, axwn = plt.subplots(2, sharex=True)
    gwp.subplots_adjust(hspace=0)
    gtp, axt = plt.subplots()
    wn = matsubara_freq(beta, beta)
    tau = np.arange(0, beta, .5)
    gfs = [op.gf_lehmann(eig_e, eig_v, c.T, beta, 1j*wn, d) for c, d in oper_pair]
    for giw, color, name in zip(gfs, c_v, names):
        axwn[0].plot(wn, giw.real, color+'s-', label=r'${}$'.format(name))
        axwn[1].plot(wn, giw.imag, color+'o-')

        tail =  [0., tp, 0.] if name[0]!=name[1] else [1., 0., 0.]
        gt = gw_invfouriertrans(giw, tau, wn, tail)
        axt.plot(tau, gt, label=r'${}$'.format(name))

        axwn[0].legend()
        axwn[0].set_title(r'Matsubara Green functions, $\beta={}$'.format(beta))
        axwn[1].set_xlabel(r'$\omega_n$')
        axwn[0].set_ylabel(r'$\Re e G(i\omega_n)$')
        axwn[1].set_ylabel(r'$\Im m G(i\omega_n)$')

        axt.set_ylim(top=0.05)
        axt.legend(loc=0)
        axt.set_title(r'Imaginary time Green functions, $\beta={}$'.format(beta))
        axt.set_xlabel(r'$\tau$')
        axt.set_ylabel(r'$G(\tau)$')


beta = 50
U = 1.
mu = 0.
tp = 0.25
c_v = ['b', 'g', 'r', 'k']
names = [r'a\uparrow', r'a\downarrow', r'b\uparrow', r'b\downarrow']

h_at, oper = rt.dimer_hamiltonian(U, mu, tp)
eig_e, eig_v = op.diagonalize(h_at.todense())
oper_pair = list(product([oper[0], oper[2]], repeat=2))
names = list(product('AB', repeat=2))
plot_real_gf(eig_e, eig_v, oper_pair, c_v, names)
plot_matsubara_gf(eig_e, eig_v, oper_pair, c_v, names)


############################################################
# The symmetric and anti-symmetric bands
# ======================================
#

h_at, oper = rt.dimer_hamiltonian_bond(U, mu, tp)
eig_e, eig_v = op.diagonalize(h_at.todense())

oper_pair = product([oper[0], oper[2]], repeat=2)

#plot_real_gf(eig_e, eig_v, oper_pair, c_v, names)

# TODO: verify the asy/sym basis scale
# TODO: view in the local one the of diag terms
