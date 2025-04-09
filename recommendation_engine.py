import pandas as pd
from apyori import apriori

def load_data(path="Grocery.csv"):
    return pd.read_csv(path)

def preprocess_data(df):
    return df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list)

def generate_rules(transactions, min_support=0.01, min_confidence=0.2, min_lift=2):
    rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift)
    results = list(rules)
    recommendations = []
    for result in results:
        for stat in result.ordered_statistics:
            if stat.items_base and stat.items_add:
                recommendations.append({
                    'Base Item': ', '.join(stat.items_base),
                    'Recommended Item': ', '.join(stat.items_add),
                    'Confidence': stat.confidence,
                    'Lift': stat.lift
                })
    return pd.DataFrame(recommendations)

def get_recommendations(item_name, rules_df):
    return rules_df[rules_df['Base Item'].str.contains(item_name, case=False)]

def recommend_items(items, rules_df):
    recommendations = pd.DataFrame()
    for item in items:
        recs = get_recommendations(item, rules_df)
        recommendations = pd.concat([recommendations, recs])
    return recommendations.drop_duplicates(subset=['Recommended Item'])[['Recommended Item', 'Confidence', 'Lift']]
