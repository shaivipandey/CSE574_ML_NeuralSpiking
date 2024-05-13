
"""
Created on January 2024 8:10 am
Acknowledgement: The neuron spiking model code was written with
reference to the Izhikevich neuron spiking model code. 

@author: Shaivi Pandey 
"""

import numpy as np
import matplotlib.pyplot as plt

tau = .25
steps = 500
tspan = np.linspace(0, steps, num=steps/tau, endpoint=True)
#T1 is the time interval at which the input first rises.
T1 = 50

ulist = []
vlist = []

def runSingleNeuronSpiking(inputIValue, tspan, steps=500, T1=50, plot=False):
    neuron1 = SpikingNeuron()
    inputI = 0
    voltageList = []
    for time in tspan:
        if time < T1:
            inputI = 0
        else:
            inputI = inputIValue
        #Stimulate the neuron.
        voltageList.append(neuron1.stimulate(inputI))
    
    #When finished, plot the function output for the time span.
    if plot:    
        plt.plot(tspan, voltageList)
        plt.axis([0, steps, -90, 40])
        plt.xlabel('Time')
        plt.ylabel('Voltage mV')
        plt.title('Tonic Spiking At Input: ' + str(inputIValue))
        plt.show()
        
    return voltageList
    
def runSequentialNeuronSpikingModel(inputIValue, tspan, steps=500, T1=50, plot=False):
    global ulist, vlist
    neuron1 = SpikingNeuron()
    neuron2 = SpikingNeuron()
    input1I = 0
    weight = 100
    voltageN1List = []
    voltageN2List = []
    for time in tspan:
        if time < T1:
            input1I = 0
        else:
            input1I = inputIValue
            
        #Stimulate neuron 1.
        neuron1Output = neuron1.stimulate(input1I)
        voltageN1List.append(neuron1Output)
        #Stimulate neuron 2.
        if neuron1Output == 30:
            voltageN2List.append(neuron2.stimulate(weight*1))
        else:
            voltageN2List.append(neuron2.stimulate(0))
    ulist = neuron2.uList
    vlist = neuron2.vList
    
            
    #When finished, plot the function output for the time span.
    if plot:  
        plt.subplot(121)
        plt.plot(tspan, voltageN1List)
        plt.axis([0, steps, -90, 40])
        plt.xlabel('Time')
        plt.ylabel('Voltage mV')
        plt.title('Tonic Spiking At Input: ' + str(inputIValue))
        plt.subplot(122)
        plt.plot(tspan, voltageN2List)
        plt.axis([0, steps, -90, 40])
        plt.xlabel('Time')
        plt.ylabel('Voltage mV')
        plt.title('Tonic Spiking At Input: ' + str(inputIValue))
        plt.tight_layout()        
        plt.show()
    
    return voltageN1List, voltageN2List

class SpikingNeuron:
    
    def __init__(self):
        self.a = 0.02
        self.b = 0.25
        self.c = -65
        self.d = 6
        self.V = -64
        self.tau = 0.25
        self.u = self.b * self.V
        self.uList = []
        self.vList = []
    
    def stimulate(self, inputI):
        #Do an incremental membrane potential update using the differential equation times the discretization.
        #Vn+1 = Vn + deltaVn
        #deltaVn = delta_t * (dV/dt)
        self.V = self.V + self.tau*( (0.04*(self.V**2)) + (5*self.V) + 140 - self.u + inputI )  
        vOut = self.V  
        self.vList.append(vOut)
        #Do an increment for the 'u' differential equation.
        self.u = self.u + self.tau*(self.a*((self.b*self.V) - self.u))
        self.uList.append(self.u)
        
        #Set up a peak saturation and breakdown condition.
        if(self.V >= 30 ):
            vOut = 30
            self.V = self.c
            self.u = self.u + self.d
        
        return vOut
        
def hwPart1():
    meanSpikingRate = []
    inputArray = np.linspace(0, 20, 20/.25, endpoint=True)
    for inputValue in inputArray:
        #Simulate neuron for current input.
        voltageOutputList = runSingleNeuronSpiking(inputValue, tspan, plot=False)
        #Filter out the beginning time from 0 to 200.(Aka take times 200 to 500.)
        voltageOutputList = voltageOutputList[800:]        
        #Find the mean spiking rate. When V is set to 30, that means a spike has occurred.
        meanSpikingRate.append(voltageOutputList.count(30)/300)
        
    plt.scatter(inputArray, meanSpikingRate)
    plt.xlabel('Input Level')
    plt.ylabel('Mean Spiking Rate')
    plt.title('Mean Spiking Rate vs Input Level')
    plt.show()
        
    inputArray = [1, 5, 10, 15, 20]
    for inputValue in inputArray:
        #Simulate neuron for current input.
        voltageOutputList = runSingleNeuronSpiking(inputValue, tspan, plot=True)
        
def hwPart2():
    meanSpikingRateN1 = []
    meanSpikingRateN2 = []
    inputArray = np.linspace(0, 20, 20/.25, endpoint=True)
    #inputArray = [0, 1, 5, 10, 15, 20]
    for inputValue in inputArray:
        #Simulate neuron for current input.
        voltageN1List, voltageN2List = runSequentialNeuronSpikingModel(inputValue, tspan, plot=False)
        #Filter out the beginning time from 0 to 200.(Aka take times 200 to 500.)
        voltageN1List = voltageN1List[800:]  
        voltageN2List = voltageN2List[800:] 
        #Find the mean spiking rate. When V is set to 30, that means a spike has occurred.
        meanSpikingRateN1.append(voltageN1List.count(30)/300)
        meanSpikingRateN2.append(voltageN2List.count(30)/300)
        
    plt.scatter(inputArray, meanSpikingRateN1)
    plt.xlabel('Input Level')
    plt.ylabel('Mean Spiking Rate')
    plt.title('Mean Spiking Rate Na vs IA')
    plt.show()
    plt.clf()
    plt.scatter(inputArray, meanSpikingRateN2)
    plt.xlabel('Input Level')
    plt.ylabel('Mean Spiking Rate')
    plt.title('Mean Spiking Rate Nb vs IA')
    plt.show()
    plt.clf()
    plt.scatter(meanSpikingRateN2, meanSpikingRateN1)
    plt.xlabel('Mean Spiking Rate Nb')
    plt.ylabel('Mean Spiking Rate Na')
    plt.title('Mean Spiking Rate Na vs Mean Spiking Rate Nb')
    plt.show()
    

if __name__ == "__main__":
    #hwPart1()
    #hwPart2()
    voltageN1List, voltageN2List = runSequentialNeuronSpikingModel(15, tspan, plot=True)
        
    
    
    
    
