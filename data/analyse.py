import nltk
from nltk.corpus import wordnet as wn
import re
import os
from nltk.corpus import stopwords
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('omw-1.4')
stop_words = set(stopwords.words('french'))
nltk.download('wordnet')

def convertir_en_texte(repertoire, nom_fichier=None):
    extensions = ('.docx',)
    try:
        if nom_fichier:
            nom_fichier = nom_fichier + '.docx'
            chemin_fichier = os.path.join(repertoire, nom_fichier)
            if os.path.isfile(chemin_fichier) and nom_fichier.endswith(extensions):
                # Extraire le texte à partir du fichier
                texte = docx2txt.process(chemin_fichier)
                    
                # Créer un nouveau nom de fichier pour le fichier texte
                nouveau_nom_fichier = os.path.splitext(nom_fichier)[0] + '.txt'
                nouveau_chemin_fichier = os.path.join(repertoire, nouveau_nom_fichier)
                    
                # Écrire le texte extrait dans un nouveau fichier texte
                with open(nouveau_chemin_fichier, 'w', encoding='utf-8') as f:
                    f.write(texte)
        else:
            for nom_fichier in os.listdir(repertoire):
                chemin_fichier = os.path.join(repertoire, nom_fichier)
                if os.path.isfile(chemin_fichier) and nom_fichier.endswith(extensions):
                    # Extraire le texte à partir du fichier
                    texte = docx2txt.process(chemin_fichier)
                    
                    # Créer un nouveau nom de fichier pour le fichier texte
                    nouveau_nom_fichier = os.path.splitext(nom_fichier)[0] + '.txt'
                    nouveau_chemin_fichier = os.path.join(repertoire, nouveau_nom_fichier)
                    
                    # Écrire le texte extrait dans un nouveau fichier texte
                    with open(nouveau_chemin_fichier, 'w', encoding='utf-8') as f:
                        f.write(texte)
    except Exception as error:
        print("An exception occurred:", error)

def lire_fichiers_texte(repertoire, nom_fichier=None):
    dictionnaire = {}
    try:
        if nom_fichier:
            nom_fichier = str(nom_fichier) + '.txt'
            if nom_fichier.endswith('.txt'):
                chemin_fichier = os.path.join(repertoire, nom_fichier)
                try:
                    with open(chemin_fichier, 'rt', encoding='utf-8') as fichier:
                        contenu = fichier.read()
                except UnicodeDecodeError:
                    with open(chemin_fichier, 'rt', encoding='ISO-8859-1') as fichier:
                        contenu = fichier.read()
                contenu = contenu.replace('\n', ' ')
                dictionnaire[nom_fichier] = contenu
        else:
            for nom_fichier in os.listdir(repertoire):
                if nom_fichier.endswith('.txt'):
                    chemin_fichier = os.path.join(repertoire, nom_fichier)
                    try:
                        with open(chemin_fichier, 'rt', encoding='utf-8') as fichier:
                            contenu = fichier.read()
                    except UnicodeDecodeError:
                        with open(chemin_fichier, 'rt', encoding='ISO-8859-1') as fichier:
                            contenu = fichier.read()
                    contenu = contenu.replace('\n', ' ')
                    dictionnaire[nom_fichier] = contenu
    except Exception as error:
        print("An exception occurred:", error)
    
    return dictionnaire
    
