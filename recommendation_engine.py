import pandas as pd
from apyori import apriori

def load_data(path="Grocery.csv"):
    df = pd.read_csv(path, header=None)
    return df

def preprocess_data(df, group_size=5):
    items = df[0].tolist()
    transactions = [items[i:i+group_size] for i in range(0, len(items), group_size)]
    return transactions

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

def get_recommendations(item_name, rules_df):
    return rules_df[rules_df['Base Item'].str.contains(item_name, case=False)]

def recommend_items(user_input):
    df = load_data()
    transactions = preprocess_data(df)
    rules_df = generate_rules(transactions)
    items = [item.strip().lower() for item in user_input.split(',')]
    recommendations = pd.DataFrame()
    for item in items:
        recs = get_recommendations(item, rules_df)
        recommendations = pd.concat([recommendations, recs])
    recommendations = recommendations.drop_duplicates(subset=['Recommended Item'])
    return recommendations[['Recommended Item', 'Confidence', 'Lift']]
