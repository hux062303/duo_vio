#!/usr/bin/python
from __future__ import print_function, division

import subprocess


def get_pid(node_name):
    process = subprocess.Popen('rosnode info /{}'.format(node_name).split(), stdout=subprocess.PIPE)
    output = process.communicate()[0].splitlines()

    for line in output:
        idx = line.find('Pid:')
        if not idx < 0:
            return int(line[idx+4:])
    return -1

if __name__ == "__main__":

    # dict keys are ros node names, values are cpu set names
    nodes = dict(vio_ros='vio_node', duo_node='duo_node', core_node='core_node')

    for node_name, cpu_set in nodes.iteritems():
        pid = get_pid(node_name)
        if not pid < 0:
            command = 'sudo -A cset proc -m -p {} -t {}'.format(pid, cpu_set)
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            print(process.communicate()[0])
        else:
            print('Failed to get PID for node {}'.format(node_name))

    # print the cpuset status after moving the nodes to their sets
    print(subprocess.Popen('sudo -A cset set -l'.split(), stdout=subprocess.PIPE).communicate()[0].splitlines())