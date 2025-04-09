import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from apyori import apriori

# Load your data
def load_data(path='Groceries_dataset.csv'):
    df = pd.read_csv(path)
    return df

# Preprocess the data
def preprocess_data(df):
    basket = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list)
    return basket

# Generate association rules
def generate_rules(transactions, min_support=0.01, min_confidence=0.2, min_lift=2):
    rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift)
    results = list(rules)
    recommendations = []
    for result in results:
        for ordered_stat in result.ordered_statistics:
            if len(ordered_stat.items_base) > 0 and len(ordered_stat.items_add) > 0:
                recommendations.append({
                    'Base Item': ', '.join(ordered_stat.items_base),
                    'Recommended Item': ', '.join(ordered_stat.items_add),
                    'Confidence': ordered_stat.confidence,
                    'Lift': ordered_stat.lift
                })
    return pd.DataFrame(recommendations)

# Get recommendations for a specific item
def get_recommendations(item_name, rules_df):
    return rules_df[rules_df['Base Item'].str.contains(item_name, case=False)]

# Optional: visualize frequently bought items
def plot_top_items(df, top_n=10):
    item_counts = df['itemDescription'].value_counts().head(top_n)
    sns.barplot(x=item_counts.values, y=item_counts.index)
    plt.title("Top {} Purchased Items".format(top_n))
    plt.xlabel("Count")
    plt.ylabel("Items")
    plt.tight_layout()
    plt.show()
