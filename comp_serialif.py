"""
author: Cody Roberson
date: 2020-01-28
desc: This is the serial interface for the compressor
"""

import serial
import time
import pycrc


class f70L_HeCompressor():
    """
    Class:  f70L_HeCompressor\n
    Description:    Sumitomo (SHI) Cryogenics of America Helium Compressor Model F-70L Control Interface\n
    Input: String:= Serial Port\n
    """
    def __init__(self, port):
        self.serialConnection = serial.Serial()
        self.serialConnection.baudrate = 9600
        self.serialConnection.bytesize = 8
        self.serialConnection.timeout = 4
        self.serialConnection.parity=serial.PARITY_NONE
        self.serialConnection.port = port
        

    def startConnection(self):
        """
        Function: startConnection()\n
        Description: The configuration for the serial interface is already set other than the port. This is called to actually open the port.
        Input: none
        Output: Boolean:= True (Port opened) / False (Failed to open port)
        """
        try:
            self.serialConnection.open()
            if self.serialConnection.is_open:
                return True
        except:
            print("There was an issue establishing the serial connection")
            return False


    def collectStats(self):
        """
        Class Function: collectStas()\n
        Description: Communicates with the Helium Compressor over serial to read various stats\n
        Input: None\n
        Output: List:= [Capsule Helium Discharge Temp, water outlet Temp, Water inlet Temp, Compressor return temp]\n
                None:= in the case that there is no connection, None is returned
        todo: Future Release: Implement 'read status bits' \n
        """
        if not self.serialConnection.is_open:
            return None
        compressorStats = []
        # First send the command to get me my temps
        readTempStr = b"$TEAA4B9\r" # This has the checksum already included
        self.serialConnection.write(readTempStr)
        tempReply = self.serialConnection.read(26)
        #print(tempReply)

        

        readPressureStr = b"$PR171F6\r" # this also has checksum included
        self.serialConnection.write(readPressureStr)
        preaReply = self.serialConnection.read(14)
        #print(len(preaReply))
        
        # Check reply length and checksum for temperature
        """
        Example Reply
        $TEA,086,040,031,000,3798<cr>
        """
        if len(tempReply) > 0:
            rep = tempReply[0:len(tempReply)-5] # extract reply without crc
            calccrc = hex(pycrc.crc16_modbus(rep))[2:].encode("ASCII")  #calculate crc of packet and convert to str
            calccrc = calccrc.upper()
            retcrc = tempReply[len(tempReply)-5:-1] # extract crc 
            if  calccrc == retcrc:
                ree = tempReply.decode("ASCII")
                subst = ree.split(',')
                compressorStats.append(subst[1])
                compressorStats.append(subst[2])
                compressorStats.append(subst[3])


        # Check reply length and checksum for pressure
        """
        Example Reply4
        $PR1,079,2EBD<cr>
        """
        
        if len(preaReply) > 0:
            rep = preaReply[0:len(preaReply)-5] # extract reply without crc
            calccrc = hex(pycrc.crc16_modbus(rep))[2:].encode("ASCII")   #calculate crc of packet and convert to str
            calccrc = calccrc.upper()
            retcrc = preaReply[len(preaReply)-5:-1] # extract crc 
            if calccrc == retcrc:
                ree = preaReply.decode("ASCII")
                subst = ree.split(',')
                compressorStats.append(subst[1])

        # Finally, Return Stats
        return compressorStats



    def turnOn(self):
        """
        Class Function:   \n
        Description:   \n
        Input:   \n
        Output:  \n
        Notes:  When the compressor is off and without active fault, this will turn the compressor and  \n
                cold head on. If the command is sent while the compressor is in other states, the RS232  \n
                response will be returned, but no action will occur.  \n
        """
        if not self.serialConnection.is_open:
            return None
        command = b"$ON177CF\r" # Precalculated command + checksum
        expectedReply = "$ON1,8936\r" #Precalculated reply+checksum
        self.serialConnection.write(command)
        reply = self.serialConnection.readline()

        if reply == expectedReply:
            print("Command: Turn On, was successfully sent")
        else:
            print("An error has occured while attempting the command: Turn on")
            print("Command:= {}\nReply:= {}".format(command, reply))


    def turnOff(self):
        """
        Class Function:   \n
        Description:   \n
        Input:   \n
        Output:  \n
        Notes:  When the compressor and/or cold head is on, this will turn either or both off. If the \n
                command is sent while the compressor and cold head are off, the RS232 response will \n
                be returned, but no action will occur.  \n
        """
        if not self.serialConnection.is_open:
            return None
        command = b"$OFF9188\r" # Precalculated command + checksum
        expectedReply = "$OFF,bb90\r" #Precalculated reply + checksum
        self.serialConnection.write(command)
        reply = self.serialConnection.readline()

        if reply == expectedReply:
            print("Command: Turn On, was successfully sent")
        else:
            print("An error has occured while attempting the command: Turn on")
            print("Command:= {}\nReply:= {}".format(command, reply))


if __name__ == "__main__":
    compressor = f70L_HeCompressor("/dev/ttyUSB0")
    compressor.startConnection()
    compressor.collectStats()