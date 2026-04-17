#practica 2 deteccion de localhost

from scapy.all import ARP, Ether, srp, sniff
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


"""
escaneo de red
"""

def escanear_red(ip_range="192.168.1.1/24"):
    print("escaneando dispositivos...")

    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    paquete = ether / arp 

    resultado = srp(paquete, timeout=2, verbose=0)[0]

    dispositivos = []
    for enviado, recibido in resultado:
        dispositivos.append({
            "ip": recibido.psrc,
            "mac": recibido.hwsrc
        })
        
    return dispositivos
    
"""
captura de trafico
"""
    
trafico = []

def captura_paquetes(packet):
    if packet.haslayer("IP"):
        trafico.append({
            "ip": packet["IP"].src,
            "longitud": len(packet),
            "protocolo": packet["IP"].proto
        })

def anailizar_trafico(tiempo=10):
    print("capturando trafico...")
    sniff(prn=captura_paquetes, timeout=tiempo)
    return pd.DataFrame(trafico)

import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier

#simulacion de datos
"""
caracteristicas: [tiempo_respuesta_ms]
"""

x = np.array([[10],[20],[30],[200],[300],[400]])
y = np.array([1,1,1,0,0,0])

"""
modelo ia
"""

modelo = DecisionTreeClassifier()
modelo.fit(x,y)

"""
escaneo de red
"""
red = "192.168.1."

for i in range (1, 20):
    ip = red + str(i)
    
    """
    pinng window
    """

    respuesta = os.popen(f"ping -n 1 -w 100 {ip}").read()

    if "tiempo=" in respuesta:

        try:
            tiempo = int(respuesta.split("tiempo=")[1].split("ms")[0])
        except:
            tiempo = 300
        
        """
        prediccion con ia
        """

        predicion = modelo.predict([[tiempo]])[0]

        if predicion == 1:
            print(f"dispositivo activo (ia): {ip} - {tiempo} ms")

        else:
            print(f"dispositivo inactivo (ia): {ip}")

    else:
        tiempo = 400

        predicion = modelo.predict([[tiempo]])[0]

        print(f"dispositivo sospechoso (ia): {ip}")