import torch

from . import misc


def sync_state(network, src = 0):
    if misc.get_world_size() == 1: return
    tensor_list = list(network.state_dict().values())
    if src == 'all':
        misc.all_reduce_mean(tensor_list)
    else:
        misc.broadcast(tensor_list, src)

def sync_grad_mean(network):
    if misc.get_world_size() == 1: return
    misc.all_reduce_mean([param.grad.data for param in network.parameters() if param.grad is not None])

def sync_grad_sum(network):
    if misc.get_world_size() == 1: return
    misc.all_reduce_sum([param.grad.data for param in network.parameters() if param.grad is not None])

def sync_bn_stat(network):
    if misc.get_world_size() == 1: return
    tensor_list = []
    for mod in network.modules():
        if type(mod) == torch.nn.BatchNorm2d:
            tensor_list.append(mod.running_mean)
            tensor_list.append(mod.running_var)
    misc.all_reduce_mean(tensor_list)
