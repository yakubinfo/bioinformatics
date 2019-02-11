# Copyright (C) 2015-2019 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

# This file contains a collection of functions to solve the problems
# at rosalind.info.

## Helper functions

import reference_tables as rrt
import functools as ft
import operator as op
import sys
import matplotlib.pyplot as plt
import re

def read_dna(name):
    with open(name,'r') as f:
        return f.read().strip()

def read_strings(test_data,init=1):
    inputs=[]
    with open(test_data) as f:
        state=init
        for line in f:
            content=line.strip()
            if state==0:
                if content=='Input:':
                    state=1
            elif state==1:
                if content=='Output:':
                    state=2
                else:
                    inputs.append(content)
            else:
                expected.append(content)
    return inputs

def print_adjacency_list(adjacency_list,path=r'c:\temp\out.text'):
    with open(path,'w') as out:
        for a,b,c in adjacency_list:
            out.write('{0} {1} {2}\n'.format(a,b,c))

def print_list(list,path=r'c:\temp\out.text'):
    sep=''
    with open(path,'w') as out:
        for el in list:
            out.write('{0} {1}'.format(sep,el))
            sep = ' '
        
def translate(string,trans):
    return ''.join([trans[c] for c in string])

def count_subset(s,subset):
    return [s.count(c) for c in subset]

def match(mm,seq):
    for (key,value) in seq:
        if mm==value:
            return (key, value)
        
def best(seq):
    return match(max([value for (key,value) in seq]),seq)

def k_mers(k):
    if k<=0:
        return ['']
    else:
        result=[]
        for ks in k_mers(k-1):
            for l in ['T','G','C','A']:
                result.append(ks+l)
    return result

def triplets(dna):
    return [dna[i:i+3] for i in range(0,len(dna),3)]   



def print_profile(profile):
    for key,value in profile.items():
        line=key
        sep=': '
        for v in value:
            line=line+sep
            line = line + str(v)
            sep = ' '
        print (line)

# Used to build a table of all the k-mers in a string, with their frequncies
def create_frequency_table(string,k):        
    freqs={}
    for kmer in [string[i:i+k] for i in range(len(string)-k+1)]:
        if kmer in freqs:
            freqs[kmer]+=1
        else:
            freqs[kmer]=1
    return freqs



def get_mass(peptide,mass=rrt.integer_masses):
    return sum([mass[amino_acid] for amino_acid in peptide])

def zeroes(n):
    return [0 for i in range(n)]

def print_peptide(seq):
    for p in seq:
        l=''
        for x in p:
            if len(l)>0:
                l=l+'-'
            l=l+str(x)
        print (l) 
        
def linearSpectrum(peptide):
    def get_pairs():
        return [(i,j) for i in range(len(peptide)) for j in range(len(peptide)+1) if i<j]  
    result=[sum(peptide[i:j]) for (i,j) in get_pairs()] 
    result.append(0)
    result.sort()
    return result 

def cycloSpectrum1(peptide):
    def get_pairs(index_range):
        n=len(index_range)
        return [(i,j) for i in index_range for j in range(i,i+n) if j!=i]
    augmented_peptide=peptide+peptide
    result=[sum(augmented_peptide[a:b]) for (a,b) in get_pairs(range(len(peptide)))]
    result.append(0)
    result.append(sum(peptide)) 
    result.sort()
    return result  

def consistent(peptide,spectrum):
    def count(element,spect):
        return len ([s for s in spect if s==element])
    peptide_spectrum=linearSpectrum(peptide)
    for element in peptide_spectrum:
        if count(element,peptide_spectrum)>count(element,spectrum):
            return False
    return True

def read_list(file_name):
    with open(file_name) as f:
        return [line.strip() for line in f]
    
def print_adjacency_graph(graph):
    for (a,b) in graph:
        print ('%(a)s -> %(b)s'%locals())
        
def format_list(list):
    return ' '.join([str(l) for l in list])

def print_adjacency_graph2(graph):
    for (a,b) in graph:
        succ=''
        for bb in b:
            if len(succ)>0:
                succ=succ+','
            succ=succ+bb
        print ('%(a)s -> %(succ)s'%locals())

def print_adjacency_graph3(graph):
    for (a,b) in graph.items():
        succ=''
        for bb in b:
            if len(succ)>0:
                succ=succ+','
            succ=succ+bb
        print ('%(a)s -> %(succ)s'%locals())

def rotate(cycle,pos):
    return cycle[pos:]+cycle[1:pos]+cycle[pos:pos+1]       

def sign(x):
    if x<0:
        return -1
    if x>0:
        return 1
    return 0

