from f5_update_controller import F5Manager, NodeController
from argparse import ArgumentParser
import getpass
import sys
def main():
 
    parser = ArgumentParser()
 
    parser.add_argument("-u","--user",
                        help="The admin user of F5",
                        default="admin", dest="user")
    parser.add_argument("-p","--password",
                        help="The admin password for F5, \
                              If no pass is specified you'll be prompted",
                        dest="password")
    parser.add_argument("-H","--host", help="The IP of F5",
                        dest="host")
    parser.add_argument("-P", "--port", type=int,
                        help="The port on which F5s APIs are served",
                        default=443, dest="port")
    parser.add_argument("-N","--node",nargs="*",
                        help="Node backend to disable, multiple nodes can also\
                        be specified", dest="nodes_list")
    parser.add_argument("--disable", action="store_true",
                        help="Take Disable action towards backend",
                        dest="disable")
    parser.add_argument("--enable", action="store_true",
                        help="Take Enable action towards backend",
                        dest="enable")
    parser.add_argument("--partition", dest="partition", default="Common",
                        help="Specify optional F5 node partition")
 
    if len(sys.argv) <= 1: 
        parser.print_help() 
        sys.exit(1) 
    else: 
        args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass("F5 Password: ")
 
    f5_manager = connect_to_f5(args.host, args.user, args.password,
                               args.port)
    if args.nodes_list:
        take_node_action(args=args,
                         f5_manager=f5_manager)

def connect_to_f5(host,user,password, port):
    f5_manager = F5Manager(hostname=host,
                           admin=user,
                           password=password,
                           port=port)
    f5_manager.connect()
 
    return f5_manager

def take_node_action(args, f5_manager):

    for node in args.nodes_list:
        node_object = load_node(node, args.partition, f5_manager)
 
        if args.disable:
            disable_node(node_object)

        elif args.enable:
            enable_node(node_object)
        else:
            print("No disable or enable specified, what are you trying to do?")
        
        get_status(node_object)
 

def load_node(node, partition, f5_manager):
    node_object = NodeController(node_name=node,
                                 partition=partition,
                                 f5_manager=f5_manager)
    node_object.load_node()
    return node_object 

def disable_node(node_object):
    node_object.take_node_down()


def enable_node(node_object):
    node_object.take_node_up()

def get_status(node_object):
    session , state = node_object.get_node_status()
    print("""node session status is: {}
           node state status is: {}""".format(session, state))


main()
