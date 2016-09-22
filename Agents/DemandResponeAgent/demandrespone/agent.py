# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright (c) 2013, Battelle Memorial Instituate
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.
#

# This material was prepared as an account of work sponsored by an
# agency of the United States Government.  Neither the United States
# Government nor the United States Department of Energy, nor Battelle,
# nor any of their employees, nor any jurisdiction or organization
# that has cooperated in the development of these materials, makes
# any warranty, express or implied, or assumes any legal liability
# or responsibility for the accuracy, completeness, or usefulness or
# any information, apparatus, product, software, or process disclosed,
# or represents that its use would not infringe privately owned rights.
#
# Reference herein to any specific commercial product, process, or
# service by trade name, trademark, manufacturer, or otherwise does
# not necessarily constitute or imply its endorsement, recommendation,
# r favoring by the United States Government or any agency thereof,
# or Battelle Memorial Institute. The views and opinions of authors
# expressed herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY
# operated by BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830


#Author : Payyoh
#}}}


from datetime import datetime
import logging
import sys
import json
import time
import random
from volttron.platform.agent import BaseAgent, PublishMixin, periodic
from volttron.platform.agent import utils, matching
from volttron.platform.messaging import headers as headers_mod

import settings


utils.setup_logging()
_log = logging.getLogger(__name__)


