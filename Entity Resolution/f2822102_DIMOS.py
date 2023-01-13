
############### Usefull libraries ###########################

import pandas as pd 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import warnings
warnings.filterwarnings("ignore")
import pprint
import time
from itertools import islice
from itertools import combinations 
from collections import Counter
from itertools import chain
import ast
import pprint 
import nltk
from nltk.corpus import stopwords
from itertools import chain
stop = stopwords.words('english')

################# Import of the data #########################
data = pd.read_csv("ER-Data.csv",sep=';',dtype={
                     'authors': str,
                     'venue': str,
                     'year':str,
                     'title' : str})
data.index=data.index+1

###### Data Cleaning #######################################

data=data.fillna('nan')

############### Making all the strings lower case #####################################

data['title']=data['title'].str.lower()
data['authors']=data['authors'].str.lower()
data['venue']=data['venue'].str.lower()

####################### Removing the Stopwords ###################################
data['authors'] = data['authors'].apply(lambda x: ' '.join([item for item in x.split() if item not in stop]))
data['venue'] = data['venue'].apply(lambda x: ' '.join([item for item in x.split() if item not in stop]))
data['title'] = data['title'].apply(lambda x: ' '.join([item for item in x.split() if item not in stop]))

################## Removing the punctuation ################################
data["authors"] = data['authors'].str.replace('[^\w\s]','')
data["venue"] = data['venue'].str.replace('[^\w\s]','')
data["title"] = data['title'].str.replace('[^\w\s]','')
data["year"] = data['year'].str.replace('[^\w\s]','')

############## Making our data a dictionary with the ID as index #####################
data_dict=data.set_index('id').T.to_dict('list')

############# The command below splits row by row the words of the dictionary in space ##########

res = {k: list(chain.from_iterable([st.split() for st in v])) for k,v in data_dict.items()}

####################### Removing the nan value ##############################

for v in res.values():
    if 'nan' in v:
        v.remove('nan')


########################################################## TASK A ############################################################################
print("----------------------------------------------------------------------------------------------------------------------------")
print("ENTERING IN TASK A")
print('\n')

####################### Impementing the Token Blocking ######################
# In this procedure below we created 2 dictionaries in order to store our key value pairs. 

blocks = dict() # Contains the blocks with the Key-Value pairs
unique_tokens = dict() # Contains the unique words of the entire csv file 
for i,j in zip(res.keys(),res.values()):
    for token in j:
        if token in unique_tokens:
            blocks[token].append(i)
        else :
            blocks[token] = [i]
            unique_tokens[token] = [token]

# Removing the blocks with size < 2 

for key, value in dict(blocks).items():
        if len(value) < 2 :
               del blocks[key]

print("Printing the outcome of the Step A....\n")
print('\n')
first_5_pairs = {k: blocks[k] for k in list(blocks)[:5]}
pprint.pprint(first_5_pairs,compact=True,sort_dicts=False)
print('\n')


########################################################## TASK B ############################################################################
print("----------------------------------------------------------------------------------------------------------------------------")
print("ENTERING IN TASK B")
print('\n')



## Compute all the possible comparisons that shall be made to resolve the duplicates within the blocks that were created in Step A.
#  After the computation, please print the final calculated number of comparisons.

# In the step B we created a procedure that is running through the blocks and computes the comparisons using the formula n(n-1)/2.
# Where n is the length of each block.
# Finally, in every iteration we store the outcome in the "comparisons" variable summing the outcome with the previous ones. 
# At the end of the procudure we have the final number of comparison we need to make to resolve the duplicates.

comparisons = 0
for i,j in  blocks.items():
    comparisons=comparisons+(len(j)*(len(j)-1))/2

print("Printing the outcome of the Step B....\n")
print("We need","{:,}".format(int(comparisons)),"comparisons to resolve the duplicates.\n")
print('\n')


########################################################## TASK C ############################################################################
print("----------------------------------------------------------------------------------------------------------------------------")
print("ENTERING IN TASK C")
print('\n')


# Create a Meta-Blocking graph of the block collection (created in step A) and 
# using the CBS Weighting Scheme (i.e., Number of common blocks that entities in a specific comparison have in common) 
# i) prune (delete) the edges that have weight < 2 
# ii) re-calculate the final number of comparisons (like in step B) of the new block collection that will be created after the edge pruning.

# Slicing the blocks because of the large outcome of different comparisons.
# With the function below we decide how many values we want to include in the Meta Blocking Procudure.


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
n = 10 # Determines how many of the blocks will be used in order to create our Meta Blocking Graph.
#All_blocks = 38351
blocks_n = take(n,blocks.items()) 
blocks_n=dict(blocks_n)

# Making the blocks dataframe in order to isolate the column with the IDs.
dataframe_blocks=pd.DataFrame(blocks_n.items(),columns=['Token', 'ID'])
dataframe_blocks = dataframe_blocks['ID'].tolist()

# Line by line we combute every ID combination the number of its appearance.
# The number of the appearance will be the weight of every edge which unites every pair of nodes.
def edge_pairs(lines):
    pair_counter = Counter()
    
    for line in lines:
        unique_tokens = sorted(set(line)) #exclude duplicates in same line and sort to ensure one word is always before othe
        combos = combinations(unique_tokens, 2)
        pair_counter += Counter(combos)
    return pair_counter

#t0 = time.time()
graph = edge_pairs(dataframe_blocks)
graph=graph.most_common()
#t1 = time.time()

#print("the run time for the edge creation is :" , t1-t0) # if you want to measure the time of the pair creation uncomment the 't0' and 't1' in lines 158 and 161.
print("\n ")
#print("The size of the whole graph is : " ,len(graph))
#print("\n")


# C1 Pruning the edges with weight < 2 

pruned_graph = {edges:weight for edges,weight in dict(graph).items() if weight >= 2}

# Print the first 5 ( from the pruned graph ) edges with the weights.

first_5_edges_C = {k: pruned_graph[k] for k in list(pruned_graph)[:5]}
print('# C1 TASK')
print('\n')
print("Printing the first 5 edges with weight >= 2.... : \n")
print(first_5_edges_C)
print('\n')
#print("Our pruned graph consists of :",len(pruned_graph),"edges")
#print('\n')

# C2 Comparisons

comparisons_C2 = 0
for i,j in pruned_graph.items():
    comparisons_C2=comparisons_C2+((j)*((j)-1))/2
print('# C2 TASK')
print('\n')
print("Printing the comparisons for the Step C2 to resolve the duplicates....\n")
print("We need","{:,}".format(int(comparisons_C2)),"comparisons.")
print('\n')


########################################################## TASK D ############################################################################
print("----------------------------------------------------------------------------------------------------------------------------")
print("ENTERING IN TASK D")
print('\n')

## Create a function that takes as input two entities and computes their Jaccard similarity based on the attribute title. 
## You are not requested to perform any actual comparisons using this function.

def Jaccard(entity1, entity2):
    str1=data.loc[data['id'] == entity1, 'title'].item()
    str2=data.loc[data['id'] == entity2, 'title'].item()
    set1 = set(str1.split())
    set2 = set(str2.split())
    print("\n")
    print("The first title is : ",str1)
    print("The second title is : ",str2)

    return float(len(set1 & set2)) / len(set1 | set2)

# Give the ID of the entity
entity1 = int(input("Give the first entity's ID (from 1 to 66879) : "))
entity2 = int(input("Give the second entitys's ID (from 1 to 66879) :"))

print("\nThe similarity of the entities based on the attribute TITLE is : ", Jaccard(entity1,entity2))