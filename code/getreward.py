# -*- coding:utf-8 -*-

def GetMaxbw(graph=None):
    edge_list = list(graph.edges())
    Maxbw = -999
    for edge in edge_list:
        if 'bw' in graph.edges[edge]:
            if graph.edges[edge]['bw'] > Maxbw:
                Maxbw = graph.edges[edge]['bw']
    #print "Maxbw:", Maxbw
    return Maxbw


def GetMinbw(graph=None):
    edge_list = list(graph.edges())
    Minbw = 999
    for edge in edge_list:
        if 'bw' in graph.edges[edge]:
            if graph.edges[edge]['bw'] < Minbw and graph.edges[edge]['bw'] != 0:
                Minbw = graph.edges[edge]['bw']
    #print "Minbw:", Minbw
    return Minbw
def GetMaxdelay(graph=None):
    edge_list = list(graph.edges())
    Maxdelay = 0
    for edge in edge_list:
        if 'delay' in graph.edges[edge]:
            if graph.edges[edge]['delay'] > Maxdelay:
                 Maxdelay = graph.edges[edge]['delay']
    return Maxdelay

def GetMaxloss(graph=None):
    edge_list = list(graph.edges())
    Maxloss = 0
    for edge in edge_list:
        if 'loss' in graph.edges[edge]:
            if graph.edges[edge]['loss'] > Maxloss:
                 Maxloss = graph.edges[edge]['loss']
    if Maxloss == 0:
        Maxloss = 1
    return Maxloss



# def GetReward(graph=None, multicast_tree = None):
#     # 单步奖励
#     if graph is None or multicast_tree is None:
#         raise ValueError("graph and multicast_tree must be provided")
#         # 在这里使用 graph 进行一些操作
#
#     #print("Graph nodes:", graph.nodes())
#
#     #print("Graph edges:", graph.edges())
#
#
#
#     #Maxbw = GetMaxbw(graph)
#     n = graph.number_of_nodes()
#     Minbw = GetMinbw(graph)
#     Maxdelay = GetMaxdelay(graph)
#     Maxloss = GetMaxloss(graph)
#     #Mindelay = GetMindelay(graph)
#     #print "Minbw", Minbw
#     #print "Maxdelay", Maxdelay
#     #print "Maxloss", Maxloss
#     if len(multicast_tree)==1:
#
#         # 初始化边列表
#
#         edges_d1 = []
#         path_d1 = multicast_tree[0]
#         cost = 0
#         for i in range(len(path_d1) - 1):
#             edges_d1.append((path_d1[i], path_d1[i + 1]))
#         for edge in edges_d1:
#             bw = graph.edges[edge]['bw']
#             delay = graph.edges[edge]['delay']
#             loss = graph.edges[edge]['loss']
#             if bw == 0:
#                 x = 1
#             else:
#                 x = Minbw/bw
#             cost += x + delay/Maxdelay + loss/Maxloss
#             #cost += -bw/Maxbw + delay/Mindelay
# 	    #print "cost", cost
#         reward1 = cost + len(path_d1)/(6*n)
#         reward = -reward1
#
#     elif len(multicast_tree)==2:
#
#         # 初始化边列表
#         edges_d1 = []
#         edges_d2 = []
#         path_d1 = multicast_tree[0]
#         path_d2 = multicast_tree[1]
#         for i in range(len(path_d1) - 1):
#             edges_d1.append((path_d1[i], path_d1[i + 1]))
#
#         for i in range(len(path_d2) - 1):
#             edges_d2.append((path_d2[i], path_d2[i + 1]))
#         # 合并 edges_d1 和 edges_d2 到 edges_all
#         edges_all = edges_d1 + edges_d2
#         cost1 = 0
#         cost2 = 0
#         for edge in edges_d1:
#             bw = graph.edges[edge]['bw']
#             delay = graph.edges[edge]['delay']
#             loss = graph.edges[edge]['loss']
#             if bw == 0:
#                 x = 1
#             else:
#                 x = Minbw/bw
#         cost1 += x + delay/Maxdelay + loss/Maxloss
#         #cost1 += Minbw/bw + delay/Maxdelay + loss/Maxloss
#             #cost1 += -bw/Maxbw + delay / Mindelay
#         for edge in edges_d2:
#             bw = graph.edges[edge]['bw']
#             delay = graph.edges[edge]['delay']
#         loss = graph.edges[edge]['loss']
#         if bw == 0:
#             x = 1
#         else:
#             x = Minbw/bw
#         cost2 += x + delay/Maxdelay + loss/Maxloss
#         reward1 = cost1 + cost2 + len(path_d1)/(12*n) + len(path_d2)/(12*n)
#         reward = -reward1
#         #cost2 += Minbw/bw + delay/Maxdelay + loss/Maxloss
#         #cost2 += -bw/Maxbw + delay / Mindelay
#     elif len(multicast_tree) == 3:
#
#         # 初始化边列表
#         edges_d1 = []
#         edges_d2 = []
#         edges_d3 = []
#         path_d1 = multicast_tree[0]
#         path_d2 = multicast_tree[1]
#         path_d3 = multicast_tree[2]
#         for i in range(len(path_d1) - 1):
#             edges_d1.append((path_d1[i], path_d1[i + 1]))
#         for i in range(len(path_d2) - 1):
#             edges_d2.append((path_d2[i], path_d2[i + 1]))
#         for i in range(len(path_d3) - 1):
#             edges_d3.append((path_d3[i], path_d3[i + 1]))
#         # 合并 edges_d1 和 edges_d2 到 edges_all
#         edges_all = edges_d1 + edges_d2 + edges_d3
#
#
#         cost1 = 0
#         cost2 = 0
#         cost3 = 0
#         for edge in edges_d1:
#             bw = graph.edges[edge]['bw']
#             delay = graph.edges[edge]['delay']
#             loss = graph.edges[edge]['loss']
#             if bw == 0:
#                 x = 1
#             else:
#                 x = Minbw/bw
#             cost1 += x + delay/Maxdelay + loss/Maxloss
#             #cost1 += Minbw/bw + delay/Maxdelay + loss/Maxloss
#             #cost1 += -bw/Maxbw + delay / Mindelay
#         for edge in edges_d2:
#             bw = graph.edges[edge]['bw']
#             delay = graph.edges[edge]['delay']
#             loss = graph.edges[edge]['loss']
#             if bw == 0:
#                 x = 1
#             else:
#                 x = Minbw/bw
#             cost2 += x + delay/Maxdelay + loss/Maxloss
#             #cost2 += Minbw/bw + delay/Maxdelay + loss/Maxloss
#             #cost2 += -bw/Maxbw + delay / Mindelay
#         for edge in edges_d3:
#             bw = graph.edges[edge]['bw']
#             delay = graph.edges[edge]['delay']
#             loss = graph.edges[edge]['loss']
#             if bw == 0:
#                 x = 1
#             else:
#                 x = Minbw/bw
#             cost3 += x + delay/Maxdelay + loss/Maxloss
#             #cost3 += Minbw/bw + delay/Maxdelay + loss/Maxloss
#             #cost3 += -bw/Maxbw + delay / Mindelay
#         reward1 = cost1 + cost2 +cost3 + len(path_d1)/(18*n) + len(path_d2)/(18*n) + len(path_d3)/(18*n)
#         reward = -reward1
#     return reward