class ListenerAgent(PublishMixin, BaseAgent):
    '''Listens to everything and publishes a heartbeat according to the
    heartbeat period specified in the settings module.
    '''

    matching_topic = '/agent/ui/lighting/update_response/bemoss/999/2HUE0017881cab4b'

    def __init__(self, config_path, **kwargs):
        super(ListenerAgent, self).__init__(**kwargs)
        self.config = utils.load_config(config_path)



    def setup(self):
        # Demonstrate accessing a value from the config file
        _log.info(self.config['message'])
        self._agent_id = self.config['agentid']

        self.modenow = "COMFORT"
        # test control air
        # self.done_control = False
        # self.publish_test()
        # self.publish_BaseCase()        # air on temp 20,  light on brightness 100,    plug EV on
        # self.publish_DRCase1()         # air on temp 27,  light on brightness 50,     plug EV on
        # self.publish_DRCase2()         # air off,         light on brightness 50,     plug EV on
        # self.publish_DRCase3()         # air off,         light on brightness 50,     plug EV off
        # self.publish_DRCase4()           # air off,         light off,                  plug EV off
        # self.publish_DRCase5()         # air on temp 27,  light on brightness 100,    plug EV off
        # self.publish_DRCase6()         # air off,         light on brightness 100,    plug EV off

        # Always call the base class setup()
        super(ListenerAgent, self).setup()
    #
    # @matching.match_start(matching_topic)
    # def on_match(self, topic, headers, message, match):
    #     '''Use match_all to receive all messages and print them out.'''
    #     _log.debug("Topic: {topic}, Headers: {headers}, "
    #                      "Message: {message}".format(
    #                      topic=topic, headers=headers, message=message))
    #     print("topic{}".format(topic))
    #     print ("message{}".format(message))
    #     if (message[0] == "success"):
    #         print "success na ja"
    #         self.done_control = True
    #     else:
    #         self.done_control = False
    #         print "fail"
    #
    # @matching.match_start('/agent/ui/airconditioner/')
    # def on_match_ac(self, topic, headers, message, match):
    #     '''Use match_all to receive all messages and print them out.'''
    #     _log.debug("Topic: {topic}, Headers: {headers}, "
    #                "Message: {message}".format(
    #         topic=topic, headers=headers, message=message))
    #     print("topic{}".format(topic))
    #     print ("message{}".format(message))
    #     if (message[0] == "success"):
    #         print "success na ja"
    #         self.done_control = True
    #     else:
    #         self.done_control = False
    #         print "fail"

    #
    # @matching.match_all
    # def on_match(self, topic, headers, message, match):
    #     '''Use match_all to receive all messages and print them out.'''
    #     _log.debug("Topic: {topic}, Headers: {headers}, "
    #                      "Message: {message}".format(
    #                      topic=topic, headers=headers, message=message))
    #     print("topic{}".format(topic))
    #     print("message{}".format(message))

    @matching.match_exact('/ui/agent/select_mode/')
    def on_match(self, topic, headers, message, match):
        '''Use match_all to receive all messages and print them out.'''
        # _log.debug("Topic: {topic}, Headers: {headers}, "
        #            "Message: {message}".format(
        #     topic=topic, headers=headers, message=message))
        print "MODE---------"
        print "Topic: {}".format(topic)
        print "Headers: {}".format(headers)
        # print "Message: {}".format(message)
        event = json.loads(message[0])
        print type(event)
        print event
        event_status = event["status"]
        event_mode = event["mode"]
        print "event_status: {} ".format(event_status)
        print "event_mode: {} ".format(event_mode)

        if (event_mode == "comfort"):
            self.publish_Comfort()
        elif (event_mode == "eco"):
            self.publish_ECO()
        elif (event_mode == "dr"):
            self.publish_DR()
        print"---------------------------------------------------"



    # @matching.match_start("/ui/agent/mode/")
    # def on_match(self, topic, headers, message, match):
    #     '''Use match_all to receive all messages and print them out.'''
    #     _log.debug("Topic: {topic}, Headers: {headers}, "
    #                      "Message: {message}".format(
    #                      topic=topic, headers=headers, message=message))
    #     print("----------------------++++++++++++++++-------------------")
    #     print type(message)
    #     massage = message[0]
    #     message = json.loads(message)
    #     print message[0]
    #     event = message[0]
    #     event_status = event["status"]
    #     event_mode = event["mode"]
    #     print "event_status: {} ".format(event_status)
    #     print "event_mode: {} ".format(event_mode)
        # massage = str(message["mode"])
        # print massage
        #
        # if self.modenow == message["home_mode"]:
        #     print "same mode"
        # else:
        #     print "change mode"
        #     if message["home_mode"] == "DR":  #", "ECO", "COMFORT"]
        #         # dr = self.publish_BaseCase()
        #         print "DR"
        #     elif message["home_mode"] == "ECO":
        #         # eco = self.publish_ECO()
        #         print "ECO"
        #     elif message["home_mode"] == "COMFORT":
        #         # comfort = self.publish_Comfort()
        #          print "COMFORT"
        #     else:
        #         print "not match"
        #
        # self.modenow = message["home_mode"]
    # Demonstrate periodic decorator and settings access
    # @periodic(settings.HEARTBEAT_PERIOD)
    # @periodic(2)
    # def publish_test(self):
    #     self.HUE_Color()

    # total Load 1100 kW
    def publish_DR(self):
        self.AC1_OFF()
        time.sleep(5)
        self.AC2_OFF()
        time.sleep(5)
        self.AC3_OFF()
        time.sleep(2)
        self.FAN_ON()
        time.sleep(2)
        self.Plug_OFF()
        time.sleep(2)
        self.TV_OFF()
        time.sleep(2)
        self.HUE_OFF()
    #
    # total Load 1200 kW
    def publish_ECO(self):
        self.AC1_temp27()
        time.sleep(5)
        self.AC2_temp27()
        time.sleep(5)
        self.AC3_temp27()
        time.sleep(2)
        self.FAN_ON()
        time.sleep(2)
        self.Plug_ON()
        time.sleep(2)
        self.TV_ON()
        time.sleep(2)
        self.HUE_DIM(10)
    #
    # total Load 4500 kW
    def publish_Comfort(self):
        self.AC1_temp20()
        time.sleep(5)
        self.AC2_temp20()
        time.sleep(5)
        self.AC3_temp20()
        time.sleep(2)
        self.FAN_OFF()
        time.sleep(2)
        self.Plug_ON()
        time.sleep(2)
        self.TV_ON()
        time.sleep(2)
        self.HUE_Max()

    def AC1_temp20(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000001'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON", "temp": "20"})
        self.publish(topic, headers, message)
        print ("AC1 turned on : temp 20")

    def AC2_temp20(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000002'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON", "temp": "20"})
        self.publish(topic, headers, message)
        print ("AC2 turned on : temp 20")

    def AC3_temp20(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000003'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON", "temp": "20"})
        print ("message{}".format(message))
        self.publish(topic, headers, message)


    def AC1_temp27(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000001'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON", "temp": "27"})
        self.publish(topic, headers, message)
        print ("AC1 turned on : temp 27")

    def AC1_OFF(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000001'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "OFF"})
        self.publish(topic, headers, message)
        print ("AC1 turned off")
    #
    def AC2_temp27(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000002'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON", "temp": "27"})
        self.publish(topic, headers, message)
        print ("AC2 turned on : temp 27")

    def AC2_OFF(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000002'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "OFF"})
        self.publish(topic, headers, message)
        print ("AC2 turned off")

    def AC3_temp27(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000003'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON", "temp": "27"})
        self.publish(topic, headers, message)
        print ("AC3 turned on : temp 27")
    #
    def AC3_OFF(self):
        # TODO this is example how to write an app to control AC
        topic = '/ui/agent/airconditioner/update/bemoss/999/1TH20000000000003'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "OFF"})
        self.publish(topic, headers, message)
        print ("AC3 turned off")

    #
    def HUE_ON(self):
        # TODO this is example how to write an app to control Lighting
        topic = "/ui/agent/lighting/update/bemoss/999/2HUE0017881cab4b"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON", "color": [255, 255, 255]})
        self.publish(topic, headers, message)
        print ("HUE turn ON")
        print ("topic{}".format(topic))
        print ("message{}".format(message))

    def HUE_OFF(self):
        # TODO this is example how to write an app to control Lighting
        topic = "/ui/agent/lighting/update/bemoss/999/2HUE0017881cab4b"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "OFF"})
        self.publish(topic, headers, message)
        print ("HUE turn OFF")
    #
    def HUE_DIM(self, brightness):
        # TODO this is example how to write an app to control Lighting
        topic = "/ui/agent/lighting/update/bemoss/999/2HUE0017881cab4b"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"color": [255, 255, 255], "status": "ON", "brightness": brightness})
        self.publish(topic, headers, message)
        print ("HUE DIM brightness")

    def HUE_Max(self):
        # TODO this is example how to write an app to control Lighting
        topic = "/ui/agent/lighting/update/bemoss/999/2HUE0017881cab4b"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"color": [255, 255, 255], "status": "ON", "brightness": 100})
        self.publish(topic, headers, message)
        print ("HUE DIM brightness")

    def HUE_Color(self):
        # TODO this is example how to write an app to control Lighting
        topic = "/ui/agent/lighting/update/bemoss/999/2HUE0017881cab4b"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        R = random.randint(0,255)
        G = random.randint(0,255)
        B = random.randint(0,255)
        message = json.dumps({"color": [R, G, B]})
        self.publish(topic, headers, message)
        print ("HUE Color")

    def Plug_ON(self):
        # TODO this is example how to write an app to control plugload EV
        topic = "/ui/agent/plugload/update/bemoss/999/3WIS221445K1200321"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON"})
        self.publish(topic, headers, message)
        print ("plug EV turn ON")
    #
    def Plug_OFF(self):
        # TODO this is example how to write an app to control plugload EV
        topic = "/ui/agent/plugload/update/bemoss/999/3WIS221445K1200321"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "OFF"})
        self.publish(topic, headers, message)
        print ("plug EV turn OFF")


    def FAN_ON(self):
        # TODO this is example how to write an app to control FAN
        topic = "/ui/agent/fan/update/bemoss/999/1FN221445K1200138"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON"})
        self.publish(topic, headers, message)
        print ("FAN turn ON")


    def FAN_OFF(self):
        # TODO this is example how to write an app to control FAN
        topic = "/ui/agent/fan/update/bemoss/999/1FN221445K1200138"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "OFF"})
        self.publish(topic, headers, message)
        print ("FAN turn OFF")


    def TV_ON(self):
        # TODO this is example how to write an app to control FAN
        topic = "/ui/agent/lgtvagent/update/bemoss/999/1LG221445K1200137"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "ON"})
        self.publish(topic, headers, message)
        print ("TV turn ON")


    def TV_OFF(self):
        # TODO this is example how to write an app to control FAN
        topic = "/ui/agent/lgtvagent/update/bemoss/999/1LG221445K1200137"
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        message = json.dumps({"status": "OFF"})
        self.publish(topic, headers, message)
        print ("TV turn OFF")

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.default_main(ListenerAgent,
                           description='Example VOLTTRON platform™ heartbeat agent',
                           argv=argv)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass