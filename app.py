import streamlit as st
from recommendation_engine import recommend_items, load_data, preprocess_data, generate_rules

st.set_page_config(page_title="Grocery Recommendation", page_icon="🛒")
st.title("🛒 Grocery Recommendation System")
st.markdown("Enter grocery items you plan to buy, and get smart suggestions!")

df = load_data()
basket = preprocess_data(df)
rules_df = generate_rules(basket.tolist())

user_input = st.text_input("Enter items (comma-separated):", placeholder="e.g. milk, bread, eggs")

if st.button("Recommend"):
    if user_input:
        items = [item.strip() for item in user_input.split(",")]
        try:
            recommendations = recommend_items(items, rules_df)
            if not recommendations.empty:
                st.success("We recommend you also consider:")
                for item in recommendations['Recommended Item']:
                    st.write("•", item)
            else:
                st.warning("No recommendations found. Try other items.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some items to get recommendations.")
