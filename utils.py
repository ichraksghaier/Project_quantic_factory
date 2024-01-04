def get_season(month):
    if (month) == None:
        return None
    elif 3 <= month <= 5:
        return 'Printemps'
    elif 6 <= month <= 8:
        return 'Été'
    elif 9 <= month <= 11:
        return 'Automne'
    else:
        return 'Hiver'