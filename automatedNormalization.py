from table import Table
import pandas as pd
import numpy as np

class AutoNormalization:
    def __init__(self, csvPath, tableName):
        self.data= Table(csvPath, tableName)
        self.tables= []
        
    # function to check for 1NF
    def is1NF(self):
        for i in range(self.data.numOfAttributes):
            for j in range(self.data.table.shape[0]):
                if (isinstance(self.data.table[self.data.attributes[i]][j], list)):
                    return False, [self.data.attributes[i], self.data.table[self.data.attributes[i]][j]]
        return True, None
    
    # function to check for partial dependencies
    def isPartialDependency(self):
        for fd in self.data.functionalDependencies:
            left = set(fd[0])
            right = fd[1]
            for key in self.data.candidateKeys:
                key = set(key)
                if (left.issubset(key) and left != key) and right not in self.data.primaryAttributes:
                    return True, [left, right]
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
        for fd in self.data.functionalDependencies:
            left= set(fd[0])
            right= fd[1]
            for key in self.data.candidateKeys:
                key= set(key)
                if not key.issubset(left) and (right not in self.data.primaryAttributes):
                    return True, [left, right]
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
        for fd in self.data.functionalDependencies:
            left = set(fd[0])
            for key in self.data.candidateKeys:
                key = set(key)
                if not key.issubset(left):
                    return False, [left, fd[1]]
        return True, None
    
    # function to decompose the table 
    def decompose(self, problem):
        left = problem[0]
        closure = self.data.findClosure(left, self.data.functionalDependencies)
        # decompose the table into two tables
        # table1 -> closure of left , table2 -> left and other attributes that are not in closure of left
        columns1 = []
        columns2 = [left]
        for attr in self.data.attributes:
            if attr not in closure:
                columns2.append(attr)
            else:
                columns1.append(attr)
                
        df1 = pd.DataFrame(self.data.table, columns=columns1)
        df2 = pd.DataFrame(self.data.table, columns=columns2)
        
        self.tables.append(Table("", self.data.tableName + "1", df1))
        self.tables.append(Table("", self.data.tableName + "2", df2))
        return
    
    def normalize(self):
        bcnf = self.isBCNF()
        if(bcnf[0]):
            return True
        else:
            self.decompose(bcnf[1])
                
            
    

    

        
        
    
        
    
    
    
    
        