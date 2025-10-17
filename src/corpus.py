"""
Module de gestion du corpus de documents
"""

import pandas as pd


class Corpus:
    """
    Classe représentant un corpus de documents
    """
    
    def __init__(self, docs):
        """
        Initialise le corpus avec une liste de documents
        
        Args:
            docs (list): Liste de dictionnaires représentant les documents
        """
        self.docs = docs
        self.df = None
        self._create_dataframe()
    
    
    def _create_dataframe(self):
        """
        Crée le DataFrame pandas à partir des documents (méthode privée)
        """
        if not self.docs:
            print(" Aucun document dans le corpus")
            self.df = pd.DataFrame()
            return
        
        # Création du DataFrame avec id, texte, source
        data = []
        for i, doc in enumerate(self.docs):
            data.append({
                'id': i,
                'texte': doc['texte'],
                'source': doc['source']
            })
        
        self.df = pd.DataFrame(data)
        print(f" DataFrame créé : {len(self.df)} documents")
    
    
    def save(self, filename):
        """
        Sauvegarde le corpus dans un fichier CSV
        
        Args:
            filename (str): Nom du fichier (ex: 'data/corpus.csv')
        """
        if self.df is None or self.df.empty:
            print(" Aucun document à sauvegarder")
            return
        
        self.df.to_csv(filename, sep='\t', index=False)
        print(f" Corpus sauvegardé dans '{filename}' ({len(self.df)} documents)")
    
    
    @staticmethod
    def load(filename):
        """
        Charge un corpus depuis un fichier CSV
        
        Args:
            filename (str): Nom du fichier à charger
        
        Returns:
            Corpus: Instance de Corpus chargée depuis le fichier
        """
        print(f" Chargement du corpus depuis '{filename}'...")
        df = pd.read_csv(filename, sep='\t')
        
        # Reconstruction de la liste de docs
        docs = []
        for _, row in df.iterrows():
            docs.append({
                'texte': row['texte'],
                'source': row['source']
            })
        
        corpus = Corpus(docs)
        print(f" {len(corpus.df)} documents chargés")
        return corpus
    
    
    def clean(self, min_length=20):
        """
        Nettoie le corpus en supprimant les documents trop courts
        
        Args:
            min_length (int): Longueur minimale en caractères (défaut: 20)
        """
        if self.df is None or self.df.empty:
            print(" Aucun document à nettoyer")
            return
        
        print(f"\n Nettoyage du corpus (min {min_length} caractères)...")
        nb_avant = len(self.df)
        
        # Filtrage
        self.df = self.df[self.df['texte'].str.len() > min_length].copy()
        
        # Réinitialisation des IDs
        self.df['id'] = range(len(self.df))
        
        nb_apres = len(self.df)
        nb_supprimes = nb_avant - nb_apres
        
        print(f" Nettoyage terminé")
        print(f"   Documents avant : {nb_avant}")
        print(f"   Documents après : {nb_apres}")
        print(f"   Supprimés : {nb_supprimes}")
    
    
    def get_stats(self):
        """
        Affiche les statistiques du corpus
        """
        if self.df is None or self.df.empty:
            print(" Corpus vide")
            return
        
        print(f"\n{'='*70}")
        print(f" STATISTIQUES DU CORPUS")
        print(f"{'='*70}\n")
        
        # Nombre de documents
        print(f"📄 Nombre total de documents : {len(self.df)}")
        
        # Répartition par source
        print(f"\n Répartition par source :")
        for source, count in self.df['source'].value_counts().items():
            print(f"   - {source:10} : {count} documents")
        
        # Statistiques sur les mots et phrases
        self.df['nb_mots'] = self.df['texte'].apply(lambda x: len(str(x).split()))
        self.df['nb_phrases'] = self.df['texte'].apply(lambda x: str(x).count('.'))
        self.df['nb_chars'] = self.df['texte'].apply(lambda x: len(str(x)))
        
        print(f"\n Statistiques textuelles :")
        print(f"   Moyenne de mots par document : {self.df['nb_mots'].mean():.1f}")
        print(f"   Moyenne de phrases par document : {self.df['nb_phrases'].mean():.1f}")
        print(f"   Moyenne de caractères par document : {self.df['nb_chars'].mean():.1f}")
        
        print(f"\n   Min mots : {self.df['nb_mots'].min()}")
        print(f"   Max mots : {self.df['nb_mots'].max()}")
    
    
    def to_text(self):
        """
        Concatène tous les textes du corpus en une seule chaîne
        
        Returns:
            str: Chaîne unique contenant tous les documents
        """
        if self.df is None or self.df.empty:
            print(" Corpus vide")
            return ""
        
        texte_complet = " ".join(self.df['texte'].tolist())
        print(f" Texte complet créé : {len(texte_complet)} caractères")
        return texte_complet
    
    
    def show_sample(self, n=5):
        """
        Affiche un échantillon de documents
        
        Args:
            n (int): Nombre de documents à afficher
        """
        if self.df is None or self.df.empty:
            print(" Corpus vide")
            return
        
        print(f"\n📄 Échantillon de {min(n, len(self.df))} documents :\n")
        
        for idx, row in self.df.head(n).iterrows():
            print(f"{'='*70}")
            print(f"Doc {row['id']} - Source: {row['source']}")
            print(f"Texte: {row['texte'][:200]}...")
            print()
    
    
    def __len__(self):
        """Retourne le nombre de documents"""
        return len(self.df) if self.df is not None else 0
    
    
    def __repr__(self):
        """Représentation du corpus"""
        return f"Corpus({len(self)} documents)"