'''
def GetMindelay(graph=None):
    edge_list = list(graph.edges())
    Mindelay = float('inf')  # 初始值设为无穷大
    for edge in edge_list:
        if 'delay' in graph.edges[edge]:
            delay = graph.edges[edge]['delay']
            if delay != 0 and delay < Mindelay:
                Mindelay = delay
    # 如果没有找到合适的最小值，则设定一个默认值
    if Mindelay == float('inf'):
        Mindelay = 1  # 可以根据实际情况调整默认值
    print("Mindelay", Mindelay)
    return Mindelay
'''




'''
def GetMindelay(graph=None):
    edge_list = list(graph.edges())
    Mindelay = 999
    for edge in edge_list:
        if 'delay' in graph.edges[edge]:
            if graph.edges[edge]['delay'] < Mindelay and graph.edges[edge]['delay'] != 0:
                Mindelay = graph.edges[edge]['delay']
    #print "Mindelay", Mindelay
    return Mindelay
'''

'''
def GetMindelay(graph=None):
    edge_list = list(graph.edges())
    Mindelay = 999
    for edge in edge_list:
        if 'delay' in graph.edges[edge]:
            if graph.edges[edge]['delay'] < Mindelay:
                Mindelay = graph.edges[edge]['delay']
    #print "Mindelay", Mindelay
    return Mindelay
'''

