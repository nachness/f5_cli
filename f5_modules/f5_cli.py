from f5_modules.f5_update_controller import (F5Manager, 
                                             NodeController,
                                             VirtualServerController)
from argparse import ArgumentParser
import getpass
import sys

class CommandParser(object):
    def __init__(self):
        
        parser = ArgumentParser(
            description='Tool to modify BIGIP F5 configuration',
             usage='''f5_cli <command> [<args>]

    The most commonly used f5_cli commands are:
    node     Record changes to the repository
    irule      Download objects and refs from another repository''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def node(self):
     
        parser = ArgumentParser(
            description='Enable\Disable a backend node')
     
        parser.add_argument('-u','--user',
                            help='The admin user of F5',
                            default='admin', dest='user')
        parser.add_argument('-p','--password',
                            help='The admin password for F5, \
                                  If no pass is specified youll be prompted',
                            dest='password')
        parser.add_argument('-H','--host', help='The IP of F5',
                            dest='host')
        parser.add_argument('-P', '--port', type=int,
                            help='The port on which F5s APIs are served',
                            default=443, dest='port')
        parser.add_argument('-N','--name',nargs='*',
                            help='Node backend to disable, multiple nodes can also\
                            be specified', dest='nodes_list')
        parser.add_argument('--disable', action='store_true',
                            help='Take Disable action towards backend',
                            dest='disable')
        parser.add_argument('--enable', action='store_true',
                            help='Take Enable action towards backend',
                            dest='enable')
        parser.add_argument('--partition', dest='partition', default='Common',
                            help='Specify optional F5 node partition')
     
        args = parser.parse_args(sys.argv[2:])

        if not args.password:
            args.password = getpass.getpass('F5 Password: ')
     
        if args.nodes_list:
            take_node_action(args=args)

    def irule(self):
     
        parser = ArgumentParser(
            description='Add\Remove an irule')
     
        parser.add_argument('-u','--user',
                            help='The admin user of F5',
                            default='admin', dest='user')
        parser.add_argument('-p','--password',
                            help='The admin password for F5, \
                                  If no pass is specified youll be prompted',
                            dest='password')
        parser.add_argument('-H','--host', help='The IP of F5',
                            dest='host')
        parser.add_argument('-P', '--port', type=int,
                            help='The port on which F5s APIs are served',
                            default=443, dest='port')
        parser.add_argument('-V', '--vip', nargs='*',
                            help='Names of VIPs to modify',
                            dest='vip_list')
        parser.add_argument('-N','--name',
                            help='Names of irules to modify',
                            dest='rule_name')
        parser.add_argument('--remove', action='store_true',
                            help='Remove iRule from a VIP',
                            dest='remove')
        parser.add_argument('--add', action='store_true',
                            help='Add iRule to a VIP',
                            dest='add')
        parser.add_argument('--partition', dest='partition', default='Common',
                            help='Specify optional F5 node partition')
     
        args = parser.parse_args(sys.argv[2:])

        if not args.password:
            args.password = getpass.getpass('F5 Password: ')
     

        if args.rule_name:
            take_rules_action(args=args)

def take_node_action(args):

    for node in args.nodes_list:
        nodeController = NodeController(node=node, **args.__dict__)
 
        if args.disable:
            nodeController.take_node_down()

        elif args.enable:
            nodeController.take_node_up()
        else:
            print('No disable or enable specified, what are you trying to do?')
        
        get_node_status(nodeController)

def get_node_status(nodeController):
    
    session , state = nodeController.get_node_status()
    print('''node session status is: {}
           node state status is: {}'''.format(session, state))

def take_rules_action(args):
    print(args.__dict__) 
    for vs_name in args.vip_list:
        virtualServerController = VirtualServerController(vip_name=vs_name,
            **args.__dict__)
 
        if args.remove:
            virtualServerController.remove(args.rule_name)
        elif args.add:
            virtualServerController.add(args.rule_name)
        else:
            print('No add or remove specified, what are you trying to do?')
        
        rules_list = virtualServerController.get_vip_attr('rules')
        print('Current active rules are %s' % (rules_list))

def main():
    CommandParser()

if __name__ == '__main__':
    main()
