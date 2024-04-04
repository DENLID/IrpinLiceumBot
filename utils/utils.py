from update_info.update_info import alphabet_ukr

all_class = [f"{n}-{l}" for n in range(11) for l in alphabet_ukr]

def get_user_class(user):
    user_class = next((c for c in all_class if c in user["tags"]), None)
    return user_class