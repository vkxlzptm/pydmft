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
import dmft.common as gf
plt.matplotlib.rcParams.update({'axes.labelsize': 22,
                                'axes.titlesize': 22, 'figure.autolayout': True})


def sigma(Aw, nf, U):
    Ap = Aw * nf
    Am = Aw * nf[::-1]
    App = signal.fftconvolve(Ap[::-1], Am, mode='same')
    Amm = signal.fftconvolve(Am[::-1], Ap, mode='same')
    Ampp = signal.fftconvolve(Am, App, mode='same')
    Apmm = signal.fftconvolve(Ap, Amm, mode='same')
    return -np.pi * U**2 * (Apmm + Ampp)


def ph_hf_sigma(Aw, nf, U):
    """Imaginary part of the second order diagram

    because of particle-hole symmetry at half-fill in the Single band
    one can work with A^+ only"""

    Ap = Aw * nf
    # convolution A^+ * A^+
    App = signal.fftconvolve(Ap, Ap, mode='same')
    # convolution A^-(-w) * App
    Appp = signal.fftconvolve(Ap, App, mode='same')
    return -np.pi * U**2 * (Appp + Appp[::-1])


def ss_dmft_loop(gloc, w, u_int, beta, conv):
    """DMFT Loop for the single band Hubbard Model at Half-Filling


    Parameters
    ----------
    gloc : complex 1D ndarray
        local Green's function to use as seed
    w : real 1D ndarray
        real frequency points
    u_int : float
        On site interaction, Hubbard U
    beta : float
        Inverse temperature
    conv : float
        convergence criteria

    Returns
    -------
    gloc : complex 1D ndarray
        DMFT iterated local Green's function
    sigma : complex 1D ndarray
        DMFT iterated self-energy

"""

    dw = w[1] - w[0]
    eta = 2j * dw
    nf = gf.fermi_dist(w, beta)

    converged = False
    while not converged:

        gloc_old = gloc.copy()
        # Self-consistency
        g0 = 1 / (w + eta - .25 * gloc)
        # Spectral-function of Weiss field
        A0 = -g0.imag / np.pi

        # Second order diagram
        isi = ph_hf_sigma(A0, nf, u_int) * dw * dw
        isi = 0.5 * (isi + isi[::-1])

        # Kramers-Kronig relation, uses Fourier Transform to speed convolution
        hsi = -signal.hilbert(isi, len(isi) * 4)[:len(isi)].imag
        sigma = hsi + 1j * isi

        # Semi-circle Hilbert Transform
        gloc = gf.semi_circle_hiltrans(w - sigma)
        converged = np.allclose(gloc, gloc_old, atol=conv)

    return gloc, sigma


def ss_dmft_loop_once(gloc, w, u_int, beta, conv):
    """DMFT Loop for the single band Hubbard Model at Half-Filling
    *loop only once.*

    Parameters
    ----------
    gloc : complex 1D ndarray
        local Green's function to use as seed
    w : real 1D ndarray
        real frequency points
    u_int : float
        On site interaction, Hubbard U
    beta : float
        Inverse temperature
    conv : float
        convergence criteria

    Returns
    -------
    gloc : complex 1D ndarray
        DMFT iterated local Green's function
    sigma : complex 1D ndarray
        DMFT iterated self-energy

"""

    dw = w[1] - w[0]
    eta = 2j * dw
    nf = gf.fermi_dist(w, beta)

    converged = False
    while not converged:

        gloc_old = gloc.copy()
        # Self-consistency
        g0 = 1 / (w + eta - .25 * gloc)
        # Spectral-function of Weiss field
        A0 = -g0.imag / np.pi

        # Second order diagram
        isi = ph_hf_sigma(A0, nf, u_int) * dw * dw
        isi = 0.5 * (isi + isi[::-1])

        # Kramers-Kronig relation, uses Fourier Transform to speed convolution
        hsi = -signal.hilbert(isi, len(isi) * 4)[:len(isi)].imag
        sigma = hsi + 1j * isi

        # Semi-circle Hilbert Transform
        gloc = gf.semi_circle_hiltrans(w - sigma)
        converged = np.allclose(gloc, gloc_old, atol=conv)
        converged = True
    return gloc, sigma


def ss_dmft_loop_D(gloc, w, u_int, beta, conv, D=1):
    """DMFT Loop for the single band Hubbard Model at Half-Filling


    Parameters
    ----------
    gloc : complex 1D ndarray
        local Green's function to use as seed
    w : real 1D ndarray
        real frequency points
    u_int : float
        On site interaction, Hubbard U
    beta : float
        Inverse temperature
    conv : float
        convergence criteria

    Returns
    -------
    gloc : complex 1D ndarray
        DMFT iterated local Green's function
    sigma : complex 1D ndarray
        DMFT iterated self-energy

"""

    dw = w[1] - w[0]
    eta = 2j * dw
    nf = gf.fermi_dist(w, beta)

    converged = False
    while not converged:

        gloc_old = gloc.copy()
        # Self-consistency
        g0 = 1 / (w + eta - .25 * gloc)
        # Spectral-function of Weiss field
        A0 = -g0.imag / np.pi

        # Second order diagram
        isi = ph_hf_sigma(A0, nf, u_int) * dw * dw
        isi = 0.5 * (isi + isi[::-1])

        # Kramers-Kronig relation, uses Fourier Transform to speed convolution
        hsi = -signal.hilbert(isi, len(isi) * 4)[:len(isi)].imag
        sigma = hsi + 1j * isi

        # Semi-circle Hilbert Transform
        gloc = gf.semi_circle_hiltrans(w - sigma, D=D)
        converged = np.allclose(gloc, gloc_old, atol=conv)

    return gloc, sigma


