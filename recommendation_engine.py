import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from apyori import apriori

# Load your data
def load_data(path="Grocery.csv"):
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
# Load data and rules once to reuse
df = load_data()
basket = preprocess_data(df)
rules_df = generate_rules(basket.tolist())

# Function to get recommendations for multiple items
def recommend_items(user_input):
    items = [item.strip().lower() for item in user_input.split(',')]
    recommendations = pd.DataFrame()
    for item in items:
        recs = get_recommendations(item, rules_df)
        recommendations = pd.concat([recommendations, recs])
    # Drop duplicates if multiple items recommend the same thing
    recommendations = recommendations.drop_duplicates(subset=['Recommended Item'])
    return recommendations[['Recommended Item', 'Confidence', 'Lift']]
