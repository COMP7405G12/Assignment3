import numpy as np
import types
class BinaryTreeNode:
    def __init__(self,data,left,right):
        self.left = left
        self.data = data
        self.right = right

class Binomial:
    def __init__(self,S,v,K,r,T,n,type):
        self.T = float(T)
        self.S = float(S)
        self.K = float(K)
        self.type = type
        self.r = r
        self.delt_t = self.T/n
        self.u = np.exp(v*np.sqrt(self.delt_t))
        self.d = 1/self.u
        self.p = (np.exp(r*self.delt_t) - self.d)/(self.u - self.d)
        self.levels = n

    def execute(self):
        binary_tree = self.makeTree(self.S,0)
        #self.presentTree(binary_tree)
        return binary_tree.data

    def presentTree(self,tree):
        if isinstance(tree,BinaryTreeNode):
            print tree.data
            self.presentTree(tree.left)
            self.presentTree(tree.right)
        else:
            print tree


    def makeTree(self,S,n):
        if n == self.levels:
            return self.get_f_value(S)
        u_node = self.makeTree(S*self.u,n+1)
        d_node = self.makeTree(S*self.d,n+1)
        if isinstance(u_node,BinaryTreeNode):
            u_value = u_node.data
        else:
            u_value = u_node
        if isinstance(d_node,BinaryTreeNode):
            d_value = d_node.data
        else:
            d_value = d_node
        b_value = np.exp(-1*self.r*self.delt_t)*(self.p*u_value + (1 - self.p)*d_value)
        f_value = self.get_f_value(S)
        value = max(b_value,f_value)
        return BinaryTreeNode(value,u_node,d_node)

    def get_f_value(self,S):
        if self.type == "call":
            return max(float((S - self.K)), float(0))
        elif self.type == "put":
            return max(float(self.K - S), float(0))
        else:
            return float(0)

if __name__ == "__main__":
    test = Binomial(50,0.223144,52,0.05,2,2,"put")
    print test.execute()
    #test computing capacity
    n = 30
    total = np.power(2,n+1)-1
    a = []
    for i in range(0,total):
        a.append(i)
    max = a[0]
    for i in range(0,len(a)):
        if i > max:
            max = i
    print max