# Calculate binomial coefficients using recurrence relation
#
# Input: n Number of oblects
#
# Return: vector [C(n,0), C(n,1),...C(n,n)]

def binomial_coefficients(n):
    coeffs=[[1,0]]
    for i in range(1,n+1):
        new_coeffs=[1]
        for j in range(i):
            new_coeffs.append(coeffs[-1][j]+coeffs[-1][j+1])
        new_coeffs.append(0)
        coeffs.append(new_coeffs)
    return coeffs[-1][0:-1]

# Multiply elements of a list
#
# Input: a list of numbers
#
# Return: product of numbers

def prod(iterable):
    return ft.reduce(op.mul, iterable, 1)

# Count occurences of a character in a string
#
# Input: a character and a string
#
# Return: Nmber of times character occurs in string

def count_occurences(c,string):
    count=0
    start=0
    while True:
        start=string.find(c,start)
        if start<0:
            return count
        count+=1
        start+=1   

def countMatchesInSpectra(spect1,spect2):
    i1=0
    i2=0
    count=0
    while i1<len(spect1) and i2<len(spect2):
        diff=spect1[i1]-spect2[i2]
        if diff==0:
            count+=1
            i1+=1
            i2+=1
        elif diff<0:
            i1+=1
        else:
            i2+=1
    return count

def print_strings(strings,sorted=False):
    if sorted:
        strings.sort()
    for s in strings:
        print (s)

# Driver for Monte Carlo methods

def mcmc_steps(step,name,N=20):
    best_score_ever=sys.float_info.max
    freqs={}
    plt.figure(1)
    plt.subplot(211)    
    for i in range(50):
        best_score,motifs,scores=step()
        if best_score<best_score_ever:
            best_score_ever= best_score
            best_motifs=[motif for motif in motifs]
        if not best_score in freqs:
            freqs[best_score]=0
        freqs[best_score]+=1
        plt.plot(range(len(scores)), scores)
    plt.xlabel('T')
    plt.ylabel('Score')
    plt.title(name)
    plt.subplot(212)
    xs=sorted(list(freqs.keys()))
    ys=[freqs[x]/N for x in xs]

    plt.plot(xs,ys, 'ro')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.axis([xs[0]-1, xs[-1]+1, min(ys), max(ys)])
    
    plt.savefig('%(name)s.png'%locals())
    return best_motifs

def binomial_index(n,k):
    return n*(n+1)//2+k

def create_binomial(n):
    def binomial(n,k,c):
        if k>0 and k<n:
            ii=binomial_index(n-1,k)
            return c[ii-1]+c[ii]
        return 1        
    c=[]
    for nn in range(n):
        for k in range(nn+1):
            c.append(binomial(nn,k,c))
    return c

    # create transition matrix (Feller, page 380)
    #   p[j][k] = probabilty of a transition from j to k,
    #   where j and k i snumber of recessives    
def create_wf_transition_matrix(n):
    c=create_binomial(2*n+1)
    transition_matrix=[]
    for j in range(2*n+1):
        p_column=[]
        pj=j/(2*n)
        term1=1
        term2=[1.0]
        for k in range(2*n):
            term2.append(term2[-1]*(1-pj))
        kk=-1
        for k in range(2*n+1):
            p_column.append(c[binomial_index(2*n,k)] * term1 *term2[kk])
            term1*=pj
            kk-=1
        transition_matrix.append(p_column) 
    return transition_matrix

def create_wf_initial_probabilites(n,m):
    e=zeroes(2*n+1)
    e[2*n-m]=1
    return e

def iterate_markov(e,p,g,n):
    for i in range(g):
        psum=sum(e)
        e1=[]
        for k in range(2*n+1):
            ee=0
            for j in range(2*n+1):
                ee+=e[j]*p[j][k]
            e1.append(ee)
        for k in range(2*n+1):
            e[k]=e1[k]
    return e

# convert a number i to a list og binary bits of lenghth n

def binary(i,n):
    dividend=i
    bits=[]
    for j in range(n):
        next_dividend=dividend//2
        bits.append(dividend-2*next_dividend)
        dividend=next_dividend
    return bits[::-1]  

# flatten a list of lists into a single list

def flatten(x):
    return [inner for outer in x for inner in outer]     

def print_matrix(B,out='./print_matrix.txt'):
    with open(out,'w') as f:
        for row in B:
            line=""
            for x in row:
                if len(line)>0:
                    line=line+' '
                line=line+"{:15.12f}".format(x)
            f.write(line+'\n')

