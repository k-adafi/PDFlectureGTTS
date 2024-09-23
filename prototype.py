from urllib.request import urlopen
from googletrans import Translator
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
        print(f"Déconnecté : {e}")
        return False


def reconnaissance():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    pas_compris = "Désolé, je n'ai pas compris! Pouvez-vous me donner plus de détail et me rédemander après, s'il vous plaît ?"
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.7
        print("écoute:............. ")
        audio = r.listen(source)
        if internet():
            try:
                vocal = r.recognize_google(audio, language='fr-FR')
                print(vocal)
                return vocal
            except sr.UnknownValueError:
                assistant_voix(pas_compris)
                print("Erreur de reconnaissance Google : Valeur inconnue")
            except sr.RequestError as e:
                assistant_voix("Erreur de service Google")
                print(f"Erreur de service Google : {e}")
        else:
            try:
                vocal = r.recognize_sphinx(audio, language='fr-fr')
                print(vocal)
                return vocal
            except sr.UnknownValueError:
                assistant_voix(pas_compris)
                print("Erreur de reconnaissance Sphinx : Valeur inconnue")
            except sr.RequestError as e:
                assistant_voix("Erreur de service Sphinx")
                print(f"Erreur de service Sphinx : {e}")


"""def reconnaissance():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    pas_compris = "Désolé, je n'ai pas compris! Pouvez-vous me donner plus de détail s'il vous plaît ?"
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.7
        print("écoute......... ")
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
                assistant_voix(pas_compris)"""

# Application à ouvrir
dico_apps = {
    "note": ["bloc-notes", "note", "bloc note"],
    "vscode": ["code", "visual studio", "visual studio code"],
    "git": ["git", "git bash"],
    "cmd": ["c m d", "invite de commande"]
}


def application(entree):
    if entree:
        for app, keywords in dico_apps.items():
            for keyword in keywords:
                if keyword in entree.lower():
                    if app == "note":
                        assistant_voix("Ouverture de l'application Bloc notes.")
                        subprocess.Popen('C:\\WINDOWS\\system32\\notepad.exe')
                    elif app == "vscode":
                        assistant_voix("Ouverture de l'éditeur de texte, Visual Studio Code.")
                        subprocess.Popen('C:\\Users\\KADAFI Ben\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
                    elif app == "git":
                        assistant_voix("Ouverture du terminale git bash.")
                        subprocess.Popen('C:\\Program Files\\Git\\git-bash.exe')
                    elif app == "cmd":
                        assistant_voix("Ouverture de l'invite de commande.")
                        subprocess.Popen('C:\\WINDOWS\\system32\\cmd.exe')
                    return


# Fonction de calcul avec WolframAlpha
def calcul(entree):
    if entree:
        traduction = Translator().translate(entree, dest='en').text
        app_id = "L5H3JP-ERXK3EVKGW"
        client = wolframalpha.Client(app_id)
        res = client.query(traduction)
        try:
            reponse = next(res.results).text
            traduction_reponse = Translator().translate(reponse, dest='fr').text
            assistant_voix(f"Le résultat est {traduction_reponse}")
        except StopIteration:
            assistant_voix("Il y a eu une erreur, désolé.")


def sur_le_net(entree):
    if entree:
        if "youtube" in entree.lower():
            indx = entree.lower().split().index("youtube")
            recherche = entree.lower().split()[indx + 1:]
            if recherche:
                assistant_voix("Recherche sur YouTube.")
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
        else:
            if "google" in entree.lower():
                indx = entree.lower().split().index("google")
                recherche = entree.lower().split()[indx + 1:]
                if recherche:
                    assistant_voix("Recherche sur Google.")
                    webbrowser.open("https://www.google.com/search?q=" + "+".join(recherche), new=2)
            elif "cherche" in entree.lower() or "recherche" in entree.lower():
                indx = entree.lower().split().index("cherche")
                recherche = entree.lower().split()[indx + 1:]
                if recherche:
                    assistant_voix("Recherche par défaut.")
                    webbrowser.open("https://www.google.com/search?q=" + "+".join(recherche), new=2)


def main():
    assistant_voix("Bonjour, je m'appel Victoria, je suis votre assistant de bureau vocal. Dites-moi ce que je peux faire pour vous !")
    salutation = ["Bonjour Victoria comment ça va!"]
    appelation = ["Comment tu t'appele ?", "Qui es tu ?"]
    draguer = ["Comment faire pour draguer une fille ?", "Comment draguer une fille ?"]
    fermer = ["arrête-toi", "fermer", "tais-toi", "tu peux disposer"]
    ouvrir = ["ouvre", "ouvrir", "salut! j'ai besoin de tes services.", "salut! j'ai besoin de toi."]
    cava = ["comment allez-vous", "est-ce que ça va", "Comment vas-tu ?"]
    cherche = ["cherche sur youtube", "cherche sur google", "cherche sur facebook", "cherche sur wikipédia", "cherche"]
    calculs = ["calcule la somme de", "calcule la différence de", "calcule le produit de", "calcule le quotient de",
               "calcule", "calcule la division de"]
    heure = ["heure", "Quel l'heure y ait-il ?", "Donner l'heure en ce moment", "Donner l'heure"]
    actif = True
    while actif:
        if (entree := reconnaissance()) is not None:
            for phrase in cherche:
                if phrase in entree.lower():
                    sur_le_net(entree)
                    break
            for phrase in calculs:
                if phrase in entree.lower():
                    calcul(entree)
                    break
            for phrase in ouvrir:
                if phrase in entree.lower():
                    application(entree)
                    break
            for phrase in fermer:
                if phrase in entree.lower():
                    assistant_voix("Passez une bonne journée alors, à bientôt!")
                    actif = False
                    break
            for phrase in appelation:
                if phrase in entree.lower():
                    assistant_voix("je m'appele Victoria, je suis un intelligence artificiel développer par Monsieur KADAFI Ben")
                    break
            for phrase in salutation:
                if phrase in entree.lower():
                    assistant_voix("Je vais bien merci, comment je peux vous aider ?")
                    break
            for phrase in cava:
                if phrase in entree.lower():
                    assistant_voix("Je vais bien merci, comment je peux vous aider ?")
                    break
            for phrase in draguer:
                if phrase in entree.lower():
                    assistant_voix("Draguer une fille que vous aimez peut être délicat, mais voici quelques conseils pour vous aider : "
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
            for phrase in heure:
                if phrase in entree.lower():
                    heur = datetime.datetime.now().strftime('%H:%M')
                    assistant_voix("il est" + heur)
                    break


if __name__ == '__main__':
    main()