'''
def Get_edge_count(graph=None, current_graph=None):

    return 1
‘’‘












’‘’
def GetReward(graph=None, multicast_tree = None):
    # 单步奖励
    if graph is None or multicast_tree is None:
        raise ValueError("graph and multicast_tree must be provided")
        # 在这里使用 graph 进行一些操作
    #print("Graph nodes:", graph.nodes())
    #print("Graph edges:", graph.edges())

    Maxbw = GetMaxbw(graph)
    # Minbw = GetMinbw(graph)
    # Maxdelay = GetMaxdelay(graph)
    Mindelay = 0.00032317638397216797


    if len(multicast_tree)==1:
        # 初始化边列表
        edges_d1 = []
        path_d1 = multicast_tree[0]
        cost = 0
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost += bw/Maxbw + delay/Mindelay
        reward1 = cost
        reward = -reward1

    elif len(multicast_tree)==2:

        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2
        cost1 = 0
        cost2 = 0
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost1 += bw/Maxbw + delay / Mindelay
        for edge in edges_d2:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost2 += bw/Maxbw + delay / Mindelay
        reward1_all = 0
        reward2_all = 0
        for edge in edges_d1:
            flag1 = 0
            flag2 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2))
            elif flag1:
                reward1 = bw/Maxbw + delay / Mindelay
            reward1_all += reward1
        for edge in edges_d2:
            flag1 = 0
            flag2 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward2 = cost * len(edges_d2) / (len(edges_d1) + len(edges_d2))
            elif flag2:
                reward2 = bw/Maxbw + delay / Mindelay
            reward2_all += reward2
        reward = -(reward1_all + reward2_all)
    elif len(multicast_tree) == 3:

        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        edges_d3 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        path_d3 = multicast_tree[2]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        for i in range(len(path_d3) - 1):
            edges_d3.append((path_d3[i], path_d3[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2 + edges_d3

        cost1 = 0
        cost2 = 0
        cost3 = 0
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost1 += bw/Maxbw + delay / Mindelay
        for edge in edges_d2:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost2 += bw/Maxbw + delay / Mindelay
        for edge in edges_d3:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost3 += bw/Maxbw + delay / Mindelay

        reward1_all = 0
        reward2_all = 0
        reward3_all = 0
        for edge in edges_d1:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag1 and flag2 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2) + len(edges_d3))
            elif flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2))
            elif flag1 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d3))
            elif flag1:
                reward1 = bw/Maxbw + delay / Mindelay
            reward1_all += reward1
        for edge in edges_d2:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag2 and flag1 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward2 = cost * len(edges_d2) / (len(edges_d1) + len(edges_d2) + len(edges_d3))
            elif flag2 and flag1:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward2 = cost * len(edges_d2) / (len(edges_d2) + len(edges_d1))
            elif flag2 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward2 = cost * len(edges_d2) / (len(edges_d2) + len(edges_d3))
            elif flag2:
                reward2 = bw/Maxbw + delay / Mindelay
            reward2_all += reward2
        for edge in edges_d3:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag3 and flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d1) + len(edges_d2))
            elif flag3 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d2))
            elif flag3 and flag1:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = bw/Maxbw + delay / Mindelay
                reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d1))
            elif flag3:
                reward3 = bw/Maxbw + delay / Mindelay
            reward3_all += reward3

        reward = -(reward1_all + reward2_all + reward3_all)
    return reward
'''


#zhuyao终

