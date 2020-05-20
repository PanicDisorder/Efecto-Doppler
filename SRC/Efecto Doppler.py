import numpy as nm
import matplotlib.pyplot as gra
from tkinter import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Proyecto para visualización del Efecto Doppler, UANL-FCFM 2020  #
# Autor; Victor Azael Guerra Riojas - 1580073                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Se necesita matplotlib, ipython, y numpy como modulos

class wave:
    def __init__(self, x, y):
        self.x = x                                                                      # Condicion inicial x
        self.y = y                                                                     # Condicion inicial y
        self.r = 0                                                                     # Radio inicial es cero
        self.wave = gra.Circle((x, y), self.r, facecolor='none', edgecolor='k')         # Generando grafica (Ondas negras)

    def updateWave(self, r):
        self.r = r                                                                      # Nuevo radio
        self.wave = gra.Circle((self.x,self.y),self.r,facecolor='none',edgecolor='k')   # Actualizar la onda

def repr(Dt, Freq, v_onda, v_foco, v_obs, L_x, L_y, d_x):

    gra.ion()
    fig = gra.figure(figsize=(7, 7))
    Graf1 = fig.add_subplot(221)                                                        # Grafico de la Onda
    Graf2 = fig.add_subplot(222)                                                        # Grafico frecuencia

    # Modificando longitudes de ejes
    s1 = abs(L_x)
    s2 = abs(L_y)

    Ondas_num = []                                                                      # Arreglo para guardar las ondas
    circle = []                                                                         # Arreglo para guardar los puntos de la onda

    #Tiempo para alcanzar
    if (v_foco > 0 and v_foco != v_obs):                                                # Tiempo para que se alcanzen foco y observador, si el foco se mueve hacia el observador
        tiempo_meet = d_x / (v_foco - v_obs)
    elif (v_foco != v_obs):                                                             # Tiempo para que se alcanzen foco y observador, si el foco se no mueve hacia el observador
        tiempo_meet = -1*d_x / (v_obs - v_foco)

    #Cordenadas iniciales
    xf_cord = (-1/2)*d_x
    xo_cord = (1/2)*d_x

    # Onda de la fuente
    Eje_x = Freq * 2                                                                    # Mostrando dos periodos de onda
    x = nm.arange(Eje_x)                                                                # Acomodando eje x
    y = nm.sin(2 * nm.pi * x / Freq)                                                    # Creando onda senoidal en base a la frecuencia
    Graf2.set_ylim(-1,1)

    i = 0

    while True:
        Graf1.cla()                                                                     # Limpiar los graficos
        Graf2.cla()

        Graf1.set_xlim([-s1,s1])                                                        # Longitud Eje x
        Graf1.set_ylim([-s2, s2])                                                       # longitud Eje y

        xf_cord += v_foco * Dt                                                          # Nueva cordenada (Foco) dependiendo del tiempo definido
        xo_cord += v_obs * Dt                                                           # Nueva cordenada (Obs.) dependiendo del tiempo definido

        Graf1.plot(xf_cord,0,'ro')                                                      # Graficando el Foco (depende del tiempo)
        Graf1.plot(xo_cord,0,'bo')                                                      # Graficando el Obs (depende del tiempo)

        #Calculo f y t
        s = round(Dt * i, 3)                                                            # Redondeo del tiempo (3 cifras sig.)


        #Datos f y t
        Graf1.text(L_x*0.7, L_y*0.8, s, color="k",fontsize=10)                          # Grafico del tiempo
        Graf1.text(L_x*0.5, L_y*0.8, 't =', color="k", fontsize=10)                     # Graf. tiempo

        if i%2 == 0:                                                                    # Separar las ondas del grafico 1, con diferencia de la cordenada del foco, en (i%4) se separan mucho las ondas
            circle.append(wave(xf_cord,0))

        if len (circle) > 50:                                                           # Limitar numero de ondas en pantalla
            del circle[0]

        Ondas = 0

        for cir in circle:
            cir.updateWave(cir.r+Dt*v_onda)                                             # Actualizar la nueva onda con un nuevo radio basado en xf_cord
            Graf1.add_artist(cir.wave)                                                  # Agregar Onda a el grafico

            x_temp = cir.x                                                              # Distancia que se movio el foco (obs)
            r_temp = cir.r                                                              # Radio ~ distancia que se movio

            d_dis = 1.0*x_temp - 1.0*xo_cord                                            # Distancia entre Foco y Obs.

            if abs(d_dis - r_temp) < 3.0*Dt*(v_onda + v_obs) :                        # Cuando la distancia entre foco y obs alcanze, la separacion entre ondas, cambiar el numero de la onda
                Ondas += 1

        Ondas_num.append(Ondas)                                                         # De lo anterior guardarlo en un arreglo con indice (Ondas)

        # Frecuencia del obs
        if (v_obs != v_foco):                                                       # Si existe diferencia entre las velocidades, estas se encontraran en algun momento, o se alejaran indefinidamente
            if ( v_foco > 0 ):                                                      # Confirmar direccion del foco (x+)
                if ( v_foco > abs(v_obs) ):                                         # Confirmar si se alcanzaran los dos puntos y la direccion del observador
                    if (s > tiempo_meet and tiempo_meet > 0):                       # Cuando el tiempo transcurrido sea mayor al tiempo donde se unen el foco y obs., se hace cambio de frecuencia
                        f_obs = (v_onda + v_obs) / (v_onda + v_foco)                # Despues de alcance
                    else:
                        f_obs = (v_onda + v_obs) / (v_onda - v_foco)                # Antes de alcanzar
                else:                                                               # No se alcanzaran
                    if (s > tiempo_meet and tiempo_meet > 0):                       # Solo cuando el foco y el obs. se acercan (este define si se encontraran o no)
                        f_obs = (v_onda + v_obs) / (v_onda + v_foco)                # Despues de alcance
                    else:
                        if (v_foco == abs(v_obs)):
                            f_obs = (v_onda - v_obs) / (v_onda - v_foco)            # Caso, Donde se acercan y luego se alejan
                        else:
                            f_obs = (v_onda + v_obs) / (v_onda - v_foco)            # Caso (no se encontraran)
            else:                                                                   # Direccion Foco (x-)
                if (v_foco > abs(v_obs) ):
                    if (s > tiempo_meet and tiempo_meet > 0):
                        f_obs = (v_onda - v_obs) / (v_onda + v_foco)
                    else:
                        f_obs = (v_onda - v_obs) / (v_onda - v_foco)
                else:
                    if (s > tiempo_meet and tiempo_meet > 0):
                        f_obs = (v_onda + v_obs) / (v_onda + v_foco)
                    else:
                        f_obs = (v_onda - v_obs) / (v_onda - v_foco)
        else:
            Graf2.plot(x, y, 'k', label="Freq. Original")                           # Graficando frecuencia original
            f_obs = 1                                                               # Si el foco y el obs. se mueven a la misma velocidad, establecer la frecuencia observada, como la frencuencia del foco

        #Graf1.text(L_x * 0.2, L_y * 0.4, f_obs, color="k", fontsize=10)            # Para checar la frecuencia observada en numeros

        x_d = nm.arange(Eje_x)                                                      # Establecer Eje x
        y_d = nm.sin(2 * nm.pi * x_d / (Freq*f_obs))                                # Graficar la frecuencia observada (Mayor y menor)

        if (f_obs < 1):                                                             # Cuando se aleja la fuente del obs, o el obs se aleja de la fuente
            Graf2.plot(x, y, 'k', label="Freq. Original")                           # Graficando frecuencia original
            Graf2.plot(x_d,y_d,'r')                                                 # Graficar en rojo
            f_obs = f_obs*100
            f_redondeada = round(f_obs,2)                                           # Redondeo de la frecuencia
            Graf2.text(0, 0.6, f_redondeada, color="r", fontsize=10)                # Agregar la frecuencia observada (redondeada), en la parte superior del segundo grafico en color rojo
        elif (f_obs > 1):                                                           # Cuando se acerca la fuente al obs, o el obs a la fuente
            Graf2.plot(x, y, 'k', label="Freq. Original")                           # Graficando frecuencia original
            Graf2.plot(x_d, y_d,'b')                                                # Graficar en azul
            f_obs = f_obs * 100
            f_redondeada = round(f_obs, 2)                                          # Redonde de la frecuencia
            Graf2.text(0, -0.6, f_redondeada, color="b", fontsize=10)               # Agregar la frecuencia obsrevada (redondeada), en la parte inferior del segundo grafico en color azul

        if len(Ondas_num) > 1:                                                      # Limpiar el arreglo para iniciar de nuevo el ciclo
            del Ondas_num[0]

        fig.canvas.draw()                                                           # Mandar a pantalla todos los graficos anteriores
        fig.canvas.flush_events()                                                   # Limpiar los graficos anteriores, para iniciar de nuevo el ciclo
        i += 1                                                                      # Contador

