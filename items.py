class Objet:
    """Classe de base pour les objets utilisables"""
    
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description
    
    def utiliser(self, pokemon):
        """Méthode à surcharger dans les sous-classes"""
        pass
    
    def __str__(self):
        return f"{self.nom}: {self.description}"


class Potion(Objet):
    """Potion qui restaure des PV"""
    
    def __init__(self):
        super().__init__("Potion", "Restaure 50 PV")
    
    def utiliser(self, pokemon):
        """Utilise la potion sur un Pokémon"""
        soin = min(50, pokemon.pv_max - pokemon.pv)
        pokemon.pv += soin
        return f"{pokemon.nom} utilise une Potion et récupère {soin} PV!"


class BoostAttaque(Objet):
    """Objet qui augmente temporairement la force"""
    
    def __init__(self):
        super().__init__("Boost d'Attaque", "Augmente la force de 5 points")
    
    def utiliser(self, pokemon):
        """Utilise le boost sur un Pokémon"""
        pokemon.force += 5
        return f"{pokemon.nom} utilise un Boost d'Attaque et gagne 5 points de force!"


class BaieOran(Objet):
    """Baie qui restaure des PV et soigne les statuts"""
    
    def __init__(self):
        super().__init__("Baie Oran", "Restaure 20 PV et soigne les statuts")
    
    def utiliser(self, pokemon):
        """Utilise la baie sur un Pokémon"""
        soin = min(20, pokemon.pv_max - pokemon.pv)
        pokemon.pv += soin
        # Réinitialiser les statuts (dans une implémentation plus complète)
        return f"{pokemon.nom} mange une Baie Oran et récupère {soin} PV!"