def GetReward(graph=None, multicast_tree = None):
    # 单步奖励
    if graph is None or multicast_tree is None:
        raise ValueError("graph and multicast_tree must be provided")
        # 在这里使用 graph 进行一些操作

    #print("Graph nodes:", graph.nodes())

    #print("Graph edges:", graph.edges())
    #print("Number of nodes:", graph.number_of_nodes())
    n = graph.number_of_nodes()
    #print("Number of nodes:", n)
    #Maxbw = GetMaxbw(graph)

    Minbw = GetMinbw(graph)

    Maxdelay = GetMaxdelay(graph)

    Maxloss = GetMaxloss(graph)

    #Mindelay = GetMindelay(graph)

    # print ("Minbw", Minbw)
    #
    # print ("Maxdelay", Maxdelay)
    #
    # print ("Maxloss", Maxloss)



    if len(multicast_tree)==1:

        # 初始化边列表

        edges_d1 = []
        path_d1 = multicast_tree[0]
        cost = 0
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            loss = graph.edges[edge]['loss']
            if bw == 0:
                x = 1
            else:
                x = Minbw/bw
            cost += x + delay/Maxdelay + loss/Maxloss
            #cost += -bw/Maxbw + delay/Mindelay
	    #print "cost", cost
        reward1 = cost + len(path_d1)/(3*n)
        reward = -reward1

    elif len(multicast_tree)==2:

        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))

        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2
        cost1 = 0
        cost2 = 0
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            loss = graph.edges[edge]['loss']
            if bw == 0:
                x = 1
            else:
                x = Minbw/bw
            cost1 += x + delay/Maxdelay + loss/Maxloss
            #cost1 += Minbw/bw + delay/Maxdelay + loss/Maxloss
            #cost1 += -bw/Maxbw + delay / Mindelay
        for edge in edges_d2:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            loss = graph.edges[edge]['loss']
            if bw == 0:
                x = 1
            else:
                x = Minbw/bw
            cost2 += x + delay/Maxdelay + loss/Maxloss
            #cost2 += Minbw/bw + delay/Maxdelay + loss/Maxloss
            #cost2 += -bw/Maxbw + delay / Mindelay
        reward1_all = 0
        reward2_all = 0
        for edge in edges_d1:
            flag1 = 0
            flag2 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2))
                x2 = cost1 / (cost1 + cost2)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward1 = y2 * cost * cost1 / (cost1 + cost2)

            elif flag1:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                reward1 = x + delay/Maxdelay + loss/Maxloss
                #reward1 = Minbw/bw + delay/Maxdelay + loss/Maxloss
            reward1_all += reward1
        for edge in edges_d2:
            flag1 = 0
            flag2 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                x2 = cost2 / (cost1 + cost2)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward2 = y2 * cost * cost2 / (cost1 + cost2)
                #reward2 = cost * cost2 / (cost2 + cost1)
            elif flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                reward2 = x + delay/Maxdelay + loss/Maxloss
                #reward2 = Minbw/bw + delay/Maxdelay + loss/Maxloss
            reward2_all += reward2
        reward2_len = reward1_all + reward2_all + len(path_d1)/(6*n) + len(path_d2)/(6*n)
        reward = -(reward2_len)
    elif len(multicast_tree) == 3:

        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        edges_d3 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        path_d3 = multicast_tree[2]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        for i in range(len(path_d3) - 1):
            edges_d3.append((path_d3[i], path_d3[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2 + edges_d3


        cost1 = 0
        cost2 = 0
        cost3 = 0
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            loss = graph.edges[edge]['loss']
            if bw == 0:
                x = 1
            else:
                x = Minbw/bw
            cost1 += x + delay/Maxdelay + loss/Maxloss
            #cost1 += Minbw/bw + delay/Maxdelay + loss/Maxloss
            #cost1 += -bw/Maxbw + delay / Mindelay
        for edge in edges_d2:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            loss = graph.edges[edge]['loss']
            if bw == 0:
                x = 1
            else:
                x = Minbw/bw
            cost2 += x + delay/Maxdelay + loss/Maxloss
            #cost2 += Minbw/bw + delay/Maxdelay + loss/Maxloss
            #cost2 += -bw/Maxbw + delay / Mindelay
        for edge in edges_d3:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            loss = graph.edges[edge]['loss']
            if bw == 0:
                x = 1
            else:
                x = Minbw/bw
            cost3 += x + delay/Maxdelay + loss/Maxloss
            #cost3 += Minbw/bw + delay/Maxdelay + loss/Maxloss
            #cost3 += -bw/Maxbw + delay / Mindelay

        reward1_all = 0
        reward2_all = 0
        reward3_all = 0
        for edge in edges_d1:
            flag1 = 0
            flag2 = 0

            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag1 and flag2 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2) + len(edges_d3))
                x2 = cost1 / (cost1 + cost2 + cost3)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward1 = y2 * cost * cost1 / (cost1 + cost2 + cost3)
                #reward1 = cost * cost1 / (cost1 + cost2 + cost3)
            elif flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2))
                x2 = cost1 / (cost1 + cost2)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward1 = y2 * cost * cost1 / (cost1 + cost2)
                #reward1 = cost * cost1 / (cost1 + cost2)
            elif flag1 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d3))
                x2 = cost1 / (cost1 + cost3)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward1 = y2 * cost1 / (cost1 + cost3)
                #reward1 = cost * cost1 / (cost1 + cost3)
            elif flag1:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                reward1 = x + delay/Maxdelay + loss/Maxloss
                #reward1 = Minbw/bw + delay/Maxdelay + loss/Maxloss
            reward1_all += reward1
        for edge in edges_d2:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag2 and flag1 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward2 = cost * len(edges_d2) / (len(edges_d1) + len(edges_d2) + len(edges_d3))
                x2 = cost2 / (cost1 + cost2 + cost3)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward2 = y2 * cost * cost2 / (cost1 + cost2 + cost3)
                #reward2 = cost * cost2 / (cost1 + cost2 + cost3)
            elif flag2 and flag1:

                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward2 = cost * len(edges_d2) / (len(edges_d2) + len(edges_d1))
                x2 = cost2 / (cost2 + cost1)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward2 = y2 * cost * cost2 / (cost2 + cost1)
                #reward2 = cost * cost2 / (cost2 + cost1)
            elif flag2 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward2 = cost * len(edges_d2) / (len(edges_d2) + len(edges_d3))
                x2 = cost2 / (cost2 + cost3)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward2 = y2 * cost * cost2 / (cost2 + cost3)
                #reward2 = cost * cost2 / (cost2 + cost3)
            elif flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                reward2 = x + delay/Maxdelay + loss/Maxloss
                #reward2 = Minbw/bw + delay/Maxdelay + loss/Maxloss
            reward2_all += reward2
        for edge in edges_d3:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag3 and flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d1) + len(edges_d2))
                x2 = cost3 / (cost1 + cost2 + cost3)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward3 = y2 * cost * cost3 / (cost1 + cost2 + cost3)
                #reward3 = cost * cost3 / (cost1 + cost2 + cost3)
            elif flag3 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d2))
                x2 = cost3 / (cost3 + cost2)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward3 = y2 * cost * cost3 / (cost3 + cost2)
                #reward3 = cost * cost3 / (cost3 + cost2)
            elif flag3 and flag1:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                cost = x + delay/Maxdelay + loss/Maxloss
                #cost = Minbw/bw + delay/Maxdelay + loss/Maxloss
                #cost = -bw/Maxbw + delay / Mindelay
                #reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d1))
                x2 = cost3 / (cost3 + cost1)
                if 0 <= x2 < 0.5:
                    y2 = 4 * x2 * (1 - x2)
                elif 0.5 <= x2 <= 1:
                    y2 = 4 * x2 * (x2 - 1) + 2
                reward3 = y2 * cost * cost3 / (cost3 + cost1)
                #reward3 = cost * cost3 / (cost3 + cost1)
            elif flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                loss = graph.edges[edge]['loss']
                if bw == 0:
                    x = 1
                else:
                    x = Minbw/bw
                reward3 = x + delay/Maxdelay + loss/Maxloss
                #reward3 = Minbw/bw + delay/Maxdelay + loss/Maxloss
            reward3_all += reward3
        reward3_len = reward1_all + reward2_all + reward3_all + len(path_d1)/(9*n) + len(path_d1)/(9*n) + len(path_d1)/(9*n)
        reward = -(reward3_len)
    return reward


