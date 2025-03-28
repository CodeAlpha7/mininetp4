from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
import time

topo = load_topo('topology.json')
controllers = {}

for p4switch in topo.get_p4switches():
    thrift_port = topo.get_thrift_port(p4switch)
    controllers[p4switch] = SimpleSwitchThriftAPI(thrift_port)

controller = controllers['s1']                        
controller.table_clear('repeater')
controller.table_add('repeater', 'random_forward', ['1'], ['2', '3'])
controller.table_add('repeater', 'forward', ['2'], ['1'])
controller.table_add('repeater', 'forward', ['3'], ['1'])

controller = controllers['s2']                        
# TODO 1: Populate the repeater table for switch s2

controller = controllers['s3']                        
# TODO 2: Populate the repeater table for switch s3

controller = controllers['s4']                        
# TODO 3: Populate the repeater table for switch s4


while True:
    # wait for 1 minute
    time.sleep(60)

    # read values of counters in the h1 -> h2 direction
    h1_h2_top_path = controllers['s2'].counter_read('packet_ctr', 0)[1]
    h1_h2_bottom_path = controllers['s4'].counter_read('packet_ctr', 0)[1]
    h1_h2_total = h1_h2_top_path + h1_h2_bottom_path

    # avoid ZeroDivisionError
    if h1_h2_total == 0:
        h1_h2_total = 1
        
    # compute percentages
    h1_h2_percentage_top = round(h1_h2_top_path / h1_h2_total * 100, 2)
    h1_h2_percentage_bottom = round(h1_h2_bottom_path / h1_h2_total * 100, 2)

    # print the results
    print('Packets from h1 to h2 in the top path:', h1_h2_percentage_top, '%')
    print('Packets from h1 to h2 in the bottom path:', h1_h2_percentage_bottom, '%')

    # TODO 4: calculate and print percentages for h2 -> h1 direction

    # TODO 5: clear the values of the counter arrays