from rapidfuzz import process, fuzz


def findBestMatch(word, choices, threshold=75):

    if not word:
        return word

    result = process.extractOne(word, choices, scorer=fuzz.ratio)

    if result is None:
        return word

    match, score, _ = result

    if score >= threshold:
        return match

    return word


def correctTarget(action, target, applications, websites, folders):

    if not target:
        return target

    if action == "open":

        choices = (
            list(applications.keys()) + list(websites.keys()) + list(folders.keys())
        )

    elif action == "search":

        choices = list(websites.keys())

    elif action == "close":

        choices = list(applications.keys()) + list(websites.keys())

    else:
        return target

    return findBestMatch(target, choices)
