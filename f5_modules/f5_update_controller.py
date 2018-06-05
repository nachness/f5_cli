from f5.bigip import *
from icontrol.exceptions import iControlUnexpectedHTTPError 

class F5Manager(object):
    
    def __init__(self, **kwargs):
        self.hostname = kwargs.pop('host')
        self.admin = kwargs.pop('user')
        self.password = kwargs.pop('password')
        self.port = kwargs.pop('port')
        self.f5_manager = None

    def connect(self):
        print('Trying to connect to {}'.format(self.hostname))
        try:
            self.f5_manager = ManagementRoot(hostname=self.hostname,
                                       username=self.admin,
                                       password=self.password,
                                       port=self.port)
            print('Connected successfully')
        except iControlUnexpectedHTTPError as err:
            raise 


class NodeController(F5Manager):
    
    def __init__(self, node_name, **kwargs):
        super(F5Manager,self).__init__(**kwargs)
        self.node_name = node_name
        self.partition = kwargs.pop('partition')
        try:
            self.f5_manager.connect()
            self.node_object = self.f5_manager.tm.ltm.nodes.node.load(
                    partition=self.partition,
                    name=self.node_name)
        except Exception as err:
            raise

    def take_node_down(self):
        try:
            print('Disabling node {}'.format(self.node_name))
            self.node_object.modify(session='user-disabled', state='user-down')
            print('Disabled node {}'.format(self.node_name))
        except Exception:
            raise 

    def take_node_up(self):
        try: 
            print('Enabling node {}'.format(self.node_name))
            self.node_object.modify(session='user-enabled', state='user-up')
            print('Enabled node {}'.format(self.node_name))
        except Exception:
            raise 

    def get_node_status(self):
        return self.node_object.session, self.node_object.state

class VirtualServerController(F5Manager):
    
    def __init__(self, vip_name, **kwargs):
        super(VirtualServerController, self).__init__(**kwargs)
        super(VirtualServerController, self).connect()
        self.vip_name = vip_name
        self.partition = kwargs.pop('partition')
        try:
            self.vip_object = self.f5_manager.tm.ltm.virtuals.virtual.load(
                name=self.vip_name,
                partition=self.partition)
        except Exception as err:
            raise

    def __refresh(self):
        try: 
            print('Reloading %s virtualserver' % self.vip_name)
            self.vip_object.refresh()
        except Exception as err:
            raise

    def add(self, irule_name):
        try:
            if irule_name not in self.vip_object.rules:
                print('Adding rule %s' % (irule_name))
                self.vip_object.rules.append(irule_name)
                self.vip_object.update()
                print('Rule added')
                self.__refresh()
            else:
                print('Rule already exists') 
        except Exception as err:
            raise 

    def remove(self, irule_name):
        try: 
            if irule_name in self.vip_object.rules:
                print('Removing rule %s' % (irule_name))
                self.vip_object.rules.remove(irule_name)
                self.vip_object.update()
                print('Rule removed')
                self.__refresh()
            else:
                print('iRule is not present on this VS')
        except Exception:
            raise 

    def get_vip_attr(self, attr):
        return self.vip_object.__dict__[attr]
