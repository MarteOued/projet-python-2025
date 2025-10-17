"""
Module d'acquisition de données depuis Reddit et Arxiv

"""

import praw
import urllib.request
import xmltodict


def get_reddit_docs(keyword, limit=20, client_id=None, client_secret=None, user_agent=None):
    """
    On récupère des documents depuis Reddit via l'API praw
    
    Args:
        keyword (str): Mot-clé de recherche
        limit (int): Nombre maximum de documents à récupérer
        client_id (str): ID client Reddit API
        client_secret (str): Secret client Reddit API
        user_agent (str): User agent pour l'API
    
    Returns:
        list: Liste de dictionnaires contenant les documents
    """
    print(f" Recherche sur Reddit : '{keyword}' (limit={limit})")
    
    # Connexion à l'API Reddit
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    
    docs = []
    
    # Recherche sur tous les subreddits
    for submission in reddit.subreddit("all").search(keyword, limit=limit):
        # Récupération du titre + texte
        texte = submission.title + " " + submission.selftext
        
        # Nettoyage des sauts de ligne
        texte = texte.replace("\n", " ")
        
        # Création du document
        doc = {
            'texte': texte,
            'source': 'reddit',
            'titre': submission.title,
            'auteur': str(submission.author),
            'date': submission.created_utc,
            'url': f"https://reddit.com{submission.permalink}"
        }
        
        docs.append(doc)
    
    print(f" {len(docs)} documents Reddit récupérés")
    return docs


def get_arxiv_docs(keyword, limit=20):
    """
    On récupère des documents depuis Arxiv via l'API
    
    Args:
        keyword (str): Mot-clé de recherche
        limit (int): Nombre maximum de documents à récupérer
    
    Returns:
        list: Liste de dictionnaires contenant les documents
    """
    print(f" Recherche sur Arxiv : '{keyword}' (limit={limit})")
    
    # Construction de l'URL pour l'API
    query = keyword.replace(" ", "+")
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={limit}"
    
    # Requête vers l'API
    with urllib.request.urlopen(url) as response:
        data = response.read()
    
    # Parser le XML
    articles = xmltodict.parse(data)
    
    docs = []
    
    # Parcourir les articles
    if 'entry' in articles['feed']:
        entries = articles['feed']['entry']
        
        # Si un seul résultat, le mettre dans une liste
        if not isinstance(entries, list):
            entries = [entries]
        
        for entry in entries:
            # Récupération du résumé (abstract)
            texte = entry.get('summary', '').replace("\n", " ")
            
            # Gestion de l'auteur (peut être dict ou liste)
            auteur = 'Unknown'
            if 'author' in entry:
                if isinstance(entry['author'], dict):
                    auteur = entry['author'].get('name', 'Unknown')
                elif isinstance(entry['author'], list):
                    auteur = entry['author'][0].get('name', 'Unknown')
            
            # Création du document
            doc = {
                'texte': texte,
                'source': 'arxiv',
                'titre': entry.get('title', '').replace("\n", " "),
                'auteur': auteur,
                'date': entry.get('published', ''),
                'url': entry.get('id', '')
            }
            
            docs.append(doc)
    
    print(f"{len(docs)} documents Arxiv récupérés")
    return docs


def get_docs(keyword, nb_reddit=20, nb_arxiv=20, 
             reddit_client_id=None, reddit_client_secret=None, reddit_user_agent=None):
    """
    On récupère des documents depuis Reddit ET Arxiv
    
    Args:
        keyword (str): Mot-clé de recherche
        nb_reddit (int): Nombre de docs Reddit
        nb_arxiv (int): Nombre de docs Arxiv
        reddit_client_id, reddit_client_secret, reddit_user_agent: Credentials Reddit
    
    Returns:
        list: Liste combinée de tous les documents
    """
    print(f"\n{'='*70}")
    print(f" Acquisition de documents sur : '{keyword}'")
    print(f"{'='*70}\n")
    
    # Récupération Reddit
    docs_reddit = get_reddit_docs(
        keyword, 
        limit=nb_reddit,
        client_id=reddit_client_id,
        client_secret=reddit_client_secret,
        user_agent=reddit_user_agent
    )
    
    # Récupération Arxiv
    docs_arxiv = get_arxiv_docs(keyword, limit=nb_arxiv)
    
    # Combinaison
    all_docs = docs_reddit + docs_arxiv
    
    print(f"\n Total : {len(all_docs)} documents récupérés")
    print(f"   - Reddit : {len(docs_reddit)}")
    print(f"   - Arxiv  : {len(docs_arxiv)}")
    
    return all_docs