def Gui_repr_values():                                                              # Valores
    d_time = 0.01                                                                   # Reduccion del tiempo para obtener mas ondas en pantalla, sin el uso de velocidades y distancias muy grandes (balanceo con i%2)
    f_onda = float(freq_onda.get())                                                 # Frecuencia de la onda
    onda_rap = float(vel_onda.get())                                                # Velocidad de la onda
    foco_rap = float(vel_foco.get())                                                # Velocidad del Foco
    obs_rap = float(vel_obs.get())                                                  # Velocidad del Obs.
    lim_x = float(Lon_x.get())                                                      # Limite Eje X
    lim_y = float(Lon_y.get())                                                      # Limite Eje Y
    dist_x = float(mag_x.get())                                                     # Separacion entre Foco y Obs.

    repr(d_time,f_onda,onda_rap,foco_rap,obs_rap,lim_x,lim_y,dist_x)                  # Mandar valores a graficar

def kill1():                                                                        # Simple boton de salir (0)
    top.destroy()
    exit(0)

def MMmain():                                                                                                                           # Main()
    global freq_onda,vel_onda,vel_foco,vel_obs,Lon_x,Lon_y,mag_x                                                                        # Variables globales de la funcion anterior

    # Botones para inicar el programa o salir (0)
    Kill1 = Button(top,text='Salir',activeforeground='red',activebackground='gray', command = kill1).grid(row = 6, column = 5)
    trats = Button(top,text='Iniciar', activeforeground='green',activebackground='gray', command = Gui_repr_values).grid(row=6,column=4)

    # Velocidad de la onda (float), velocidad del sonido (base)
    Label(top, text='Velocidad de la Onda:').grid(row=1, column=0)
    vel_onda = Entry(top, width=6)
    vel_onda.insert(10, '343.0')
    vel_onda.grid(row=1, column=1)

    # Distancia entre focos (float), 20 metros (base)
    Label (top, text = 'Distancia entre foco y obs:').grid(row = 1, column = 3)
    mag_x = Entry(top, width = 6)
    mag_x.insert(10,'20.0')
    mag_x.grid(row = 1, column = 4)

    # Frecuencia de la onda (float), 300 Hz (base)
    Label(top, text='Frecuencia de la onda:').grid(row=2, column=0)
    freq_onda = Entry(top, width=6)
    freq_onda.insert(10, '300.0')
    freq_onda.grid(row=2, column=1)

    # Velocidad de la fuente (float), +100 m/s (base)
    Label(top, text='Velocidad de la fuente:').grid(row=3, column=0)
    vel_foco = Entry(top, width=6)
    vel_foco.insert(10, '100.0')
    vel_foco.grid(row=3, column=1)

    # Velocidad del observador (float), 0 m/s (base) - Estacionario
    Label(top, text='Velocidad del observador:').grid(row=3, column=3)
    vel_obs = Entry(top, width=6)
    vel_obs.insert(10, '0.0')
    vel_obs.grid(row=3, column=4)

    # Separador de los botones de salir e iniciar (se ve feo)
    Label(top, text='      ').grid(row=8, column=2)

    # Longitud del Eje X (float), 50 metros (base)
    Label(top, text='Longitud eje X:').grid(row=5, column=0)
    Lon_x = Entry(top, width=6)
    Lon_x.insert(10, '50.0')
    Lon_x.grid(row=5, column=1)

    # Longitud del Eje Y (float), 50 metros (base)
    Label(top, text='Longitud eje Y:').grid(row=5, column=3)
    Lon_y = Entry(top, width=6)
    Lon_y.insert(10, '50.0')
    Lon_y.grid(row=5, column=4)

global top                                                                  # Global de tkinter

top = Tk()                                                                  # Creacion de la ventana del menu
top.title('Efecto Doppler')                                                 # Nombre de la ventana
MMmain()                                                                    # Ciclar Menu
top.mainloop()                                                              # Ciclar Menu
