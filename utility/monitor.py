# Copyright 2024 hd company
# Authors: Hyeongjun Jeon
import copy
import subprocess


def get_monitor_info():

    if not get_monitor_info.initialized:
        monitor_infos = \
            subprocess.Popen(
                'xrandr --listmonitors',
                shell=True,
                stdout=subprocess.PIPE).communicate()[0].decode().split('\n')
        del monitor_infos[0], monitor_infos[-1]

        get_monitor_info.saved_monitor_infos['count'] = len(monitor_infos)

        for index, monitor_info in enumerate(monitor_infos):
            info = monitor_info.split(' ')
            monitor_port_type = info[2]
            monitor_scale = info[3]
            monitor_offset = monitor_scale.split('+')
            del monitor_offset[0]

            if monitor_port_type[1] == '*':
                get_monitor_info.saved_monitor_infos['primary_index'] = index

            size = [int(scale_info.split('/')[0]) for scale_info in monitor_scale.split('x')]
            get_monitor_info.saved_monitor_infos['size'].append(
                {'width': size[0],
                 'height': size[1],
                 'x_offset': int(monitor_offset[0]),
                 'y_offset': int(monitor_offset[1])})
        get_monitor_info.initialized = True

    return copy.deepcopy(get_monitor_info.saved_monitor_infos)


get_monitor_info.initialized = False
get_monitor_info.saved_monitor_infos = {'primary_index': 0, 'size': [], 'count': 0}

if __name__ == '__main__':
    saved_monitor_info = get_monitor_info()
    primary_index = saved_monitor_info['primary_index']
    print('height :', saved_monitor_info['size'][primary_index]['height'])
    print('width :', saved_monitor_info['size'][primary_index]['width'])
    print('x_offset :', saved_monitor_info['size'][primary_index]['x_offset'])
    print('y_offset :', saved_monitor_info['size'][primary_index]['y_offset'])
    print('count :', saved_monitor_info['count'])
