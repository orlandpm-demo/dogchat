dogs = [
    {
        "name" : "Melba",
        "handle" : "melba",
        "bio" : "Hi, I'm Melba! I'm a mini-goldendoodle and I love to play.",
        "age" : 3
    },
    {
        "name" : "Charlie",
        "handle" : "chucky",
        "bio" : "Hi I'm Charlie! I'm a big white standard poodle.",
        "age" : 7
    },
    {
        "name" : "Rosie",
        "handle" : "rose",
        "bio" : "Hi I'm Rosie! I'm from the hard streets of LA, don't mess with me.",
        "age" : 9
    }
]

def get_dog_by_handle(handle):
    for dog in dogs:
        if dog['handle'] == handle:
            return dog
    return None

posts = [
    ("melba", "I'm so excited to move to California!"),
    ("melba", "Great game of fetch today with my Dad, Paul"),
    ("chucky", "Took a great 8 hour nap today, then guarded the household"),
    ("melba", "Peanut butter is my favorite snack!"),
    ("rose", "Today I stole food from a blind dog.")
]


def get_posts_by_handle(handle):
    results = []
    for post in posts:
        if post[0] == handle:
            results.append(post)
    return results
