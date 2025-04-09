#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd 


# In[5]:


df = pd.read_csv("Grocery.csv", header=None)



# In[6]:


df.head(2)


# In[12]:


data_list=df.values.tolist()


# In[16]:


#data preprocessing
cleaned_data = [[item for item in row if not pd.isna(item)] for row in data_list]


# In[18]:





# In[19]:


from apyori import apriori
rules = apriori(cleaned_data,min_support= 0.03,min_confidence=0.35,min_lift=3,min_length=2)


# In[20]:


list(rules)


# In[22]:


import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# Create an empty co-occurrence matrix
items = set(item for transaction in cleaned_data for item in transaction)
item_list = list(items)
matrix = pd.DataFrame(np.zeros((len(items), len(items))), index=item_list, columns=item_list)

# Fill co-occurrence matrix
for transaction in cleaned_data:
    for item1 in transaction:
        for item2 in transaction:
            if item1 != item2:
                matrix.loc[item1, item2] += 1

# Create heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(matrix, annot=True, cmap='Blues', fmt=".0f")
plt.title("Item Co-Occurrence Heatmap")
plt.show()


# In[ ]:





# In[24]:


get_ipython().system('pip install networkx')


# In[25]:


import networkx as nx
import matplotlib.pyplot as plt
from apyori import apriori

# Generate association rules again
rules = apriori(cleaned_data, min_support=0.03, min_confidence=0.35, min_lift=3, min_length=2)
rules_list = list(rules)

# Create a Directed Graph
G = nx.DiGraph()

# Add nodes and edges
for rule in rules_list:
    for base in rule.ordered_statistics:
        for item in base.items_base:
            for add in base.items_add:
                G.add_edge(item, add, weight=base.lift)

# Draw the network graph
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, k=0.5)  # Layout for better spacing
edges = G.edges(data=True)

# Draw nodes and edges
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in edges}, font_size=8)

plt.title("Association Rule Network")
plt.show()


# In[ ]:





# === Grocery Recommendation Function ===

def recommend_items(user_items):
    user_items = set([item.strip().lower() for item in user_items])
    recommended = set()

    for rule in rules_list:
        for stat in rule.ordered_statistics:
            base_items = set(stat.items_base)
            add_items = set(stat.items_add)

            # If all base items are in user_items, suggest the added items
            if base_items and base_items.issubset(user_items):
                recommended.update(add_items)

    # Remove already present items
    final_recommendations = list(recommended - user_items)
    return final_recommendations
