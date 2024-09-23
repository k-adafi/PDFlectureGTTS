from urllib.request import urlopen
from translate import Translator
from random import choice
import speech_recognition as sr
import pyttsx3
import subprocess
import wolframalpha
import webbrowser
import wikipedia
import datetime


def assistant_voix(sortie):
    if sortie:
        voix = pyttsx3.init()
        print("A.I : " + sortie)
        voix.say(sortie)
        voix.runAndWait()


def internet():
    try:
        urlopen('https://www.google.com', timeout=1)
        print("Connecté")
        return True
    except Exception as e:
        print(f"Déconnecté : " + str(e))
        return False


def reconnaissance():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    pas_compris = "Désolé, je n'ai pas compris! Pouvez-vous me donner plus de détail et me rédemander après, s'il vous plaît !"
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.7
        print("ecoute.... ")
        audio = r.listen(source)
        if internet():
            try:
                vocal = r.recognize_google(audio, language='fr-FR')
                print(vocal)
                return vocal
            except sr.UnknownValueError:
                assistant_voix(pas_compris)
        else:
            try:
                vocal = r.recognize_sphinx(audio, language='fr-fr')
                print(vocal)
                return vocal
            except sr.UnknownValueError:
                assistant_voix(pas_compris)


def application(entree):
    if entree:
        dico_apps = {
            "note": ["bloc-notes", "note", "bloc note"],
            "vscode": ["visual studio code"],
            "chrom": ["chrome", "google chrome", "google", "navigateur"]
        }
        fini = False
        while not fini:
            for x in dico_apps["note"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de l'application Bloc notes .")
                    subprocess.Popen('C:\\WINDOWS\\system32\\notepad.exe')
                    fini = True
            for x in dico_apps["vscode"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de l'éditeur de texte, Visual Studio Code .")
                    subprocess.Popen('C:\\Users\\KADAFI Ben\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
                    fini = True
            for x in dico_apps["chrom"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de navigateur web .")
                    subprocess.Popen('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
                    fini = True
            fini = True


def calcul(entree):
    if entree:
        traduction = Translator(to_lang="en").translate(entree)

        app_id = "L5H3JP-ERXK3EVKGW"
        client = wolframalpha.Client(app_id)
        res = client.query(traduction)
        try:
            reponse = next(res.results).text
            traduction_reponse = Translator(to_lang="fr").translate(reponse)
            assistant_voix("le résultat est %d" % (traduction_reponse))

        except Exception as e:
            assistant_voix("Il y'a eu l'erreur, " + str(e) + " désolé")


def sur_le_net(entree):
    if entree:
        if "youtube" in entree.lower():
            indx = entree.lower().split().index("youtube")
            recherche = entree.lower().split()[indx + 1:]
            if len(recherche) != 0:
                assistant_voix("recherche sur YouTube .")
                webbrowser.open("http://www.youtube.com/results?search_query=" + "+".join(recherche), new=2)
        elif "wikipédia" in entree.lower():
            wikipedia.set_lang("fr")
            try:
                recherche = entree.lower().replace("cherche sur wikipédia", "").strip()
                if recherche:
                    resultat = wikipedia.summary(recherche, sentences=1)
                    assistant_voix("Recherche sur Wikipédia.")
                    assistant_voix(resultat)
            except wikipedia.exceptions.DisambiguationError as e:
                assistant_voix("Désolé, plusieurs pages trouvées. Soyez plus précis.")
                print(f"Erreur de désambiguïsation : {e}")
            except wikipedia.exceptions.PageError as e:
                assistant_voix("Désolé, aucune page trouvée.")
                print(f"Erreur de page : {e}")

            """wikipedia.set_lang("fr")
            try:
                recherche = entree.lower().replace("cherche sur wikipédia", "")
                if len(recherche) != 0:
                    resultat = wikipedia.summary(recherche, sentences=1)
                    assistant_voix("recherche sur Wikipédia .")
                    assistant_voix(resultat)
            except Exception as e:
                assistant_voix("Désolé, aucune page trouvée ." + str(e))"""
        else:
            if "google" in entree.lower():
                indx = entree.lower().split().index("google")
                recherche = entree.lower().split()[indx + 1:]
                if len(recherche) != 0:
                    assistant_voix("recherche sur Google .")
                    webbrowser.open("https://www.google.com/search?q=" + "+".join(recherche), new=2)
            elif "cherche" in entree.lower() or "recherche" in entree.lower():
                indx = entree.lower().split().index("cherche")
                recherche = entree.lower().split()[indx + 1:]
                if len(recherche) != 0:
                    assistant_voix("recherche par défaut .")
                    webbrowser.open("https://www.google.com/search?q=" + "+".join(recherche), new=2)
            elif "recherche" in entree.lower():
                indx = entree.lower().split().index("recherche")
                recherche = entree.lower().split()[indx + 1:]
                if len(recherche) != 0:
                    assistant_voix("recherche sur Google .")
                    webbrowser.open("http://www.google.com/search?q=" + "+".join(recherche), new=2)


def main():
    assistant_voix(
        "Bonjour, je m'appel Victoria, je suis votre assistant de bureau vocal. Dites-moi ce que je peux faire pour vous aujourd'hui .")
    fermer = ["arrête-toi", "tais-toi", "fermeture"]
    ouvrir = ["ouvre", "ouvrir", "ouverture"]
    cava = ["comment allez-vous", "est-ce que ça va"]
    cherche = ["cherche sur youtube", "cherche sur google", "cherche sur wikipédia", "cherche"]
    calculs = ["calcule la somme de", "calcule la différence de", " calcule le produit de", "calcule le quotient de",
               "calcule"]
    salutation = ["bonjour victoria comment ça va", "bonjour comment",
                  "salut comment ça va", "Salut comment"]
    salutation1 = ["je vais bien aussi", "oui ça va"]
    appelation = ["comment tu t'appel", "qui es-tu", "quel est ton nom", "quel est ton non"]
    draguer = ["comment faire pour draguer une fille", "comment draguer une fille"]
    conseils = ["donne-moi un conseil pour réussir dans la vie", "comment faire pour devenir riche",
                "comment faire pour être riche", "comment faire pour être"]
    createur = ["qui est ton créateur", "qous êtes créé par qui"]
    heure = ["heure", "quelle heure est-il", "donner l'heure en ce moment", "donner l'heure"]
    date = ["date", "quelle est la date d'aujourd'hui", "donner la date en ce moment", "donner la date"]
    cv = ["comment faire un c v", "comment faire c v"]
    lettre = ["comment faire une lettre de motivation", "comment faire une lettre de demande", "comment rediger une lettre de motivation"]
    actif = True
    while actif:
        if (entree := reconnaissance()) is not None:
            for x in range(len(fermer)):
                if fermer[x] in entree.lower():
                    assistant_voix("A bientôt monsieur .")
                    actif = False
            for x in range(len(ouvrir)):
                if ouvrir[x] in entree.lower():
                    application(entree)
                    break
            for x in range(len(cava)):
                if cava[x] in entree.lower():
                    assistant_voix("Je vais bien merci, et vous ?")
                    break
            for x in range(len(cherche)):
                if cherche[x] in entree.lower():
                    sur_le_net(entree)
                    break
            for x in range(len(calculs)):
                if calculs[x] in entree.lower():
                    calcul(entree)
                    break
            for x in range(len(salutation)):
                if salutation[x] in entree.lower():
                    assistant_voix("Je vais bien de mon côté, comment allez-vous par contre ?")
                    break
            for x in range(len(salutation1)):
                if salutation1[x] in entree.lower():
                    assistant_voix("Géniale! Comment je puisse vous aider ?")
                    break
            for x in range(len(appelation)):
                if appelation[x] in entree.lower():
                    assistant_voix(
                        "je m'appel Victoria, je suis une intelligence artificielle développée et créée par Monsieur KADAFI Ben. .")
                    break
            for x in range(len(createur)):
                if createur[x] in entree.lower():
                    assistant_voix(
                        "Je suis une intelligence artificielle développée et créée par Monsieur KADAFI Ben .")
                    break
            for x in range(len(conseils)):
                if conseils[x] in entree.lower():
                    assistant_voix(
                        "Pour devenir riche, il faut que vous travailliez dur, mais plus important encore, il faut que vous travailliez intelligemment .")
                    break
            for x in range(len(lettre)):
                if lettre[x] in entree.lower():
                    assistant_voix(
                        "Rédiger une lettre de motivation efficace est essentiel pour capter l’attention des recruteurs. Voici quelques étapes pour t’aider à créer une lettre de motivation convaincante :"
                        "En-tête : Tes coordonnées (nom, adresse, téléphone, e-mail). Les coordonnées de l’entreprise (nom de l’entreprise, adresse, nom du recruteur si connu). La date."
                        "Objet : Indique l’objet de ta lettre, par exemple : “Candidature au poste de [Nom du poste]”."
                        "Salutation : Adresse la lettre à une personne spécifique si possible, par exemple : Madame/Monsieur [Nom]"
                        "Introduction : Présente-toi brièvement et explique pourquoi tu écris. Mentionne le poste pour lequel tu postules et comment tu as entendu parler de l’offre."
                        "Paragraphe : Montre que tu as fait des recherches sur l’entreprise. Explique pourquoi elle t’intéresse et ce que tu apprécies dans ses valeurs, ses projets ou son secteur d’activité1."
                        "Paragraphe Moi : Mets en avant tes compétences et expériences pertinentes pour le poste. Donne des exemples concrets de tes réalisations et explique en quoi elles sont en adéquation avec les besoins de l’entreprise2."
                        "Paragraphe Nous : Explique comment tu peux contribuer à l’entreprise et pourquoi tu serais un atout pour l’équipe. Montre ton enthousiasme et ta motivation à rejoindre l’entreprise1."
                        "Conclusion : Remercie le recruteur pour son temps et exprime ton souhait de le rencontrer pour discuter de ta candidature. Termine par une formule de politesse, par exemple : Je vous prie d’agréer, Madame/Monsieur, l’expression de mes salutations distinguées."
                        "Signature : Signe ta lettre si elle est imprimée. Sinon, indique simplement ton nom.")
                    break
            for x in range(len(cv)):
                if cv[x] in entree.lower():
                    assistant_voix(
                        "Choisir un modèle : Utilise des outils en ligne comme Canva ou Zety pour choisir un modèle de CV qui te plaît. Ces plateformes offrent des modèles gratuits et faciles à personnaliser."
                        "Informations personnelles : Commence par inclure tes informations de contact en haut de ton CV : nom, adresse, numéro de téléphone, et adresse e-mail."
                        "Titre et accroche : Ajoute un titre clair et une accroche percutante qui résume tes compétences et tes objectifs professionnels."
                        "Expérience professionnelle : Liste tes expériences professionnelles en ordre antéchronologique (de la plus récente à la plus ancienne). Pour chaque poste, mentionne le nom de l’entreprise, les dates de début et de fin, et une brève description de tes responsabilités et réalisations."
                        "Formation : Indique tes diplômes et formations pertinentes, en précisant les établissements fréquentés et les dates d’obtention."
                        "Compétences : Énumère tes compétences techniques et personnelles. Par exemple, pour toi, cela pourrait inclure des compétences en développement web (HTML, CSS, JavaScript, Symfony) et en design UX/UI."
                        "Langues : Mentionne les langues que tu maîtrises et ton niveau de compétence pour chacune."
                        "Sections supplémentaires : Ajoute des sections supplémentaires si nécessaire, comme les certifications, les projets personnels, les publications, ou les centres d’intérêt."
                        "Mise en page : Assure-toi que ton CV est bien structuré et facile à lire. Utilise des polices claires, des titres en gras, et des espaces suffisants entre les sections."
                        "Relecture : Relis ton CV pour corriger les fautes d’orthographe et de grammaire. Demande à quelqu’un d’autre de le relire pour avoir un avis extérieur."
                        "Pour plus de détails, tu peux consulter des guides en ligne comme celui de MakeMyCV ou regarder des tutoriels vidéo comme celui-ci pour des conseils pratiques.")
                    break
            for x in range(len(heure)):
                if heure[x] in entree.lower():
                    heur = datetime.datetime.now().strftime('%H:%M')
                    assistant_voix("il est" + heur)
                    break
            for x in range(len(date)):
                if date[x] in entree.lower():
                    today = datetime.datetime.now().strftime('%d/%m/%Y')
                    assistant_voix("Nous sommes le " + today)
                    break
            for x in range(len(draguer)):
                if draguer[x] in entree.lower():
                    assistant_voix(
                        "Draguer une fille que vous aimez peut être délicat, mais voici quelques conseils pour vous aider : "
                        "Soyez vous-même : L’authenticité est très importante. Ne prétendez pas être quelqu’un que vous n’êtes pas."
                        "Montrez de l’intérêt : Posez-lui des questions sur ses intérêts, ses passions, et écoutez attentivement ses réponses."
                        "Complimentez-la sincèrement : Un compliment authentique sur son apparence ou sa personnalité peut faire des merveilles."
                        "Soyez respectueux : Respectez ses limites et ne soyez pas insistant si elle ne semble pas intéressée."
                        "Humour : Utilisez l’humour pour briser la glace et créer une atmosphère détendue1."
                        "Prenez soin de votre apparence : Une bonne hygiène et une tenue soignée peuvent faire une grande différence2."
                        "Si vous cherchez des idées de messages pour commencer une conversation, voici quelques exemples :"
                        "Salut, j’ai remarqué que tu aimes [son intérêt]. Moi aussi, j’adore ça !”"
                        "J’ai vu que tu as lu [un livre qu’elle aime]. Qu’en as-tu pensé ?")
                    break


if __name__ == '__main__':
    main()
