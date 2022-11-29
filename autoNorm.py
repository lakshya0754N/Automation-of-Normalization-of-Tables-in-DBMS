from table import Table
import pandas as pd
import numpy as np

class AutoNormalization:
    def __init__(self, csvPath, tableName, dataframe=None):
        if dataframe is not None:
            self.orgTable = Table("", tableName, dataframe)
            self.data = [Table("", tableName, dataframe)]
        else:
            self.orgTable = Table(csvPath, tableName)
            self.data = [Table(csvPath, tableName)]
        self.idx = 0
        self.autoNormalize()
        
    # function to check for 1NF
    def is1NF(self):
        for i in range(self.data[self.idx].numOfAttributes):
            for j in range(self.data[self.idx].table.shape[0]):
                if (isinstance(self.data[self.idx].table[self.data[self.idx].attributes[i]][j], list)):
                    return False, [self.data[self.idx].attributes[i], self.data[self.idx].table[self.data[self.idx].attributes[i]][j]]
        return True, None
    
    # function to check for partial dependencies
    def isPartialDependency(self):
        for fd in self.data[self.idx].functionalDependencies:
            left = set(fd[0])
            right = fd[1]
            for key in self.data[self.idx].candidateKeys:
                key = set(key)
                if (left.issubset(key) and left != key) and right not in self.data[self.idx].primaryAttributes:
                    return True, fd
        return False, None
    
    # function to check for 2NF
    def is2NF(self):
        prev = self.is1NF()
        if not prev[0]:
            return prev
        Pd = self.isPartialDependency()
        if not Pd[0]:
            return True, None
        return False, Pd[1]
    
    # function to check for transitive dependencies
    def isTransitiveDependency(self):
        for fd in self.data[self.idx].functionalDependencies:
            left= set(fd[0])
            right= fd[1]
            for key in self.data[self.idx].candidateKeys:
                key= set(key)
                if not key.issubset(left) and (right not in self.data[self.idx].primaryAttributes):
                    return True, fd
        return False, None
    
    # function to check for 3NF
    def is3NF(self):
        prev = self.is2NF()
        if not prev[0]:
            return prev
        Td = self.isTransitiveDependency()
        if not Td[0]:
            return True, None
        return False, Td[1]
    
    # function to check for BCNF
    def isBCNF(self):
        prev = self.is3NF()
        if not prev[0]:
            return prev
        for fd in self.data[self.idx].functionalDependencies:
            left = set(fd[0])
            for key in self.data[self.idx].candidateKeys:
                key = set(key)
                if not key.issubset(left):
                    return False, fd
        return True, None
    
    # function to decompose the table 
    def decompose(self, problem):
        left = problem[0]
        closure = list(self.data[self.idx].findClosure(left, self.data[self.idx].functionalDependencies))
        # decompose the table into two tables
        # table1 -> closure of left , table2 -> left and other attributes that are not in closure of left
        # print(f"closure : {closure}")
        columns1 = []
        columns2 = [left[0]]
        for attr in self.data[self.idx].attributes:
            if attr not in closure:
                columns2.append(attr)
            else:
                columns1.append(attr)
                
        df1 = pd.DataFrame(self.data[self.idx].table, columns=columns1)
        df2 = pd.DataFrame(self.data[self.idx].table, columns=columns2)
        
        self.data.append(Table("", self.data[self.idx].tableName + "1", df1))
        self.data.append(Table("", self.data[self.idx].tableName + "2", df2))
        self.data.remove(self.data[self.idx])
        
        return
    
    def normalize(self, idx):
        self.idx = idx
        bcnf = self.isBCNF()
        if(bcnf[0]):
            return True
        else:
            self.decompose(bcnf[1])
            return False
            
    def autoNormalize(self):
        while(True):
            flag = True
            for i in range(len(self.data)):
                isNormalized = self.normalize(i)
                flag = flag and isNormalized
            if flag:
                break
        return 
              
            
    

    

        
        
    
        
    
    
    
    
        