'''
#zhuyao

def GetReward(graph=None, multicast_tree = None):
    # 单步奖励
    if graph is None or multicast_tree is None:
        raise ValueError("graph and multicast_tree must be provided")
        # 在这里使用 graph 进行一些操作
    #print("Graph nodes:", graph.nodes())
    #print("Graph edges:", graph.edges())

    #Maxbw = GetMaxbw(graph)
    Minbw = GetMinbw(graph)
    Maxdelay = GetMaxdelay(graph)
    Maxloss = GetMaxloss(graph)
    #Mindelay = GetMindelay(graph)
    print "Minbw", Minbw
    print "Maxdelay", Maxdelay
    print "Maxloss", Maxloss

    if len(multicast_tree)==1:
        # 初始化边列表
        edges_d1 = []
        path_d1 = multicast_tree[0]
        cost = 0
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
	    loss = graph.edges[edge]['loss']
	    cost += Minbw/bw + delay/Maxdelay + loss/Maxloss
            #cost += -bw/Maxbw + delay/Mindelay
	    #print "cost", cost
        reward1 = cost
        reward = -reward1

    elif len(multicast_tree)==2:

        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2
        cost1 = 0
        cost2 = 0
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost1 += -bw/Maxbw + delay / Mindelay
        for edge in edges_d2:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost2 += -bw/Maxbw + delay / Mindelay
        reward1_all = 0
        reward2_all = 0
        for edge in edges_d1:
            flag1 = 0
            flag2 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2))
                reward1 = cost * cost1 / (cost1 + cost2)
            elif flag1:
                reward1 = -bw/Maxbw + delay / Mindelay
            reward1_all += reward1
        for edge in edges_d2:
            flag1 = 0
            flag2 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                reward2 = cost * cost2 / (cost2 + cost1)
            elif flag2:
                reward2 = -bw/Maxbw + delay / Mindelay
            reward2_all += reward2
        reward = -(reward1_all + reward2_all)
    elif len(multicast_tree) == 3:

        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        edges_d3 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        path_d3 = multicast_tree[2]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        for i in range(len(path_d3) - 1):
            edges_d3.append((path_d3[i], path_d3[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2 + edges_d3

        cost1 = 0
        cost2 = 0
        cost3 = 0
        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost1 += -bw/Maxbw + delay / Mindelay
        for edge in edges_d2:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost2 += -bw/Maxbw + delay / Mindelay
        for edge in edges_d3:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost3 += -bw/Maxbw + delay / Mindelay

        reward1_all = 0
        reward2_all = 0
        reward3_all = 0
        for edge in edges_d1:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag1 and flag2 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2) + len(edges_d3))
                reward1 = cost * cost1 / (cost1 + cost2 + cost3)
            elif flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d2))
                reward1 = cost * cost1 / (cost1 + cost2)
            elif flag1 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward1 = cost * len(edges_d1) / (len(edges_d1) + len(edges_d3))
                reward1 = cost * cost1 / (cost1 + cost3)
            elif flag1:
                reward1 = -bw/Maxbw + delay / Mindelay
            reward1_all += reward1
        for edge in edges_d2:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag2 and flag1 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward2 = cost * len(edges_d2) / (len(edges_d1) + len(edges_d2) + len(edges_d3))
                reward2 = cost * cost2 / (cost1 + cost2 + cost3)
            elif flag2 and flag1:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward2 = cost * len(edges_d2) / (len(edges_d2) + len(edges_d1))
                reward2 = cost * cost2 / (cost2 + cost1)
            elif flag2 and flag3:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward2 = cost * len(edges_d2) / (len(edges_d2) + len(edges_d3))
                reward2 = cost * cost2 / (cost2 + cost3)
            elif flag2:
                reward2 = -bw/Maxbw + delay / Mindelay
            reward2_all += reward2
        for edge in edges_d3:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag3 and flag1 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d1) + len(edges_d2))
                reward3 = cost * cost3 / (cost1 + cost2 + cost3)
            elif flag3 and flag2:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d2))
                reward3 = cost * cost3 / (cost3 + cost2)
            elif flag3 and flag1:
                bw = graph.edges[edge]['bw']
                delay = graph.edges[edge]['delay']
                cost = -bw/Maxbw + delay / Mindelay
                #reward3 = cost * len(edges_d3) / (len(edges_d3) + len(edges_d1))
                reward3 = cost * cost3 / (cost3 + cost1)
            elif flag3:
                reward3 = -bw/Maxbw + delay / Mindelay
            reward3_all += reward3

        reward = -(reward1_all + reward2_all + reward3_all)
    return reward
'''






