# -*- coding: UTF-8 -*-
import numpy as np
import math


# 归并排序
def sort(a,begin,end):
    mid = int((begin+end)/2)
    if begin<end-1:
        sort(a,begin,mid)
        sort(a,mid,end)
        a[begin:end] = combine(a,begin,mid,end)

def combine(a, begin, mid, end):
    i = begin
    j = mid
    temp=[]
    while i<mid and j<end:
        if a[i]<a[j]:
            temp.append(a[i])
            i+=1
        else:
            temp.append(a[j])
            j+=1
    while i<mid:
        temp.append(a[i])
        i+=1
    while j<end:
        temp.append(a[j])
        j+=1
    return temp
# a=[9,8,7,6,5,4,3,2,2,1,1,10]
# sort(a,0,len(a))
# print a


class KD_node:                          # 定义kd-tree的节点，节点就是用来划分空间的标记
    def __init__(self,point, split_dim, left_child=None, right_child=None):
        self.point = point              # 被选中用于空间划分的样本点
        self.split_dim = split_dim      # 用于进行此次空间划分的样本属性（维度）
        self.left_child = left_child    # 当前节点的左孩子，即划分当前空间得到的左子空间
        self.right_child = right_child  # 当前节点的右孩子，即划分当前空间得到的右子空间


def selectSplitDim(pointset):           # 选择每个kd-tree节点的划分属性，在待划分区间的所有样本中，方差最大的属性被筛选作为split_dim
    dim_len = len(pointset[0])          # 每个样本包含的属性个数
    max_var = 0
    max_var_dim = 0

    for i in range(dim_len):
        pointset = np.array(pointset)
        var = np.var(pointset[:,i])
        if var>max_var:
            max_var = var
            max_var_dim = i

    return max_var_dim


def selectNode(pointset, split_dim):    # 根据当前空间样本方差最大的属性，选取该在这些属性值中处于中位数的样本作为本次空间划分的根节点
    featurelist=[]
    for i in range(len(pointset)):
        featurelist.append(pointset[i][split_dim])
    sort(featurelist,0,len(featurelist))
    midindex = int(len(featurelist)/2)
    midvalue = featurelist[midindex]
    for i in range(len(pointset)):
        if pointset[i][split_dim]==midvalue:
            return pointset[i]



def kdTreeCreator(pointset):            # 生成kd-Tree
    if len(pointset)<=1:
        root = KD_node(pointset[0],0)
    else:
        dim_index = selectSplitDim(pointset)
        split_point = selectNode(pointset, dim_index)
        root = KD_node(split_point,dim_index)
        leftset = []
        rightset = []
        for i in range(len(pointset)):
            if pointset[i][dim_index]<split_point[dim_index]:
                leftset.append(pointset[i])
            else:
                rightset.append(pointset[i])
        root.left_child = kdTreeCreator(leftset)
        root.right_child = kdTreeCreator(rightset)
    return root

def computeDist(pointA, pointB):
    dist=0
    for i in range(len(pointA)):
        dist+=(pointA[i]-pointB[i])*(pointA[i]-pointB[i])
    return math.sqrt(dist)


def selectKnearest(pointset , target, k):   # 找出k近邻
    resultset=[]
    min_dist_set=[]
    for topk in range(k):
        root = kdTreeCreator(pointset)
        root_Set = []                      # 定义待会需要回溯的节点集
        NN = None
        min_dist = 10000
        # 扫描到离目标最近的叶子节点，再回溯，回溯是判断目标距离当前分割平面的距离是否大于其与当前最近点的距离，如果比当前最近距离大，
        # 则不需要考虑分割平面的子空间，继续回溯，否则，进入该分割平面对应的子空间搜索
        # 扫描至叶子节点
        while root:
            root_Set.append(root)
            if computeDist(target,root.point)<min_dist:
                min_dist=computeDist(target,root.point)
                NN = root.point
            dim_index=root.split_dim
            if root.point[dim_index]>target[dim_index]:
                root = root.left_child
            else:
                root = root.right_child

        # 回溯
        while root_Set:
            back_point = root_Set.pop()
            dim_index = back_point.split_dim

            temp_root = None
            if abs(back_point.point[dim_index]-target[dim_index])<min_dist: # 判断是否需要到当前分割点的子空间搜索，若当前最近邻距离大于目标点距离分割平面的距离，
                                                                            # 那么在子空间有可能存在离目标点更近的点，去其子空间搜索，并将经历点加入到回溯栈
                if target[dim_index]<back_point.point[dim_index]:
                    temp_root = back_point.right_child
                else:
                    temp_root=back_point.left_child
            if temp_root:                                                   # 子空间有可能有更近的点，去瞧瞧，真有的话要加入回溯栈
                root_Set.append(temp_root)
                d = computeDist(temp_root.point,target)
                if d<min_dist:
                    min_dist=d
                    NN = temp_root.point

        resultset.append(NN)
        min_dist_set.append(min_dist)
        index_ = pointset.index(NN)
        pointset.pop(index_)
    return min_dist_set, resultset

def rootFistScan(root):
    if root==None:
        print ' '
        return
    else:
        print root.point
        rootFistScan(root.left_child)
        rootFistScan(root.right_child)

a=[1,2]
b=[1,3]
c=[1,4]
d=[1,5]
e=[1,6]
f=[1,7]
g=[1,8]
h=[1,9]
t=[1,5.5]
pointset=[a,b,c,d,e,f,g,h]
# rootFistScan(root)
distance, point = selectKnearest(pointset,t,3)
print distance
print point