def extraire_pages_de_garde(dictionnaire_nettoye):
    # MOTIFS DE RECHERCHE
    code_expression = r'N° d’ordre :' + r'(.*?)' + r'Mémoire'
    students_expression = re.escape(r'Par :') + r'(.*?)' + re.escape(r'Soutenu')
    jury_expression = r'devant le jury composé de :(.*?)\bExaminateur\b'
    titre_expression = r'Parcours(.*?)Par'

    # LISTE POUR STOCKER LES INFORMATIONS DE LA PAGE DE GARDE
    pages_de_garde = []
    mots_vides = set(stopwords.words('french'))


    descripteur_global = {
        "codes_pages_de_garde": [],
        "titres_pages_de_garde": [],
        "liens_descripteurs_locaux": []
    }

    for nom_fichier, contenu in dictionnaire_nettoye.items():
        file_list = [nom_fichier]
        code_list = []
        students_list = []
        jury_list = []
        titre_list = []

        # Code
        if re.search(code_expression, contenu):
            code = re.search(code_expression, contenu)
            code_list.append(code.group(1).replace(":", "", 1))
            descripteur_global["codes_pages_de_garde"].append(code.group(1).replace(":", "", 1))
        else:
            code_list.append('')

        # Students
        if re.search(students_expression, contenu.replace("\xa0", "")):
            students = re.search(students_expression, contenu.replace("\xa0", ""))
            students_list.append(students.group(1))
        else:
            students_list.append('')

        # Jury
        if re.search(jury_expression, contenu.replace("\xa0", "")):
            jury_match = re.search(jury_expression, contenu.replace("\xa0", ""))
            jury_text = jury_match.group(1)
            examinateur = "Examinateur"
            jury_list.append(jury_text + examinateur)
        else:
            jury_list.append('')

        # Titre
        if re.search(titre_expression, contenu.replace("\xa0", "")):
            match = re.search(titre_expression, contenu.replace("\xa0", ""))
            titre_text = match.group(1).strip()

            # Nettoyage du titre
            titre_nettoye = []
            for mot in titre_text.split():
                mot = re.sub(r'[^\w\s]', '', mot)  # Supprimer les caractères spéciaux
                mot = mot.lower()  # Convertir en minuscules
                if mot and mot not in mots_vides:  # Vérifier s'il n'est pas vide et pas un mot vide
                    titre_nettoye.append(mot)
            titre_list.append(titre_nettoye)
            descripteur_global["titres_pages_de_garde"].append(titre_text)

            # SEGMENTATION DU TITRE
            titre_segmente = {}
            taille_paragraphe = 255  # Taille fixe en caractères pour les paragraphes
            taille_phrase = 66  # Taille fixe en caractères pour les phrases
            taille_mot = 10  # Taille fixe en caractères pour les mots

            # Segmentation des paragraphes
            paragraphes = []
            paragraphe_courant = ""
            mots = []
            mots_courants = []

            for mot in titre_nettoye:
                if len(paragraphe_courant) + len(mot) + 1 <= taille_paragraphe:
                    paragraphe_courant += mot + " "
                    mots_courants.append(mot)
                else:
                    paragraphes.append(paragraphe_courant.strip())
                    paragraphe_courant = mot + " "
                    mots.append(mots_courants)
                    mots_courants = [mot]

            if paragraphe_courant:
                paragraphes.append(paragraphe_courant.strip())
                mots.append(mots_courants)

            titre_segmente["paragraphes"] = paragraphes
            titre_segmente["mots"] = mots

            nombre_paragraphes = len(paragraphes)
            nombre_mots = sum([len(p) for p in mots])
            nombre_phrases = sum([len(nltk.sent_tokenize(p)) for p in paragraphes])

            titre_segmente["nombre_paragraphes"] = nombre_paragraphes
            titre_segmente["nombre_phrases"] = nombre_phrases
            titre_segmente["nombre_mots"] = nombre_mots

            descripteur_local_titre = {
                "nombre_paragraphe": nombre_paragraphes,
                "nombre_phrase": nombre_phrases,
                "nombre_mot": nombre_mots,
            }
            titre_segmente["descripteur_local"] = descripteur_local_titre
            descripteur_global["liens_descripteurs_locaux"].append({
                "type": "titre",
                "lien": titre_segmente["descripteur_local"]
            })

        pages_de_garde.append({
            "code": code_list,
            "students": students_list,
            "jury": jury_list,
            "titre": titre_list
        })

    return descripteur_global

