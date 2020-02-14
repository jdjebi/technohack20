import hashlib


def coder_mdp(password):

    chaine_mot_de_passe = password.encode()
    mot_de_passe_chiffre = hashlib.sha1(chaine_mot_de_passe).hexdigest()

    return mot_de_passe_chiffre