# def GetReward(graph=None, multicast_tree = None):
#     # 单步奖励
#     if graph is None or multicast_tree is None:
#         raise ValueError("graph and multicast_tree must be provided")
#         # 在这里使用 graph 进行一些操作
#     #print("Graph nodes:", graph.nodes())
#     #print("Graph edges:", graph.edges())
#
#     #Maxbw = GetMaxbw(graph)
#     # Minbw = GetMinbw(graph)
#     # Maxdelay = GetMaxdelay(graph)
#     #Mindelay = 0.00032317638397216797
#
#
#     if len(multicast_tree)==1:
#         # 初始化边列表
#         edges_d1 = []
#         path_d1 = multicast_tree[0]
#         cost = 0
#         for i in range(len(path_d1) - 1):
#             edges_d1.append((path_d1[i], path_d1[i + 1]))
#         reward1 = len(edges_d1)
#         reward = -reward1
#
#     elif len(multicast_tree)==2:
#
#         # 初始化边列表
#         edges_d1 = []
#         edges_d2 = []
#         path_d1 = multicast_tree[0]
#         path_d2 = multicast_tree[1]
#         for i in range(len(path_d1) - 1):
#             edges_d1.append((path_d1[i], path_d1[i + 1]))
#         for i in range(len(path_d2) - 1):
#             edges_d2.append((path_d2[i], path_d2[i + 1]))
#         # 合并 edges_d1 和 edges_d2 到 edges_all
#         edges_all = edges_d1 + edges_d2
#         cost1 = len(edges_d1)
#         cost2 = len(edges_d2)
#         reward = -(cost1 + cost2)
#     elif len(multicast_tree) == 3:
#
#         # 初始化边列表
#         edges_d1 = []
#         edges_d2 = []
#         edges_d3 = []
#         path_d1 = multicast_tree[0]
#         path_d2 = multicast_tree[1]
#         path_d3 = multicast_tree[2]
#         for i in range(len(path_d1) - 1):
#             edges_d1.append((path_d1[i], path_d1[i + 1]))
#         for i in range(len(path_d2) - 1):
#             edges_d2.append((path_d2[i], path_d2[i + 1]))
#         for i in range(len(path_d3) - 1):
#             edges_d3.append((path_d3[i], path_d3[i + 1]))
#         # 合并 edges_d1 和 edges_d2 到 edges_all
#         edges_all = edges_d1 + edges_d2 + edges_d3
#
#         cost1 = len(edges_d1)
#         cost2 = len(edges_d2)
#         cost3 = len(edges_d3)
#         reward = -(cost1 + cost2 + cost3)
#     return reward



