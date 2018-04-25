from f5.bigip import *
from icontrol.exceptions import iControlUnexpectedHTTPError 

class F5Manager(object):
    
    def __init__(self, hostname, admin, password, port):

        self.hostname = hostname
        self.admin = admin
        self.password = password
        self.port = port
        self.mgmt = None

    def connect(self):
        print("Trying to connect to {}".format(self.hostname))
        try:
            self.mgmt = ManagementRoot(hostname=self.hostname,
                                       username=self.admin,
                                       password=self.password,
                                       port=self.port)
            print("Connected successfully")
        except iControlUnexpectedHTTPError as err:
            raise



class NodeController(object):
    
    def __init__(self, node_name, partition, f5_manager):
        self.node_name = node_name
        self.partition = partition
        self.f5_manager = f5_manager.mgmt
        self.node_object = None

    def load_node(self):
        try:
            print("Trying to load node {}".format(self.node_name))
            self.node_object = self.f5_manager.tm.ltm.nodes.node.load(
                partition=self.partition,
                name=self.node_name)
            print("Loaded node {}".format(self.node_name))
        except Exception:
            raise

    def take_node_down(self):
        try:
            print("Disabling node {}".format(self.node_name))
            self.node_object.modify(session="user-disabled", state="user-down")
            print("Disabled node {}".format(self.node_name))
        except Exception:
            raise 

    def take_node_up(self):
        try: 
            print("Enabling node {}".format(self.node_name))
            self.node_object.modify(session="user-enabled", state="user-up")
            print("Enabled node {}".format(self.node_name))
        except Exception:
            raise 

    def get_node_status(self):
        return self.node_object.session, self.node_object.state
   
