# class to represent a table in the RDBMS
import pandas as pd
import numpy as np


class Table:
    def __init__(self, csvFilePath, tableName):
        self.tableName = tableName
        self.table = pd.read_csv(csvFilePath)
        self.attributes = list(self.table.columns)
        self.numOfAttributes = len(self.attributes)
        self.functionalDependencies = None
        self.candidateKeys = None
        self.primaryAttributes = None
        self.nonPrimaryAttributes = None
        self.primaryKeys = None

    def __str__(self):
        print(self.table)
        return (f"\nTable:\n {self.tableName} : {self.attributes}\n Functional Dependencies: {self.functionalDependencies}\n Candidate Keys: {self.candidateKeys}\n Primary Attributes: {self.primaryAttributes}\n Non Primary Attributes: {self.nonPrimaryAttributes}\n Primary Keys: {self.primaryKeys}")

    def isDependency(self, lhs, rhs):
        setX = set()
        for i in range(self.table.shape[0]):
            tupList = []
            for j in lhs:
                tupList.append(self.table[j][i])
            setX.add(tuple(tupList))
        length = len(setX)
        listX = list(setX)
        listY = [set() for i in range(length)]
        for i in range(self.table.shape[0]):
            tupList = []
            for j in lhs:
                tupList.append(self.table[j][i])
            id = listX.index(tuple(tupList))
            listY[id].add(self.table[rhs][i])
            if (len(listY[id]) > 1):
                return False
        return True

    # function to find all functional dependencies of the table
    def findAllDependencies(self):
        functionalDependencies = []
        funDepSet = set()
        for i in range(self.numOfAttributes):
            for j in range(i, self.numOfAttributes):
                if (i != j):
                    lhs = [self.attributes[i]]
                    rhs = self.attributes[j]
                    if(self.isDependency(lhs, rhs)):
                        # print(f"{self.attributes[i]} --> {self.attributes[j]} -True")
                        functionalDependencies.append([lhs, [rhs]])
                        funDepSet.add((self.attributes[i], self.attributes[j]))
        for i in range(self.numOfAttributes):
            for j in range(i, self.numOfAttributes):
                for k in range(j, self.numOfAttributes):
                    if ((i != j) and (i != k) and (j != k)):
                        lhs = [self.attributes[i], self.attributes[j]]
                        rhs = self.attributes[k]
                        if(self.isDependency(lhs, rhs)):
                            # print(f"{self.attributes[i],self.attributes[j]} --> {self.attributes[k]} -True")
                            temp = set()
                            temp.add((self.attributes[i], self.attributes[j]))
                            temp.add((self.attributes[i], self.attributes[k]))
                            temp.add((self.attributes[j], self.attributes[k]))
                            if(temp.isdisjoint(funDepSet)):
                                functionalDependencies.append([lhs, [rhs]])
        return functionalDependencies

    # function to find closure of a set of attributes
    def findClosure(self, attribute, functionalDependencies):
        attributeClosure = set(attribute)
        while(True):
            prev = attributeClosure
            for dependency in functionalDependencies:  # list<list>>
                left = set(dependency[0])  # set of attribute
                right = set(dependency[1])  # set of attribute
                if(left.issubset(attributeClosure)):
                    attributeClosure = attributeClosure.union(right)
            if(prev == attributeClosure):
                break
        return attributeClosure

    # function to find candidate keys in a table given its functional dependencies
    def findCandidateKeys(self):
        self.functionalDependencies = self.findAllDependencies()
        candidateKeys = []
        for attr in self.attributes:
            val = [attr]
            closure = self.findClosure(val, self.functionalDependencies)
            if (len(closure) == self.numOfAttributes) and (val not in candidateKeys):
                candidateKeys.append(val)

        if len(candidateKeys) > 0:
            return candidateKeys

        for i in range(0, self.numOfAttributes-1):
            for j in range(i+1, self.numOfAttributes):
                val = [self.attributes[i], self.attributes[j]]
                closure = self.findClosure(val, self.functionalDependencies)
                if len(closure) == self.numOfAttributes:
                    if val not in candidateKeys:
                        candidateKeys.append(val)

        if len(candidateKeys) > 0:
            return candidateKeys

        for i in range(0, self.numOfAttributes-2):
            for j in range(i+1, self.numOfAttributes-1):
                for k in range(j+1, self.numOfAttributes):
                    val - [self.attributes[i],
                           self.attributes[j], self.attributes[k]]
                    closure = self.findClosure(val, self.functionalDependencies)
                    if len(closure) == self.numOfAttributes:
                        if val not in candidateKeys:
                            candidateKeys.append(val)

        if len(candidateKeys) > 0:
            return candidateKeys

        return None
    
    # function to set attributes as prime and non prime
    def setAttributes(self):
        self.candidateKeys = self.findCandidateKeys()
        primaryAttributes= set()
        minLen = 100000
        for key in self.candidateKeys:
            if len(key) < minLen:
                self.primaryKeys = key
                minLen = len(key)
            
            for attr in key:
                primaryAttributes.add(attr)

        self.primaryAttributes = list(primaryAttributes)
        self.nonPrimaryAttributes = [
            x for x in self.attributes if x not in self.primaryAttributes]

        return

