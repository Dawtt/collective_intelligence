import random


### STEP 1:     find similar users
from collecting_preferences_1.critics_dictionary import critics



print(critics)
print(type(critics))
print(critics['Michael Phillips'])
print(critics['Toby'])
print(critics['Toby']['Snakes on a Plane'])
print(len(critics))


### STEP 2:     find distances


def sim_distance(prefs, person1, person2):
    sim = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            print("similar item found:  ", item)
            sim[item] = 1
    if len(sim) == 0:
        return 0

    # start euclidean length calculations
    sum_of_squares = sum([pow( prefs[person1][item] - prefs[person2][item]
                               , 2)
                          for item in sim])
    return 1/1 + sum_of_squares

def sim_distance_book(prefs, person1, person2):
    sim = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            #print("similar item found:  ", item)
            sim[item] = 1
    if len(sim) == 0:
        return 0

    # start euclidean length calculations
    sum_of_squares = sum([pow( prefs[person1][item] - prefs[person2][item]
                               , 2)
                          for item in prefs[person1]
                          if item in prefs[person2]])
    return 1/(1 + sum_of_squares)

# brainstorming
def get_user_names(dictionary):
    nameslist = []
    for name in dictionary:
        nameslist.append(name)
    return nameslist

print(get_user_names(critics))
names_list = get_user_names(critics)


def ran_name():
    names = get_user_names(critics)
    return random.choice(names)


def get_random_similarities(prefs):
    names = get_user_names(prefs)
    name1 = random.choice(names)
    name2 = random.choice(names)
    print(name1)
    print(name2)
    print("similarity between ", name1, " and ", name2, ":\n")
    print(sim_distance_book(critics, name1, name2))


def top_matches(prefs, person, n=5, similarity = sim_distance):
    print("top matches started")
    scores = [(sim_distance_book(prefs, person, other)) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[:n]


get_random_similarities(critics)

print(top_matches(critics, ran_name()))


### STEP 3      CREATE RECOMMENDATION:
# find movies not seen by user
# find most similar users
# find movies from them
# create ratings from those unseen movies


def get_recommendations(prefs, person):
    print("starting get_recommendations")
    totals = {}
    sim_sum = {}

    for other in prefs:
        if other == person:
            continue
        sim = sim_distance_book(prefs, person, other)
        if sim <= 0: continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                sim_sum.setdefault(item, 0)
                sim_sum[item] += sim
    rankings = [(total / sim_sum[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


print(get_recommendations(critics, ran_name()))