def extraire_introduction(dictionnaire_nettoye, descripteur_global):
    # MOTIF DE RECHERCHE
    intro_expression = r'Introduction générale [\s\n]+(.*?)Chapitre'

    # LISTE POUR STOCKER LES INFORMATIONS DE L'INTRODUCTION
    introduction = []
    descripteur_code = {}
    for nom_fichier, contenu in dictionnaire_nettoye.items():
        file_list = [nom_fichier]
        intro_list = []
        if re.search(intro_expression, contenu):
            intro = re.search(intro_expression, contenu)
            intro_text = intro.group(1).strip()

            # SEGMENTATION DE L'INTRODUCTION
            intro_segmentee = {}
            intro_segmentee["paragraphes"] = intro_text.split("\n")
            nombre_paragraphes = len(intro_segmentee["paragraphes"])
            phrases = []
            for paragraphe in intro_segmentee["paragraphes"]:
                phrases.extend(nltk.sent_tokenize(paragraphe))
            intro_segmentee["phrases"] = phrases
            nombre_phrases = len(phrases)
            mots = []
            for phrase in phrases:
                for word in nltk.word_tokenize(phrase):
                    synonyms = []
                    for syn in wn.synsets(word, lang='fra'):
                        for lemma in syn.lemmas(lang='fra'):
                            if lemma.name() != word:
                                synonyms.append(lemma.name())
                    mots.append({
                        "texte": word,
                        "synonymes": synonyms,
                        "prefixes": [word[:i] for i in range(3, min(len(word), 3) + 1)],
                        "suffixes": [word[-i:] for i in range(3, min(len(word), 3) + 1)],
                    })

                intro_segmentee["mots"] = mots
                nombre_mots = len(mots)
            intro_segmentee["nombre_paragraphes"] = nombre_paragraphes
            intro_segmentee["nombre_phrases"] = nombre_phrases
            intro_segmentee["nombre_mots"] = nombre_mots
            intro_list.append(intro_segmentee)

            # Création du descripteur local
            descripteur_local_intro = {
                "nombre_paragraphe": nombre_paragraphes,
                "nombre_phrase": nombre_phrases,
                "nombre_mot": nombre_mots,
            }
            intro_segmentee["descripteur_local"] = descripteur_local_intro
            descripteur_global["liens_descripteurs_locaux"].append({
                "type": "introductuion",
                "lien": intro_segmentee["descripteur_local"]
            
            })
        introduction.append(intro_list)
    return descripteur_local_intro

def extraire_conclusion(dictionnaire_nettoye, descripteur_global):
    # MOTIF DE RECHERCHE
    conclu_expression = r'Conclusion générale [\s\n]+(.*?)Bibliographie'

    # LISTE POUR STOCKER LES INFORMATIONS DE LA CONCLUSION
    conclusion = []
    for nom_fichier, contenu in dictionnaire_nettoye.items():
        file_list = [nom_fichier]
        conclu_list = []
        if re.search(conclu_expression, contenu):
            conclu = re.search(conclu_expression, contenu)
            conclu_text = conclu.group(1).strip()

            # SEGMENTATION DE LA CONCLUSION
            conclu_segmentee = {}
            conclu_segmentee["paragraphes"] = conclu_text.split("\n")
            nombre_paragraphes = len(conclu_segmentee["paragraphes"])
            phrases = []
            for paragraphe in conclu_segmentee["paragraphes"]:
                phrases.extend(nltk.sent_tokenize(paragraphe))
            conclu_segmentee["phrases"] = phrases
            nombre_phrases = len(phrases)
            mots = []
            for phrase in phrases:
                for word in nltk.word_tokenize(phrase):
                    synonyms = []
                    for syn in wn.synsets(word, lang='fra'):
                        for lemma in syn.lemmas(lang='fra'):
                            if lemma.name() != word:
                                synonyms.append(lemma.name())
                    mots.append({
                        "texte": word,
                        "synonymes": synonyms,
                        "prefixes": [word[:i] for i in range(3, min(len(word), 3) + 1)],
                        "suffixes": [word[-i:] for i in range(3, min(len(word), 3) + 1)],
                    })

                conclu_segmentee["mots"] = mots
                nombre_mots = len(mots)
            conclu_segmentee["nombre_paragraphes"] = nombre_paragraphes
            conclu_segmentee["nombre_phrases"] = nombre_phrases
            conclu_segmentee["nombre_mots"] = nombre_mots
            conclu_list.append(conclu_segmentee)

            # Création du descripteur local
            descripteur_local_conclu = {
                "nombre_paragraphe": nombre_paragraphes,
                "nombre_phrase": nombre_phrases,
                "nombre_mot": nombre_mots,
            }
            conclu_segmentee["descripteur_local"] = descripteur_local_conclu
            descripteur_global["liens_descripteurs_locaux"].append({
                "type": "conclusion",
                "lien": conclu_segmentee["descripteur_local"]
            })

        conclusion.append(conclu_list)
    return descripteur_local_conclu    

