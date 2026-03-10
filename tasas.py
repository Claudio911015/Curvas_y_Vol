# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline

class Interpolator:
    def interpolate(ts,ps):
        pass

class LogLinearInterpolator(Interpolator):
    def interpolate(self,ts,ps,t):
        #ps: factor de descuento
        #ts : tenors
        rts= [-np.log(p) for p in ps]
        interpolator = interp1d(ts, rts)
        return interpolator(t)/t
    
class LinearInterpolator(Interpolator):
    #Interpolación lineal sobre tasas simples
    def interpolate(self,ts,ps,t):
        rs = [-np.log(p) / t_   for (t_,p) in zip(ts, ps)]
        interpolator = interp1d(ts, rs)
        return interpolator(t)
    
class SplineInterpolator(Interpolator):
    #Interpolación spline sobre tasas simples
    def interpolate(self,ts,ps,t):
        rs = [-np.log(p) / t_   for (t_,p) in zip(ts, ps)]
        interpolator = CubicSpline(ts, rs)
        return interpolator(t)
    
class LogLinearSplineInterpolator(Interpolator):
    #Interpolación spline sobre tasas simples
    def interpolate(self,ts,ps,t):
        if t > 5:
            rs = [-np.log(p) / t_   for (t_,p) in zip(ts, ps)]
            interpolator = CubicSpline(ts, rs)
            return interpolator(t)
        else:
            rts= [-np.log(p) for p in ps]
            interpolator = interp1d(ts, rts)
            return interpolator(t)/t
        
class Curva: 
    # ts: lista con tenors/vencimientos asociados a los factores de descuento
    # ps: lista con factores de descuento
    def __init__(self,obj, ts, ps):
        self._ts = ts 
        self._ps = ps 
        self._interp = obj
        
    def get_ts(self):
        return self._ts
    
    def get_ps(self):
        return self._ps
    
    def descuento(self, t):
        rs= [-np.log(p)/t_ for (p,t_) in zip(self._ps,self._ts)]
        if (t >= self._ts[-1]):
            r =  rs[-1]
        elif (t <= self._ts[0]):
            r = rs[0]
        else:
            r = self._interp.interpolate(self._ts,self._ps,t)
        p = np.exp( - r * t)
        return p
    
    def tasa_forward(self, t1, t2):
        p1 = self.descuento(t1)
        p2 = self.descuento(t2)
        forward = ((p1 / p2) - 1.) / (t2 -  t1)
        return forward
    
    def agregar_nodo(self, t, p):
        self._ts.append(t)
        self._ps.append(p)
        
    def cambiar_ultimo_nodo(self, p):
        self._ps[-1] = p