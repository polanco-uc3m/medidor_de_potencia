#-*-coding:utf-8-*-

# Author Antonio Polanco Belmonte

#-------------------------------------------------------------------------------
import serial
import time
import numpy as np
##from matplotlib import pyplot as plt
#from scipy.optimize import leastsq

rpiLibre = 'n' #variable para indicar al micro que se pueden recibir datos
r=0 #variable que se utiliza para repetir el bucle while hasta recibir los datos
caracter="inductivo" #para imprimir por consola si el fdp es inductivo o capacitivo
#inicia la comunicación con el micro
arduino=serial.Serial('/dev/ttyACM0',baudrate=9600, timeout = 3.0) 
arduino.close()
arduino.open()

while r==0:  
    arduino.flushInput() #elimina los datos que se hayan quedado a la espera de ser recibidos
    
    rpiLibre = 'y' #raspberry lista para recibir
    time.sleep(3)# Da tiempo a capturar los datos
    arduino.write(str.encode(rpiLibre)) # manda la señal de raspberry lista para recibir
    a = arduino.inWaiting() #comprueba que hay datos en cola
    print(a)
    if a>0:
        r=2
        vMatrix=[]
        iMatrix=[]
        tMatrix=[]
        #en esta parte se reciben los valores
        for i in range(150):
            tMatrix.append(arduino.readline())
            iMatrix.append(arduino.readline())
            vMatrix.append(arduino.readline())
 #en esta parte se borran lops caracteres extra por culpa de la función Serial.println()
        for i in range(150):
            tMatrix[i]=tMatrix[i][:-2]
            iMatrix[i]=iMatrix[i][:-2]
            vMatrix[i]=vMatrix[i][:-2]
        for i in range(150):
            tMatrix[i]=int(tMatrix[i])
            iMatrix[i]=int(iMatrix[i])
            vMatrix[i]=int(vMatrix[i])
 #en esta parte se traducen los valores de intensidad y voltaje
        for i in range(150):
            iMatrix[i]=(512-iMatrix[i])*27.03/1023
            vMatrix[i]=(501-vMatrix[i])*54.7/1024
        print("start")
 #en esta parte se desechan los valores fuera de los primeros 20ms
        t=0
        k=0
        t_ciclo=[]
        i_ciclo=[]
        v_ciclo=[]
        while t<20000:
            t_ciclo.append(tMatrix[k])
            i_ciclo.append(iMatrix[k])
            v_ciclo.append(vMatrix[k])
            t=tMatrix[k]
            k=k+1
        #print(tMatrix)
        #print(iMatrix)
        #print(vMatrix)
     #calculo de variables
        i_max=max(i_ciclo)
        i_min=min(i_ciclo)
        v_max=max(v_ciclo)
        v_min=min(v_ciclo)
        i_pico=(abs(i_max)+abs(i_min))/2
        v_pico=(abs(v_max)+abs(v_min))/2
        i_ef=i_pico/(np.sqrt(2))
        v_ef=v_pico/(np.sqrt(2))
        posic=0
        for i in i_ciclo:
            if i==i_max:
                t_i= t_ciclo[posic]
            posic=posic+1
        posic=0
        for i in v_ciclo:
            if i==v_max:
                t_v= t_ciclo[posic]
            posic=posic+1
        desfase=t_i-t_v
        if desfase > 0:
            caracter= "inductivo"
        elif desfase < 0:
            caracter = "capacitivo"
        else:
            caracter= ""
        fdp = np.cos((abs(desfase)*2*np.pi)/20000)
        fdr = np.sin((abs(desfase)*2*np.pi)/20000)
        S = i_ef*v_ef
        Q = S*fdr
        P = S*fdp

        #mostrar por pantalla
        print(t_i)
        print(t_v)
        print ("i eficaz=",i_ef)
        print ("v eficaz=",v_ef)
        print ("fdp =",fdp,caracter)
        print ("La potencia aparente es S=",S)
        print ("La potencia reactiva es Q=",Q)
        print ("La potencia activa es P=",P) 
##        xt =t_ciclo
##        yi=i_ciclo
##        yv=v_ciclo
##        plt.plot(xt, yi, 'r-')
##        plt.plot(xt, yv, 'b-')
##        plt.xlabel('tiempo (us)')
##        plt.ylabel('Voltaje (V) -Intensidad (A)')
##        plt.title('Circuito R')
##        plt.legend(('Intensidad', 'Voltaje'))
##        plt.grid(True)
##        plt.show()
