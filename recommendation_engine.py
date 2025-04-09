import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from apyori import apriori

# Load data
def load_data(path="Grocery.csv"):
    return pd.read_csv(path, header=None)

# Preprocess data into transactions
def preprocess_data(df):
    transactions = []
    for i in range(len(df)):
        transaction = df.iloc[i].dropna().tolist()
        transactions.append(transaction)
    return transactions

# Generate association rules
def generate_rules(transactions, min_support=0.01, min_confidence=0.2, min_lift=2):
    rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift)
    results = list(rules)
    recommendations = []
    for result in results:
        for ordered_stat in result.ordered_statistics:
            if ordered_stat.items_base and ordered_stat.items_add:
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

# Recommend for multiple items
def recommend_items(user_input, rules_df):
    items = [item.strip().lower() for item in user_input.split(',')]
    recommendations = pd.DataFrame()
    for item in items:
        recs = get_recommendations(item, rules_df)
        recommendations = pd.concat([recommendations, recs])
    return recommendations.drop_duplicates(subset=['Recommended Item'])[['Recommended Item', 'Confidence', 'Lift']]

# Example usage
df = load_data()
transactions = preprocess_data(df)
rules_df = generate_rules(transactions)

# Uncomment below to test:
# print(recommend_items("bread, tea", rules_df))
