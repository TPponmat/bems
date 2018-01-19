# -*- coding: utf-8 -*-
'''
Copyright (c) 2016, Virginia Tech
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
 following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the authors and should not be
interpreted as representing official policies, either expressed or implied, of the FreeBSD Project.

This material was prepared as an account of work sponsored by an agency of the United States Government. Neither the
United States Government nor the United States Department of Energy, nor Virginia Tech, nor any of their employees,
nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty,
express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or
any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe
privately owned rights.

Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or
otherwise does not necessarily constitute or imply its endorsement, recommendation, favoring by the United States
Government or any agency thereof, or Virginia Tech - Advanced Research Institute. The views and opinions of authors
expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

VIRGINIA TECH – ADVANCED RESEARCH INSTITUTE
under Contract DE-EE0006352

#__author__ = "BEMOSS Team"
#__credits__ = ""
#__version__ = "2.0"
#__maintainer__ = "BEMOSS Team"
#__email__ = "aribemoss@gmail.com"
#__website__ = "www.bemoss.org"
#__created__ = "2014-09-12 12:04:50"
#__lastUpdated__ = "2016-03-14 11:23:33"
'''

import time
import json
import requests

class API:
    # 1. constructor : gets call every time when create a new class
    # requirements for instantiation1. model, 2.type, 3.api, 4. address
    def __init__(self,**kwargs):
        # Initialized common attributes
        self.variables = kwargs
        self.debug = True
        self.set_variable('offline_count',0)
        self.set_variable('connection_renew_interval', 6000)
        self.only_white_bulb = None


    def renewConnection(self):
        pass

    def set_variable(self,k,v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self,k):
        return self.variables.get(k, None)  # default of get_variable is none

    # 2. Attributes from Attributes table

    '''
    Attributes:
     ------------------------------------------------------------------------------------------
    label            GET          label in string
    illuminance      GET          illuminance
    temperature      GET          temporary target heat setpoint (floating point in deg F)
    battery          GET          percent battery of Fibaro censor
    motion           GET          motion  status (active/inactive)
    tamper           GET          tamper  status (active/inactive)
    unitTime         GET          Hue light effect 'none' or 'colorloop'
     ------------------------------------------------------------------------------------------

    '''
    # 3. Capabilites (methods) from Capabilities table
    '''
    API3 available methods:
    1. getDeviceStatus() GET
    '''    

    # ----------------------------------------------------------------------
    # getDeviceStatus(), getDeviceStatusJson(data), printDeviceStatus()
    def getDeviceStatus(self):

        getDeviceStatusResult = True

        try:
            headers = {"Authorization": self.get_variable("bearer")}
            url = str(self.get_variable("url") + self.get_variable("device"))
            r = requests.get(url,
                             headers=headers, timeout=20);
            format(self.variables.get('agent_id', None), str(r.status_code))
            print r.text
            if r.status_code == 200:
                getDeviceStatusResult = False

                self.getDeviceStatusJson(r.text)
                if self.debug is True:
                    self.printDeviceStatus()
            else:
                print (" Received an error from server, cannot retrieve results")
                getDeviceStatusResult = False
            # Check the connectivity
            if getDeviceStatusResult==True:
                self.set_variable('offline_count', 0)
            else:
                self.set_variable('offline_count', self.get_variable('offline_count')+1)
        except Exception as er:
            print er
            print('ERROR: classAPI_PhilipsHue failed to getDeviceStatus')
            self.set_variable('offline_count',self.get_variable('offline_count')+1)

    def getDeviceStatusJson(self, data):

        conve_json = json.loads(data)
        print conve_json
        # self.set_variable('label', str(conve_json["label"]))
        # self.set_variable('status', str(conve_json["status"]))
        # self.set_variable('unitTime', conve_json["unitTime"])
        # self.set_variable('type', str(conve_json["type"]))

    def printDeviceStatus(self):

        # now we can access the contents of the JSON like any other Python object
        # print(" the current status is as follows:")
        # print(" label = {}".format(self.get_variable('label')))
        # print(" status = {}".format(self.get_variable('status')))
        # print(" unitTime = {}".format(self.get_variable('unitTime')))
        # print(" type= {}".format(self.get_variable('type')))
        print("---------------------------------------------")

    # setDeviceStatus(postmsg), isPostmsgValid(postmsg), convertPostMsg(postmsg)
    def setDeviceStatus(self, postmsg):

        if type(postmsg) == str:
            postmsg = eval(postmsg)

        setDeviceStatusResult = True

        headers = {"Authorization": self.get_variable("bearer")}
        url = str(self.get_variable("url") + self.get_variable("device"))

        if self.isPostMsgValid(postmsg) == True:  # check if the data is valid
            _data = json.dumps(self.convertPostMsg(postmsg))
            _data = _data.encode(encoding='utf_8')
            print type(postmsg)
            print (_data)



            try:
                _data2 =   json.dumps({"command": "TwoOff"})
                print (_data2)
                print "sending requests put"
                r3 = requests.put(url, headers=headers, data=_data, timeout=20);
                time.sleep(1)

                # _data3 = json.dumps(self.convertPostMsg(postmsg2))
                _data3 =   json.dumps({"command": "OneOff"})
                print (_data3)
                print "sending requests put"
                r2 = requests.put(url, headers=headers, data=_data3, timeout=20);
                time.sleep(1)


                print "sending requests put"
                r = requests.put(url, headers=headers, data=_data, timeout=20);

                time.sleep(15)



                _data3 =  json.dumps({"command": "OneOff"})
                print (_data3)
                print "sending requests put"
                r2 = requests.put(url, headers=headers, data=_data3, timeout=20);

                _data2 =   json.dumps({"command": "TwoOff"})
                print (_data2)
                print "sending requests put"
                r3 = requests.put(url, headers=headers, data=_data2, timeout=20);
                time.sleep(1)

                # _data3 = json.dumps(self.convertPostMsg(postmsg2))
                _data3 =   json.dumps({"command": "OneOff"})
                print (_data3)
                print "sending requests put"
                r2 = requests.put(url, headers=headers, data=_data3, timeout=20);



            except:
                print("ERROR: classAPI_Somfy connection failure! @ setDeviceStatus")
                setDeviceStatusResult = False
        else:
            print("The POST message is invalid, try again\n")
        return setDeviceStatusResult

    def isPostMsgValid(self, postmsg):  # check validity of postmsg
        dataValidity = True
        # TODO algo to check whether postmsg is valid
        return dataValidity

    def convertPostMsg(self, postmsg):
        msgToDevice = {}
        print

        if postmsg['status'] == 'ON':

            msgToDevice['command'] = "OneOn"

        elif postmsg['status'] == 'OFF':
            msgToDevice['command'] = "TwoOn"

        return msgToDevice

    # ----------------------------------------------------------------------

# This main method will not be executed when this class is used as a module
def main():
    # create an object with initialized data from DeviceDiscovery Agent
    # requirements for instantiation1. model, 2.type, 3.api, 4. address

    Somfy = API(model='Somfy', type='tv', api='API3', agent_id='SomfyAgent',url = 'https://graph-na02-useast1.api.smartthings.com/api/smartapps/installations/202124fc-478e-4fdf-9e67-a81bb5ae1213/switches/', bearer = 'Bearer 0291cb9f-168e-490e-b337-2d1a31abdbf4',device = 'e75fb1ac-aebe-427d-a4e4-5d50f0572c18')
    Somfy.getDeviceStatus()


    #
    Somfy.setDeviceStatus({"status": "ON"})
    #
    # time.sleep(10)
    #
    # Somfy.setDeviceStatus({"status": "ON"})
    #
    # time.sleep(10)
    #
    # Somfy.setDeviceStatus({"status": "OFF"})

if __name__ == "__main__": main()