import json


def translate(key, lang='fr'):
    """
    Une fonction de traduction
    """
    with open('langs.json') as fichier:
        trans = json.load(fichier)
    mot_cle = trans.get(key)
    if mot_cle:
        return mot_cle.get(lang) \
            if mot_cle.get(lang) else mot_cle
    else:
        return key
