# Domoticz-Remote-GPIO-Plugin
#
# Author: Rafalwal
#
#
"""
<plugin key="RPiRemoteGPIO" name="Raspberry Pi Remote GPIO" author="rafalwal (oryginal plugin created by dnpwwo)" version="1.0.0" wikilink="https://github.com/rafalwal/Domoticz-Remote-GPIO-Plugin" >
    <description>
        <h2>Domoticz Remote GPIO Plugin</h2><br/>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li style="line-height:normal">Remote RPi IP address</li>
            <li style="line-height:normal">Output Pins - Comma delimited list of output (relay) pins. Format is pin number colon NO or NC (e.g 39:NO)</li>
            <li style="line-height:normal">Heartbeat Frequency - Determines how often Output Pins are checked for values</li>
            <li style="line-height:normal">Debug - When true the logging level will be much higher to aid with troubleshooting</li>
        </ul>
    </description>
    <params>
        <param field="Mode1" label="Remote RPi IP address" width="300px"/>
        <param field="Mode2" label="Output Pins" width="400px"/>
        <param field="Mode3" label="Heartbeat Frequency" width="50px">
            <options>
                <option label="1" value="1"/>
                <option label="2" value="2"/>
                <option label="3" value="3"/>
                <option label="4" value="4"/>
                <option label="5" value="5"/>
                <option label="6" value="6"/>
                <option label="8" value="8"/>
                <option label="10" value="10" default="true" />
                <option label="12" value="12"/>
                <option label="14" value="14"/>
                <option label="16" value="16"/>
                <option label="18" value="18"/>
                <option label="20" value="20"/>
            </options>
        </param>
        <param field="Mode4" label="Debug" width="150px">
            <options>
                <option label="None" value="0"  default="true" />
                <option label="Python Only" value="2"/>
                <option label="Basic Debugging" value="62"/>
                <option label="Event Queue" value="128"/>
                <option label="All" value="-1"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import pigpio
def onStart():
    if Parameters["Mode4"] != "0":
        Domoticz.Log("Parameter is: '"+Parameters["Mode4"]+"'")
        Domoticz.Debugging(int(Parameters["Mode4"]))
        DumpConfigToLog()

    p1=pigpio.pi(Parameters["Mode1"])
    Domoticz.Heartbeat(int(Parameters["Mode3"]))
    
    # Process Output Pins
    if (len(Parameters["Mode2"]) > 0):
        try:
            outputPins = Parameters["Mode2"].split(',')
            for pin in outputPins:
                items = pin.split(':')
                pinNo = int(items[0])
                if not (pinNo in Devices):
                    Domoticz.Log("Creating Output device #"+str(pin))
                    Domoticz.Device(Name="Output "+items[0], Unit=pinNo, TypeName="Switch").Create() 
                rpin=p1.read(pinNo) 
                if (items[1]=="NC"):
                    if (rpin==0):
                        rpin=1
                    else:
                        rpin=0
                UpdateDevice(pinNo, rpin, "", 0)
        except Exception as inst:
            Domoticz.Error("Exception in onStart, processing Output Pins")
            Domoticz.Error("Exception detail: '"+str(inst)+"'"+Parameters["Mode2"])
            raise
    p1.stop()

def onCommand(Unit, Command, Level, Hue):
    #gotowe
    p1=pigpio.pi(Parameters["Mode1"])
    Domoticz.Log("onCommand for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
    outputPins = Parameters["Mode2"].split(',')
    for pin in outputPins:
        items = pin.split(':')
        pinNotmp = int(items[0])
        pinNCNOtmp = items[1]
        if (pinNotmp==Unit):
            pinNCNO=pinNCNOtmp

    if (Command == "On"):    
        if (pinNCNO=="NC"):
            rpin=0
        else:
            rpin=1
    else:
        if (pinNCNO=="NC"):
            rpin=1
        else:
            rpin=0

    p1.write(Unit,rpin)
    p1.stop
    UpdateDevice(Unit, rpin, Command, 0)

#def onStop():
    #gotowe	
#    Domoticz.Debug("onStop")

def onHeartbeat():
   if (len(Parameters["Mode2"]) > 0):
        try:
            p1=pigpio.pi(Parameters["Mode1"])
            outputPins = Parameters["Mode2"].split(',')
            for pin in outputPins:
                items = pin.split(':')
                pinNo = int(items[0])
                rpin=p1.read(pinNo) 
                if (items[1]=="NC"):
                    if (rpin==0):
                        rpin=1
                    else:
                        rpin=0
                UpdateDevice(pinNo, rpin, "", 0)
            p1.stop()
        except Exception as inst:
            Domoticz.Error("Exception in onHeartbeat, processing Output Pins")
            Domoticz.Error("Exception detail: '"+str(inst)+"'"+Parameters["Mode1"])
            raise

# Generic helper functions
#gotowe
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Log( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Log("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Log("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Log("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Log("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Log("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Log("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Log("Device LastLevel: " + str(Devices[x].LastLevel))
    return
    
def UpdateDevice(Unit, nValue, sValue, TimedOut):
    #gotowe
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (Devices[Unit].TimedOut != TimedOut):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return