def Segmentation(repertoire, nom_fichier=None):
    convertir_en_texte(repertoire, nom_fichier)
    dictionnaire_nettoye = lire_fichiers_texte(repertoire, nom_fichier)
    descripteurs_globaux = []
    
    descripteur_global = extraire_pages_de_garde(dictionnaire_nettoye)
    descripteur_local_intro = extraire_conclusion(dictionnaire_nettoye, descripteur_global)
    descripteur_local_conclu = extraire_introduction(dictionnaire_nettoye, descripteur_global)
    descripteurs_globaux.append(descripteur_global)

    return descripteurs_globaux

def concatener_mots_titres(descripteurs_globaux):
    mots_concatenes = []

    for descripteur_global in descripteurs_globaux:
        titres_pages_de_garde = descripteur_global.get("titres_pages_de_garde")
        if titres_pages_de_garde:
            mots_concatenes.extend(titres_pages_de_garde)

    return mots_concatenes

def rechercher_titres_similaires(titre_cible, titres):
    
    # Prétraitement du titre cible en supprimant les mots vides
    mots_vides = set(stopwords.words('french'))
    mots_titre_cible = [mot for mot in titre_cible.lower().split() if mot not in mots_vides]

    # Liste des titres pertinents
    titres_pertinents = []

    # Recherche des titres similaires
    for titre in titres:
        mots_titre = titre.lower().split()

        # Vérification de la similarité des mots dans le même ordre
        if mots_titre_cible == mots_titre:
            titres_pertinents.append(titre)
        else:
            # Vérification de la similarité des mots dans un autre ordre
            mots_titre_triés = sorted(mots_titre)
            mots_titre_cible_triés = sorted(mots_titre_cible)
            if set(mots_titre_cible_triés).issubset(set(mots_titre_triés)):
                titres_pertinents.append(titre)

    return titres_pertinents

def recuperer_descripteur(titres_pertinents, liste_descripteurs):
    descripteur_pertinent = None
    for titre in titres_pertinents:
        for descripteur in liste_descripteurs:
            titres_pages_de_garde = descripteur.get("titres_pages_de_garde", [])
            for titre_page_de_garde in titres_pages_de_garde:
                if titre.lower() in titre_page_de_garde.lower():
                    descripteur_pertinent = descripteur
                    break
            if descripteur_pertinent is not None:
                break
        if descripteur_pertinent is not None:
            break
    return descripteur_pertinent
    
def calculer_similarite_cosinus(descripteur_cible, descripteurs_pertinents):
    # Extraire les titres des descripteurs cible et pertinents
    titre_cible = descripteur_cible.get("titres_pages_de_garde", [""])[0]
    titres_pertinents = [descripteur.get("titres_pages_de_garde", [""])[0] for descripteur in descripteurs_pertinents]

    # Concaténer les titres en une seule chaîne de caractères
    tous_les_titres = titres_pertinents + [titre_cible]

    # Calculer la similarité cosinus entre le descripteur cible et les descripteurs pertinents
    vectorizer = TfidfVectorizer()
    vecteurs = vectorizer.fit_transform(tous_les_titres)
    similarites = cosine_similarity(vecteurs[:-1], vecteurs[-1])

    return similarites
    
def recherche(repertoire, titre_cible):
    titres = []
    discripteur= Segmentation(repertoire)
    titres = concatener_mots_titres(discripteur)
    titres_pertinents=rechercher_titres_similaires(titre_cible, titres)
    descripteur_pertinent=recuperer_descripteur(titres_pertinents, discripteur)
    
    return descripteur_pertinent