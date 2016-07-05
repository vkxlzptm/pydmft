# -*- coding: utf-8 -*-
r"""
IPT in real frequencies
-----------------------
"""
# Author: Óscar Nájera

from __future__ import division, absolute_import, print_function
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import slaveparticles.quantum.dos as dos
import dmft.common as gf
plt.matplotlib.rcParams.update({'axes.labelsize': 22,
                                'axes.titlesize': 22, 'figure.autolayout': True})


def real_IPT_sigma(Aw, nf, U):
    Ap = Aw * nf
    Am = Aw * nf[::-1]
    App = signal.fftconvolve(Ap[::-1], Am, mode='same')
    Amm = signal.fftconvolve(Am[::-1], Ap, mode='same')
    Ampp = signal.fftconvolve(Am, App, mode='same')
    Apmm = signal.fftconvolve(Ap, Amm, mode='same')
    return -np.pi * U**2 * (Apmm + Ampp)


def dimer_solver(w, dw, tp, U, nfp, gss, gsa):
    # Self consistency in diagonal basis
    g0ss = 1 / (w + 3e-3j - tp - .25 * gss)
    g0sa = 1 / (w + 3e-3j + tp - .25 * gsa)

    # Rotate to local basis
    A0d = -0.5 * (g0ss + g0sa).imag / np.pi
    A0o = -0.5 * (g0ss - g0sa).imag / np.pi
    # Cleaning for PH and half-fill
    A0d = 0.5 * (A0d + A0d[::-1])
    A0o = 0.5 * (A0o - A0o[::-1])  # * tp

    # Second order diagram
    isd = real_IPT_sigma(A0d, nfp, U) * dw * dw
    iso = real_IPT_sigma(A0o, nfp, U) * dw * dw

    # Rotate to diagonal basis
    iss = isd + iso
    isa = isd - iso

    # Kramers-Kronig relation, uses Fourier Transform to speed convolution
    rss = -signal.hilbert(iss, len(iss) * 4)[:len(iss)].imag
    rsa = -signal.hilbert(isa, len(isa) * 4)[:len(isa)].imag

    # Semi-circle Hilbert Transform
    ss = rss - 1j * np.abs(iss)
    gss = gf.semi_circle_hiltrans(w - tp - ss)
    sa = rsa - 1j * np.abs(isa)
    gsa = gf.semi_circle_hiltrans(w + tp - sa)

    return (gss, gsa), (ss, sa)


def dimer_dmft(U, tp, nfp, w, dw, gss, gsa):

    converged = False
    loops = 0
    while not converged:
        gss_old = gss.copy()
        gsa_old = gsa.copy()
        (gss, gsa), (ss, sa) = dimer_solver(w, dw, tp, U, nfp, gss, gsa)
        converged = np.allclose(gss_old, gss)
        converged *= np.allclose(gsa_old, gsa)
        loops += 1
        if loops > 3000:
            converged = True
            print('Failed to converge in less than 3000 iterations')

    return (gss, gsa), (ss, sa)