'''
def GetReward(graph=None, multicast_tree = None):
    # 单步奖励
    if graph is None or multicast_tree is None:
        raise ValueError("graph and multicast_tree must be provided")
        # 在这里使用 graph 进行一些操作
    #print("Graph nodes:", graph.nodes())
    #print("Graph edges:", graph.edges())

    Maxbw = GetMaxbw(graph)
    # Minbw = GetMinbw(graph)
    # Maxdelay = GetMaxdelay(graph)
    Mindelay = 0.00032317638397216797


    if len(multicast_tree)==1:
        # 初始化边列表
        edges_d1 = []
        path_d1 = multicast_tree[0]
        cost = 0
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))

        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost += bw/Maxbw + delay/Mindelay

        reward1 = cost
        reward = -reward1

    elif len(multicast_tree)==2:

        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2
        cost1 = 0
        cost2 = 0

        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost1 += bw/Maxbw + delay / Mindelay
        for edge in edges_d2:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost2 += bw/Maxbw + delay / Mindelay
        reward = -(cost1 + cost2)
    elif len(multicast_tree) == 3:

        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        edges_d3 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        path_d3 = multicast_tree[2]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        for i in range(len(path_d3) - 1):
            edges_d3.append((path_d3[i], path_d3[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2 + edges_d3

        cost1 = 0
        cost2 = 0
        cost3 = 0

        for edge in edges_d1:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost1 += bw/Maxbw + delay / Mindelay
        for edge in edges_d2:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost2 += bw/Maxbw + delay / Mindelay
        for edge in edges_d3:
            bw = graph.edges[edge]['bw']
            delay = graph.edges[edge]['delay']
            cost3 += bw/Maxbw + delay / Mindelay
        reward = -(cost1 + cost2 + cost3)
    return reward
'''





'''
def GetReward(graph=None, multicast_tree = None):
    # 单步奖励
    #print "计算奖励" 

    #Maxbw = GetMaxbw(graph)
    # Minbw = GetMinbw(graph)
    # Maxdelay = GetMaxdelay(graph)
    #Mindelay = GetMindelay(graph)


    if len(multicast_tree)==1:
        reward1 = len(multicast_tree[0])
        reward = -reward1
    elif len(multicast_tree)==2:
        reward1_all = 0
        reward2_all = 0
        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2
        for edge in edges_d1:
            flag1 = 0
            flag2 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if flag1 and flag2:
                reward1 = 1 * len(edges_d1) / (len(edges_d1) + len(edges_d2))
            elif flag1:
                reward1 = 1 * len(edges_d1) / len(edges_d1)
            reward1_all += reward1
        for edge in edges_d2:
            flag1 = 0
            flag2 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if flag1 and flag2:
                reward2 = 1 * len(edges_d2) / (len(edges_d1) + len(edges_d2))
            elif flag2:
                reward2 = 1 * len(edges_d2) / len(edges_d2)
            reward2_all += reward2
        reward = -(0.1*reward1_all + 0.9*reward2_all)
    elif len(multicast_tree) == 3:
        reward1_all = 0
        reward2_all = 0
        reward3_all = 0
        # 初始化边列表
        edges_d1 = []
        edges_d2 = []
        edges_d3 = []
        path_d1 = multicast_tree[0]
        path_d2 = multicast_tree[1]
        path_d3 = multicast_tree[2]
        for i in range(len(path_d1) - 1):
            edges_d1.append((path_d1[i], path_d1[i + 1]))
        for i in range(len(path_d2) - 1):
            edges_d2.append((path_d2[i], path_d2[i + 1]))
        for i in range(len(path_d3) - 1):
            edges_d3.append((path_d3[i], path_d3[i + 1]))
        # 合并 edges_d1 和 edges_d2 到 edges_all
        edges_all = edges_d1 + edges_d2 + edges_d3


        for edge in edges_d1:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag1 and flag2 and flag3:
                reward1 = 1 * len(edges_d1) / (len(edges_d1) + len(edges_d2) + len(edges_d3))
            elif flag1 and flag2:
                reward1 = 1 * len(edges_d1) / (len(edges_d1) + len(edges_d2))
            elif flag1 and flag3:
                reward1 = 1 * len(edges_d1) / (len(edges_d1) + len(edges_d3))
            elif flag1:
                reward1 = 1 * len(edges_d1) / len(edges_d1)
            reward1_all += reward1
        for edge in edges_d2:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag2 and flag1 and flag3:
                reward2 = 1 * len(edges_d2) / (len(edges_d1) + len(edges_d2) + len(edges_d3))
            elif flag2 and flag1:
                reward2 = 1 * len(edges_d2) / (len(edges_d2) + len(edges_d1))
            elif flag2 and flag3:
                reward2 = 1 * len(edges_d2) / (len(edges_d2) + len(edges_d3))
            elif flag2:
                reward2 = 1 * len(edges_d2) / len(edges_d2)
            reward2_all += reward2
        for edge in edges_d3:
            flag1 = 0
            flag2 = 0
            flag3 = 0
            if edge in edges_d1:
                flag1 = 1
            if edge in edges_d2:
                flag2 = 1
            if edge in edges_d3:
                flag3 = 1
            if flag3 and flag1 and flag2:
                reward3 = 1 * len(edges_d3) / (len(edges_d3) + len(edges_d1) + len(edges_d2))
            elif flag3 and flag2:
                reward3 = 1 * len(edges_d3) / (len(edges_d3) + len(edges_d2))
            elif flag3 and flag1:
                reward3 = 1 * len(edges_d3) / (len(edges_d3) + len(edges_d1))
            elif flag3:
                reward3 = 1 * len(edges_d3) / len(edges_d3)
            reward3_all += reward3

        reward = -(0.1*reward1_all + 0.2*reward2_all + 0.7*reward3_all)
    return reward
'''


