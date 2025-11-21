import json
import os

main_file = '/Users/zvwgvx/Antigravity/polythink-instruct-dataset/dataset/multi-turn/sensitive_topics.json'
batch_files = [
    'sensitive_topics_fix_batch_1.json',
    'sensitive_topics_fix_batch_2.json',
    'sensitive_topics_fix_batch_3.json'
]

# Read main file
with open(main_file, 'r') as f:
    main_data = json.load(f)

# Filter out old samples (550-800)
# Note: IDs are strings "st_mt_XXX"
# We need to parse the number to filter correctly
kept_data = []
for item in main_data:
    try:
        item_id_num = int(item['id'].replace('st_mt_', ''))
        if item_id_num < 550 or item_id_num > 800:
            kept_data.append(item)
    except ValueError:
        # Keep items with non-standard IDs if any (shouldn't be)
        kept_data.append(item)

print(f"Kept {len(kept_data)} samples from original file.")

# Read and append new batches
new_samples = []
for b_file in batch_files:
    if os.path.exists(b_file):
        with open(b_file, 'r') as f:
            batch_data = json.load(f)
            new_samples.extend(batch_data)
            print(f"Loaded {len(batch_data)} samples from {b_file}")

# Combine and sort
final_data = kept_data + new_samples
# Sort by ID number
final_data.sort(key=lambda x: int(x['id'].replace('st_mt_', '')))

# Write back
with open(main_file, 'w') as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)

print(f"Total samples after merge: {len(final_data)}")
