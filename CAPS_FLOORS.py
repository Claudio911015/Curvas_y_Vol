#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 22:20:01 2023

@author: claudio
"""

import numpy as np
from scipy.stats import norm

# Función para valorar un caplet o floorlet
def valorar_caplet_floorlet(notional, strike, t_i, t_i1, volatilidad, tasa):
    d1 = (np.log(notional / strike) + (0.5 * volatilidad**2) * (t_i1 - t_i)) / (volatilidad * np.sqrt(t_i1 - t_i))
    d2 = d1 - volatilidad * np.sqrt(t_i1 - t_i)
    
    caplet = notional * (t_i1 - t_i) * (norm.cdf(d1) - norm.cdf(d2)) * np.exp(-tasa * t_i1)
    floorlet = notional * (t_i1 - t_i) * (norm.cdf(-d2) - norm.cdf(-d1)) * np.exp(-tasa * t_i1)
    
    return caplet, floorlet

# Parámetros generales
notional = 1000000  # Principal
strike = 0.03       # Tasa de interés de referencia
volatilidad = 0.2   # Volatilidad del mercado
tasa = 0.02         # Tasa libre de riesgo

# Fechas de observación y vencimiento
fechas_observacion = [0.25, 0.5, 0.75, 1.0]  # Ejemplo: Observaciones trimestrales
vencimiento = 1.0

# Valuación de caplets y floorlets para cada período
for i in range(len(fechas_observacion)):
    if i == 0:
        t_i = 0
    else:
        t_i = fechas_observacion[i-1]
    t_i1 = fechas_observacion[i]
    
    caplet, floorlet = valorar_caplet_floorlet(notional, strike, t_i, t_i1, volatilidad, tasa)
    
    print(f'Caplet {i+1} (T={t_i1}): {caplet:.2f}')
    print(f'Floorlet {i+1} (T={t_i1}): {floorlet:.2f}')

# Valor total del cap y floor
#valor_total_cap = np.sum(caplet for _, caplet in caplets)
#valor_total_floor = npsum(floorlet for _, floorlet in floorlets)

#print(f'Valor total del Cap: {valor_total_cap:.2f}')
#print(f'Valor total del Floor: {valor_total_floor:.2f}')
