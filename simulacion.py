import numpy as np
import random
from scipy import stats
import sys

## variables de control
cant2 = 8500
cant16 = 12000
cant125 =50000
imp = 30

## TEF
tpllmp = 0
tpllp = 0

##resultado
pkp2 = 0
pkp16 = 0
pkp125 = 0
pmps2 = 0
pmps16 =0
pmps125 = 0


#sumatorias

smps2 = 0
smps16 = 0
smps125 = 0
perdida2 = 0
perdida16 = 0
perdida125 = 0
ganancia = 0


t = 0
tf = 50010
staActual2 = 0
staActual16 = 0
staActual125 = 0
kg = 0
espesor = 0
ip = 0
nt = 0
tope = 300000

def intervaloPedido():
    intervalo = stats.pearson3.rvs(skew = 2.237830897269321,loc = 0.14514574269715144,scale = 0.16240581380739422, random_state=None)
    return intervalo
def generarKG():
    sinRedondear = 12001
    while sinRedondear > 12000:
        sinRedondear = stats.foldcauchy.rvs(c = 0.04378797938418702,loc = 199.99998479055455,scale = 389.4065466129497,random_state=None)
    return sinRedondear - sinRedondear%10
def generarEspesor():
    return stats.halfgennorm.rvs(beta = 0.7644947456920824,loc = 0.29999999967008933,scale = 0.5613952812257972, random_state=None)
cantSepaso = 0
while(t < tf):
    if int(tpllp) < tpllmp:
        ##rama pedido
        t = tpllp
        ip = intervaloPedido()
        tpllp = t + ip
        kg = generarKG()
        # print(kg)
        espesor = generarEspesor()
        if espesor < 2 and espesor > 0.7:
            nt += 1
            # ganancia += kg*cm
            if espesor > 1.6:
                if kg > staActual2:
                    perdida2 += 1
                else:
                    staActual2 -= kg
            else:
                if espesor > 1.25:
                    if kg > staActual16:
                        perdida16 += 1
                    else:
                        staActual16 -= kg
                else:
                    if kg > staActual125:
                        perdida125 += 1
                    else:
                        staActual125 -= kg

    else:
        ##rama compra
        t = tpllmp
        tpllmp = t + imp
        smps2 += staActual2
        smps16 += staActual16
        smps125 += staActual125
        # ganancia -= staActual2*ca
        if staActual2 + cant2 +staActual16 + cant16 + staActual125 + cant125 < tope:
            staActual2 += cant2
            staActual16 += cant16
            staActual125 += cant125

pkp2 = perdida2*100/nt
pkp16 = perdida16*100/nt
pkp125 = perdida125*100/nt

pmps2 = (smps2/t)*imp
pmps16 = smps16*imp/t
pmps125 = smps125*imp/t

print("porcentaje de pedidos de materia prima de 2.0 rechazados = ",pkp2)
print("porcentaje de pedidos de materia prima de 1.6 rechazados = ",pkp16)
print("porcentaje de pedidos de materia prima de 1.25 rechazados = ",pkp125)
print("promedio de materia prima de 2.0 sobrante por intervalo = ",pmps2)
print("promedio de materia prima de 1.6 sobrante por intervalo = ",pmps16)
print("promedio de materia prima de 1.25 sobrante por intervalo = ",pmps125)
