"""
practica 4

simplre con ia para detectar dispositivo en tu red
"""

import os
import numpy as np
import sklearn.tree import DecisionTreeClassifier

#simulacion de datos
"""
caracteristicas: [tiempo_respuesta_ms]

"""

x = np.array({[10],[20],[30],[200],[300],[400]})
y = np.array({1,1,1,0,0,0})

"""
modelo ia
"""

modelo = DecisionTreeClassifier
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

    respuesta = os.popen(f"ping -n -w 100 (ip) ").read()

    if "tiempo=" in respuesta:

        try:
            tiempo = int(respuesta.split("tiempo="[1].split("ms") [0]))
        except:
             tiempo = 300
        
        else:
            tiempo = 400


            """
            prediccion con ia
            """

            predicion = modelo.predict([[tiempo]]) [0]

            if predicion == 1:
                print(f"dispositivo activa ia: {ip} - {tiempo} ms")

            else:
                print (f"dispositivo inactivo (ia): {ip} ")
                