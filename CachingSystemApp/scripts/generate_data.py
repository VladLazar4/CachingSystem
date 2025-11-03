import csv
import json
import random

f_name_list =  [
    "Andrei", "Mihai", "Ion", "Maria", "Elena", "Gabriel", "Ioana", "Alexandru", "Ana", "Cristian",
    "Radu", "Daniel", "Florin", "Georgiana", "Alina", "Simona", "Laura", "Vlad", "Catalin", "Marius",
    "Sorina", "Oana", "Bogdan", "Claudiu", "Adrian", "Iulia", "Stefan", "Denisa", "Mariana", "Paul",
    "Petru", "Alina", "Diana", "Andreea", "Silviu", "Teodora", "Alex", "Eliza", "Violeta", "Ciprian",
    "Valentin", "Ramona", "Lorena", "Emil", "Ioan", "Raluca", "Nicolae", "Anca", "Marinela", "Sergiu"
]

l_name_list = [
    "Popescu", "Ionescu", "Georgescu", "Dumitrescu", "Stan", "Marin", "Tudor", "Iliescu", "Florea", "Radu",
    "Munteanu", "Niculae", "Petrescu", "Matei", "Constantinescu", "Anghel", "Voicu", "Grigorescu", "Enache", "Preda",
    "Barbu", "Sava", "Vasilescu", "Sandu", "Roman", "Dinu", "Panait", "Badea", "Ciobanu", "Chirita",
    "Cojocaru", "Niculescu", "Alexandrescu", "Croitoru", "Oprea", "Stanciu", "Filip", "Coman", "Petcu", "Rusu",
    "Vlad", "Simion", "Paraschiv", "Lungu", "Voinea", "Iancu", "Dobre", "Popa", "Mihai", "Ene"
]

lat_min, lat_max = 43.6, 48.7
long_min, long_max = 20.3, 29.7

def generate_users(n=100):
    users = []
    for i in range(n):
        f_name = random.choice(f_name_list)
        l_name = random.choice(l_name_list)
        lat = round(random.uniform(lat_min, lat_max), 6)
        long = round(random.uniform(long_min, long_max), 6)
        users.append(
            {
                "id": i,
                "f_name": f_name,
                "l_name": l_name,
                "lat": lat,
                "long": long,
                "friends": []
            }
        )
    generate_friendships(users)
    return users


def generate_friendships(users):
    n = len(users)
    user_ids = [u["id"] for u in users]
    friendships = {u["id"]: set() for u in users}

    for user in users:
        num_friends = random.randint(100, min(100, n - 1))
        possible_friends = [uid for uid in user_ids if uid != user["id"]]
        chosen = random.sample(possible_friends, num_friends)

        for fid in chosen:
            friendships[user["id"]].add(fid)
            friendships[fid].add(user["id"])

    for user in users:
        user["friends"] = list(friendships[user["id"]])


def check_bidirectional(users):
    for user in users:
        user_friends_ids = user["friends"]
        for fr_id in user_friends_ids:
            if fr_id not in users[user["id"]]["friends"]:
                print(f"ERROR {fr_id} is not in {users}")


def save_to_json(users, filename="users.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    print(f"Data saved in {filename}")


def save_to_csv(users, filename="users.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "f_name", "l_name", "lat", "long", "friends"])
        writer.writeheader()
        for u in users:
            writer.writerow(u)
    print(f"Data saved in {filename}")


if __name__ == "__main__":

    # #Generate 1000 users
    users = generate_users(1000)
    save_to_json(users, "../../data/users_1000.json")
    save_to_csv(users, "../../data/users_1000.csv")

    #Generate 10000 users
    users = generate_users(10000)
    save_to_json(users, "../../data/users_10000.json")
    save_to_csv(users, "../../data/users_10000.csv")

    #Generate 100000 users
    users = generate_users(100000)
    save_to_json(users, "../../data/users_100000.json")
    save_to_csv(users, "../../data/users_100000.csv")


