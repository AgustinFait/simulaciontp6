import numpy as np
import random
from scipy import stats
import sys

tf = 50000

total_comprado2=0

## variables de control
cant2 = 20000#8500
cant16 = 20000#11500
cant125 = 50000#60000
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
kg2pedidos = 0
kg16pedidos = 0
kg125pedidos = 0
kg2perdidos = 0
kg125perdidos = 0
kg16perdidos =  0
cantSepaso = 0



t = 0
staActual2 = 0
staActual16 = 0
staActual125 = 0
kg = 0
espesor = 0
ip = 0
nt = 0
tope = 500000

def intervaloPedido():
    intervalo = stats.pearson3.rvs(skew = 2.237830897269321,loc = 0.14514574269715144,scale = 0.16240581380739422, random_state=None)
    return intervalo
def generarKG():
    sinRedondear = stats.foldcauchy.rvs(c = 0.04378797938418702,loc = 199.99998479055455,scale = 089.4065466129497,random_state=None)
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
            if espesor > 1.6:
                kg2pedidos+=kg
                if kg > staActual2:
                    kg2perdidos += kg
                else:
                    staActual2 -= kg
            else:
                if espesor > 1.25:
                    kg16pedidos+=kg
                    if kg > staActual16:
                        kg16perdidos += kg
                    else:
                        staActual16 -= kg
                else:
                    kg125pedidos+=kg
                    if kg > staActual125:
                        kg125perdidos += kg
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
            total_comprado2 +=cant2
            staActual16 += cant16
            staActual125 += cant125
        else:
            cantSepaso+=1
            libre = tope - (staActual125 + staActual16 + staActual2)
            staActual2 += libre * cant2 / (cant2 + cant125 + cant16)
            staActual16 += libre * cant16 / (cant2 + cant125 + cant16)
            staActual125 += libre * cant125 / (cant2 + cant125 + cant16)
            


pmps2 = (smps2/t)*imp
pmps16 = smps16*imp/t
pmps125 = smps125*imp/t

print("")
print("promedio de materia prima de 2.0 sobrante por intervalo = ",pmps2)
print("promedio de materia prima de 1.6 sobrante por intervalo = ",pmps16)
print("promedio de materia prima de 1.25 sobrante por intervalo = ",pmps125)
print("")

print("Compra_2.00",cant2)
print("Compra_1.60",cant16)
print("Compra_1.25",cant125)
print("")
print("tf",tf)


print("")
if cantSepaso > 0:
    print("Intervalo promedio entre depósito lleno",tf/cantSepaso)
print("kg_perdidos_2 / kg_pedidos_2 [%] = ",kg2perdidos*100/kg2pedidos)
print("kg_perdidos_16 / kg_pedidos_16 [%] = ",kg16perdidos*100/kg16pedidos)
print("kg_perdidos_125 / kg_pedidos_125 [%] = ",kg125perdidos*100/kg125pedidos)
print("kg_pedidos_totales / dias = ", (kg125pedidos + kg16pedidos + kg2pedidos)/t)
print("kg_perdidos_totales / dias = ", (kg125perdidos + kg16perdidos + kg2perdidos)/t)
print("\033[32mOcupación promedio del depósito por intervalo [%] = ", (tope - (pmps2+pmps16+pmps125))*100/tope)
print("kg_perdidos_totales / kg_pedidos_totales [%] = ", (kg125perdidos + kg16perdidos + kg2perdidos)*100/(kg125pedidos + kg16pedidos + kg2pedidos))

print("\033[0m")