# -*- coding: utf-8 -*-


cimport numpy as np
import cython
from libc.math cimport exp, sqrt

cdef extern from "hfc.h":
    void cgnew(size_t N, double *g, double dv, int k)

def gnew(np.ndarray[np.float64_t, ndim=2] g, double dv, int k):
    cdef int N=g.shape[0]
    cgnew(N, &g[0,0], dv, k)


cdef extern from "gsl/gsl_rng.h":
    ctypedef struct gsl_rng_type:
        pass
    ctypedef struct gsl_rng:
        pass
    gsl_rng_type *gsl_rng_mt19937
    gsl_rng *gsl_rng_alloc(gsl_rng_type * T)
    double uniform "gsl_rng_uniform"(gsl_rng *r)

cdef extern from "gsl/gsl_randist.h":
    double normal "gsl_ran_gaussian"(gsl_rng *r, double sigma)

cdef gsl_rng *r = gsl_rng_alloc(gsl_rng_mt19937)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef updateDHS(np.ndarray[np.float64_t, ndim=2] gup,
             np.ndarray[np.float64_t, ndim=2] gdw,
             np.ndarray[np.float64_t, ndim=1] v):
    cdef double dv, ratup, ratdw, rat
    cdef int j, i, up, dw, pair, N=v.shape[0]
    for j in range(N):
        dv = 2.*v[j]
        ratup = 1. + (1. - gup[j, j])*(exp(-dv)-1.)
        ratdw = 1. + (1. - gdw[j, j])*(exp( dv)-1.)
        rat = ratup * ratdw
        rat = rat/(1.+rat)
        if rat > uniform(r):
            v[j] *= -1.
            cgnew(N, &gup[0,0], -dv, j)
            cgnew(N, &gdw[0,0],  dv, j)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef updateCHS(np.ndarray[np.float64_t, ndim=2] gup,
             np.ndarray[np.float64_t, ndim=2] gdw,
             np.ndarray[np.float64_t, ndim=1] v,
             double U, double dtau):
    cdef double Vjp, dv, ratup, ratdw, rat, gauss_weight
    cdef int j, i, up, dw, pair, N=v.shape[0]
    for j in range(N):
        Vjp = -1.* dtau * normal(r, sqrt(U/dtau) )
        dv = Vjp - v[j]
        ratup = 1. + (1. - gup[j, j])*(exp( dv)-1.)
        ratdw = 1. + (1. - gdw[j, j])*(exp(-dv)-1.)
        rat = ratup * ratdw
        gauss_weight = exp((Vjp*Vjp-v[j]*v[j])/(2*U*dtau))
        rat = rat/(gauss_weight+rat)
        if rat > uniform(r):
            v[j] = Vjp
            cgnew(N, &gup[0,0],  dv, j)
            cgnew(N, &gdw[0,0], -dv, j)