def ss_dmft_loop_t(gloc, w, u_int, beta, conv, t=0.5):
    """DMFT Loop for the single band Hubbard Model at Half-Filling


    Parameters
    ----------
    gloc : complex 1D ndarray
        local Green's function to use as seed
    w : real 1D ndarray
        real frequency points
    u_int : float
        On site interaction, Hubbard U
    beta : float
        Inverse temperature
    conv : float
        convergence criteria

    Returns
    -------
    gloc : complex 1D ndarray
        DMFT iterated local Green's function
    sigma : complex 1D ndarray
        DMFT iterated self-energy

"""

    dw = w[1] - w[0]
    eta = 2j * dw
    nf = gf.fermi_dist(w, beta)

    converged = False
    while not converged:

        gloc_old = gloc.copy()
        # Self-consistency
        g0 = 1 / (w + eta - t*t * gloc)
        # Spectral-function of Weiss field
        A0 = -g0.imag / np.pi

        # Second order diagram
        isi = ph_hf_sigma(A0, nf, u_int) * dw * dw
        isi = 0.5 * (isi + isi[::-1])

        # Kramers-Kronig relation, uses Fourier Transform to speed convolution
        hsi = -signal.hilbert(isi, len(isi) * 4)[:len(isi)].imag
        sigma = hsi + 1j * isi

        # Semi-circle Hilbert Transform
        gloc = gf.semi_circle_hiltrans(w - sigma)
        converged = np.allclose(gloc, gloc_old, atol=conv)

    return gloc, sigma




def dimer_solver(w, dw, tp, U, nfp, gss, gsa, t=0.5, eta=3e-3j):
    # Self consistency in diagonal basis
    g0ss = 1 / (w + eta - tp - t * t * gss)
    g0sa = 1 / (w + eta + tp - t * t * gsa)

    # Rotate to local basis
    A0d = -0.5 * (g0ss + g0sa).imag / np.pi
    A0o = -0.5 * (g0ss - g0sa).imag / np.pi
    # Cleaning for PH and half-fill
    A0d = 0.5 * (A0d + A0d[::-1])
    A0o = 0.5 * (A0o - A0o[::-1])  # * tp

    # Second order diagram
    isd = sigma(A0d, nfp, U) * dw * dw
    iso = sigma(A0o, nfp, U) * dw * dw

    # Rotate to diagonal basis
    iss = isd + iso
    isa = isd - iso

    # Kramers-Kronig relation, uses Fourier Transform to speed convolution
    rss = -signal.hilbert(iss, len(iss) * 4)[:len(iss)].imag
    rsa = -signal.hilbert(isa, len(isa) * 4)[:len(isa)].imag

    # Semi-circle Hilbert Transform
    ss = rss - 1j * np.abs(iss)
    gss = gf.semi_circle_hiltrans(w - tp - ss, 2 * t)
    sa = rsa - 1j * np.abs(isa)
    gsa = gf.semi_circle_hiltrans(w + tp - sa, 2 * t)

    return (gss, gsa), (ss, sa)


def dimer_dmft(U, tp, nfp, w, dw, gss, gsa, conv=1e-7, t=0.5):
    """Solve DMFT equations in real frequencies for the dimer

    Parameters
    ----------
    U : float
        Couloumb interaction
    tp : float
        Dimerization
    npf : 1D real ndarray
        Thermal Fermi function
    w : 1D real ndarray
        frequency grid. Has to be equispaced and symmetric
    dw : float
        frequency separation
    gss : 1D complex ndarray
        Starting guess for the symmetric Green function
    gsa : 1D complex ndarray
        Starting guess for the asymmetric Green function
    conv : float
        convergence criteria
    t : float
        hopping

    Returns
    -------
    (gss, gsa) : tuple of 1D complex ndarray, Green Functions
    (ss, sa) : tuple of 1D complex ndarray, Self-Energy

    """

    converged = False
    loops = 0
    while not converged:
        gss_old = gss.copy()
        gsa_old = gsa.copy()
        (gss, gsa), (ss, sa) = dimer_solver(w, dw, tp, U, nfp, gss, gsa, t)
        converged = np.allclose(gss_old, gss, atol=conv)
        converged *= np.allclose(gsa_old, gsa, atol=conv)
        loops += 1
        if loops > 3000:
            converged = True
            print('Failed to converge in less than 3000 iterations')

    return (gss, gsa), (ss, sa)
