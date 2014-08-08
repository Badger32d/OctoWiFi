#!/usr/bin/env python

import logging
import sys
import time
import common


class WiFiServer(object):
    """
    Master process for WiFi service
    """
    def __init__(self, cfg=None):
        self.svc = common.SVC()
        common.WiFiObj.svc = self.svc
        self.ap = common.WiFiAP()
        self.setup_logging()
        self.shutdown = False
        self.networks = []

    def setup_logging(self):
        """Setup Logging"""
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.StreamHandler(sys.stdout)

    def keyboardinterrupt(self):
        self.shutdown = True
        logging.info("KeyboardInterrupt Called, Shutting down application")

    def start(self):
        self.main()

    def start_ws(self):
        """start the webservice"""
        pass

    def start_ap(self):
        """star the ap if we're in ap mode"""
        if self.svc.apmode:
            logging.info("starting AP")
            if not self.svc.ap_active:
                self.ap.startap()
            else:
                logging.debug("WiFi AP already active")
        else:
            logging.info("this shouldn't get hit, no reason to start the AP")

    def stop_ap(self):
        """stop the AP"""

    def get_networks(self):
        wificlient = common.WifiClient()
        self.networks = wificlient.scan()

    def add_network(self, data):
        """add new network config information"""
        wificlient = common.WifiClient()
        result = wificlient.add_network(data)
        return result

    def cleanup(self):
        pass

    def main(self):
        """main thread"""
        try:
            logging.info("Main Thread Stable (startup complete)")
            while self.shutdown is False:
                try:
                    time.sleep(1)
                    logging.debug('Main loop')
                except KeyboardInterrupt:
                    self.keyboardinterrupt()
            logging.info("Begin Shutdown Sequeuence")
            self.cleanup()
            logging.info("WiFiServer is Shutdown")
        except Exception as e:
            logging.critical("Error in Main loop: {0}".format(e))
        finally:
            exit()