#Tree --> Subtree ";" | Branch ";"
#Subtree --> Leaf | Internal
#Leaf --> Name
#Internal --> "(" BranchSet ")" Name
#BranchSet --> Branch | Branch "," BranchSet
#Branch --> Subtree Length
#Name --> empty | string
#Length --> empty | ":" number
class Newick(object):
    @staticmethod
    def find_commas(string):
        commas=[]
        bracket_level=0
        for i in range(len(string)):
            if string[i]==',' and bracket_level==0:
                commas.append(i)
            if string[i]=='(':
                bracket_level+=1
            if string[i]==')':
                bracket_level-=1                            
        return commas
    
    @staticmethod
    def find_balanced_brackets(string):
        bracket_level=0
        for i in range(len(string)):
            if string[i]=='(':
                bracket_level+=1
            if string[i]==')':
                bracket_level-=1 
                if bracket_level==0:
                    return i
                
class Tree(Newick):
    def __init__(self,subtree):
        self.subtree=subtree
    def __str__(self):
        return '{};'.format(str(self.subtree))
    @staticmethod
    def parse(string):
        print (string)
        s=string.replace(' ','')
        branch=Branch.parse(s[0:-1])
        if branch and s[-1]==';':
            return Tree(branch)
        subtree=SubTree.parse(s[0:-1])
        if subtree and s[-1]==';':
            return Tree(subtree)          
        
class SubTree(Newick):
    def __init__(self,subtreeOrInternal):
        self.subtreeOrInternal=subtreeOrInternal
    def __str__(self):
        return str(self.subtreeOrInternal) 
    @staticmethod
    def parse(string):
        internal=Internal.parse(string)
        if internal:
            return SubTree(internal)
        leaf=Leaf.parse(string)
        if leaf:
            return SubTree(leaf)  
        
class Internal(Newick):
    def __init__(self,branchSet,name):
        self.branchSet=branchSet
        self.name=name
    def __str__(self):
        return '{}{}'.format(str(self.branchSet), str(self.name))
    @staticmethod
    def parse(string):
        if len(string)>1 and string[0]=='(':
            rh=Newick.find_balanced_brackets(string)
            internal_string=string[1:rh]
            remainder=string[rh+1:].strip()
            branch_set=BranchSet.parse(internal_string)
            if branch_set:
                name=Name.parse(remainder)
                return Internal(branch_set,name)  
            
class BranchSet(Newick):
    def __init__(self,branches):
        self.branches=[b for b in branches]
    def __str__(self):
        return '({})'.format(','.join([str(b) for b in self.branches]))
    @staticmethod
    def parse(string):
        commas=Newick.find_commas(string)
        if len(commas)==0:
            return BranchSet([Branch.parse(string)])
        start=0
        branch_set=[]
        for pos in commas:
            branch=Branch.parse(string[start:pos])
            if branch:
                branch_set.append(branch)
            else:
                return None
            start=pos+1
        branch=Branch.parse(string[start:])
        if branch:
            branch_set.append(branch)
            return BranchSet(branch_set)        

class Branch(Newick):
    def __init__(self,subtree,length=None):
        self.subtree=subtree
        self.length=length
    def __str__(self):
        return str(self.subtree)                         \
               if self.length==None or self.length.number==None else  \
               '{}:{}'.format(self.subtree, self.length)
    @staticmethod
    def parse(string):
        parts=string.split(':')
        if len(parts)>1:
            return Branch(SubTree.parse(':'.join(parts[0:-1])),Length(parts[-1]))
        return Branch(SubTree.parse(string))  
        
class Leaf(Newick):
    def __init__(self,name):
        self.name=name
    def __str__(self):
        return str(self.name)
    @staticmethod
    def parse(string):
        return Leaf(Name.parse(string))
    
class Name(object):
    def __init__(self,name=None):
        self.name=name
    def __str__(self):
        return '' if self.name==None else '{}'.format(str(self.name))
    @staticmethod
    def parse(string):
        if len(string)==0:
            return Name()        
        matches=re.match('[A-Za-z_]*',string)
        if matches:
            return Name(matches.group(0))
        
class Length(object):
    def __init__(self,number=None):
        self.number=number    
    def parse(string):
        return None if number==None else float(number)        
    def __str__(self):    
        return '' if self.number==None else str(self.number)
if __name__=='__main__':
    print (k_mers(4))
    print(binomial_coefficients(8)) 
    print (prod([2,3,4,5,6]))
    print (Tree.parse('(a,b);'))
    print (Tree.parse('((a,b),(c,d));'))
    print (Tree.parse('((a,),(c,d));'))
    print (Tree.parse('(dog,cat);'))
    print (Tree.parse('(cat)dog;'))
    print (Tree.parse('(dog:20, (elephant:30, horse:60):20):50;'))