'''def GetReward(graph=None, f=None,current_graph=None, edge_count=None, edge=None,path_to_d1=None,path_to_d2=None,path_to_d3=None,path_to_d1_edges=None,path_to_d2_edges=None,path_to_d3_edges=None):
    # 单步奖励
    flag1 = 0
    for e in path_to_d1_edges:
        if e == edge:  # 判断是否和当前边相同
            flag1=1  # 如果相同，Se加1
    flag2 = 0
    for e in path_to_d2_edges:
        if e == edge:  # 判断是否和当前边相同
            flag2 = 1  # 如果相同，Se加1
    flag3 = 0
    for e in path_to_d3_edges:
        if e == edge:  # 判断是否和当前边相同
            flag3 = 1  # 如果相同，Se加1

    # 获取 path_to_d1 中第二条路径的 value 值
    cost = len(path_to_d1_edges)
    print(cost)
    if flag1 and flag2 and flag3:
        new_cost = 1 * len(f) / len(path_to_d1_edges)+len(path_to_d2_edges)+len(path_to_d3_edges)  # All flags are set
    elif flag1 and flag2:
        new_cost = 1 * len(f) / len(path_to_d1_edges)+len(path_to_d2_edges)  # flag1 and flag2 are set
    elif flag1 and flag3:
        new_cost = 1 * len(f) / len(path_to_d1_edges)+len(path_to_d3_edges)  # flag1 and flag3 are set
    elif flag2 and flag3:
        new_cost = 1 * len(f) / len(path_to_d2_edges)+len(path_to_d3_edges)  # flag2 and flag3 are set
    elif flag1:
        new_cost = 1 * len(f) / len(path_to_d1_edges)  # Only flag1 is set
    elif flag2:
        new_cost = 1 * len(f) / len(path_to_d2_edges)  # Only flag2 is set
    elif flag3:
        new_cost = 1 * len(f) / len(path_to_d3_edges)  # Only flag3 is set
    else:
        new_cost = 0  # None of the flags are set
    return new_cost'''

















    # # 给path_to_d1中的每条路径赋值
    # if path_to_d1 is not None:
    #     for path in path_to_d1:
    #         value = len(path) - 1  # 计算路径的边的个数
    #         # 在这里使用value进行你想要的操作，比如打印或者存储
    #         print(value)  # 示例操作，打印每条路径的边的个数
    #
    # # 给path_to_d2中的每条路径赋值，同上
    # if path_to_d2 is not None:
    #     for path in path_to_d2:
    #         value = len(path) - 1
    #         print(value)
    #
    # # 给path_to_d3中的每条路径赋值，同上
    # if path_to_d3 is not None:
    #     for path in path_to_d3:
    #         value = len(path) - 1
    #         print(value)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # b1 = 0.5
    # b2 = 0.5
    # bw = graph.edges[edge]['bw']
    # bw = (bw - Minbw) / (Maxbw - Minbw)
    # delay = graph.edges[edge]['delay']
    # delay = (delay - Mindelay) / (Maxdelay - Mindelay)
    # reward = b1 * bw + b2 * (1 - delay)
    # return stepcoef * reward
    #
    # bwlist.append(graph.edges[edge]['bw'])
    # delaylist.append(graph.edges[edge]['delay'])
    # print "bwlist:", bwlist
    # print "delaylist:", delaylist
    # len1 = len(bwlist)
    # len2 = len(delaylist)
    # if len1 != len2:
    #     print "ERROR"
    # cost = (len1 - 1) / (13 - 1)
    # b1 = 0.5
    # b2 = 0.5
    # b3 = 0
    # bbw = 999
    # for m in bwlist:
    #     if m < bbw:
    #         bbw = m
    # tdelay = 0
    # for n in delaylist:
    #     tdelay = tdelay + n
    # bw = bbw
    # bw = (bw - Minbw) / (Maxbw - Minbw)
    # delay = tdelay
    # Maxtdelay = GetMaxtdelay(graph)
    # delay = (delay - Mindelay) / (Maxtdelay - Mindelay)
    # reward = b1 * bw + b2 * (1 - delay) + b3 * (1 - cost)
    # print "tdelay:", tdelay
    # print "bbw:", bbw
    # print "cost:", cost
    # return reward
