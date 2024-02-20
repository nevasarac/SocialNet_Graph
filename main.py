import json
import networkx as nx
from collections import Counter
import re

class User:
    def __init__(self, username, name, followers_count, following_count, language, region, tweets, followers, following):
        self.username = username
        self.name = name
        self.followers_count = followers_count
        self.following_count = following_count
        self.language = language
        self.region = region
        self.tweets = tweets
        self.followers = followers
        self.following = following
        self.interests = self.extract_interests(tweets)

    def extract_interests(self, tweets):
        stop_words = ["ama", "ve", "bir", "da","bu","çok","de","büyük","yer","ile","olarak","tarafından","ben","sen","daha","i"]
        words = re.findall(r'\b\w+\b', ' '.join(tweets).lower())
        words = [word for word in words if word not in stop_words]
        word_counts = Counter(words)
        most_common_word, _ = word_counts.most_common(1)[0] if word_counts else ('', 0)
        return most_common_word


class CustomHashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    def add_item(self, key, value):
        hash_value = self._custom_hash_function(key)
        if self.table[hash_value] is None:
            self.table[hash_value] = []
        self.table[hash_value].append((key, value))

    def get_item(self, key):
        hash_value = self._custom_hash_function(key)
        items = self.table[hash_value]
        if items is not None:
            for k, v in items:
                if k == key:
                    return v
        return None

    def _custom_hash_function(self, key):

        hash_value = 1
        for char in key:
            hash_value *= ord(char)
        return hash_value % self.size

    def add_relationship(self, follower, following):
        follower_user = self.get_item(follower)
        following_user = self.get_item(following)

        if follower_user and following_user:
            follower_user.following.append(following_user.username)
            following_user.followers.append(follower_user.username)

    def search_users_by_interest(self, interest):
        users_with_interest = []
        for user_list in self.table:
            if user_list is not None:
                for key, user in user_list:
                    if interest in user.interests:
                        users_with_interest.append(user.username)
        return users_with_interest

    def calculate_all_interests(self):
        for user_list in self.table:
            if user_list is not None:
                for key, user in user_list:
                    user.interests = user.extract_interests(user.tweets)


def create_user_objects_from_json(json_data, hash_table):
    for user_data in json_data:
        username = user_data['username']
        user = User(**user_data)
        hash_table.add_item(username, user)

if __name__ == '__main__':
    with open("D:/PythonProject/proje_3/data1.json", "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    user_objects = CustomHashTable()
    create_user_objects_from_json(json_data, user_objects)

    desired_username1 = "ymohr"
    desired_username2 = "schimmel.ronaldo"
    desired_username3 = "monserrat82"

    desired_user1 = user_objects.get_item(desired_username1)
    desired_user2 = user_objects.get_item(desired_username2)

    user_objects.add_relationship(desired_username1, desired_username2)
    user_objects.add_relationship(desired_username2, desired_username3)

    G = nx.Graph()
    for user_list in user_objects.table:
        if user_list is not None:
            for key, user in user_list:
                G.add_node(key)
                for follower in user.followers:
                    G.add_edge(follower, key)

    edge_list_file_path = "graph_edgelist.txt"
    nx.write_edgelist(G, edge_list_file_path)

    print(f"Graph edge list has been written to: {edge_list_file_path}")

    print(f"Most common word in {desired_user1.username}'s tweets: {desired_user1.interests}")
    print(f"Most common word in {desired_user2.username}'s tweets: {desired_user2.interests}")

    user_objects.calculate_all_interests()

    searched_interest = "büyük"

    matching_users = user_objects.search_users_by_interest(searched_interest)
    if matching_users:
        print(f"Kullanıcılar ilgi alanını '{searched_interest}' paylaşıyor: {matching_users}")
    else:
        print(f"İlgilenilen kelimeye sahip kullanıcı bulunamadı.")

    #if desired_user1:
    #    print(f"Kullanıcı Adı: {desired_user1.username}")
    #    print(f"Adı: {desired_user1.name}")
    #    print(f"Takip Ettiği Kişi Sayısı: {desired_user1.following_count}")
    #    print(f"Takipçi Sayısı: {desired_user1.followers_count}")
    #    print(f"Language: {desired_user1.language}")
    #    print(f"Region: {desired_user1.region}")
    #    print(f"Tweets: {desired_user1.tweets}")
    #    print(f"Following: {desired_user1.following}")
    #    print(f"Followers: {desired_user1.followers}")
    #else:
    #    print(f"{desired_username1} adlı kullanıcı bulunamadı.")


