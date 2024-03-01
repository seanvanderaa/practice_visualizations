def calculate_match_perc(user1, user2):
    print("Hello")

def jaccard_similarity(user1_data, user2_data, data_key):
    user1_set = set(user1_data.get(data_key, []))
    user2_set = set(user2_data.get(data_key, []))

    intersection = user1_set.intersection(user2_set)
    union = user1_set.union(user2_set)

    if not union:
        return 0  # Avoid division by zero; implies both sets are empty

    similarity = len(intersection) / len(union)
    return similarity


