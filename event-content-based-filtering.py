import pandas as pd
import json

def parse_categories(json_string):
  try:
    return json.loads(json_string)
  except json.JSONDecodeError:
    return []

# Load and preprocess the dataset
data = pd.read_csv('events.csv')
data['categories'] = data['categories'].apply(parse_categories)

# User preferences (selected category IDs)
selected_category_ids = [1, 2]  # Replace with the actual category IDs

def recommend_events_by_category(user_category_ids, data):
    # Filter events based on user-selected category IDs
    filtered_data = data[data['categories'].apply(lambda x: any(cat_id in x for cat_id in user_category_ids))]

    # Check if there are no events found for the specified categories
    if filtered_data.empty:
        print("No events found for the specified categories.")
        return []

    # Get the top 5 recommended events
    top_events = filtered_data.to_dict(orient='records')

    return top_events

# Test the recommendation system
recommendations = recommend_events_by_category(selected_category_ids, data)

# Display the recommendations
print(f'{len(recommendations)} recommendations')
print(f"Recommendations for User's Selected Category IDs {selected_category_ids}:")
for event in recommendations:
    print(f"Event ID: {event['id']}, Title: {event['title']}")
