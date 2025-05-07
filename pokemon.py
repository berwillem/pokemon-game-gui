from abc import ABC, abstractmethod
import random
from decorators import cooldown

class Pokemon(ABC):
    """Classe abstraite pour tous les Pokémon"""
    
    def __init__(self, nom, type_pokemon, pv=100, force=10, niveau=1):
        self.nom = nom
        self.type = type_pokemon
        self.niveau = niveau
        # Ajuster les stats en fonction du niveau
        self.pv_max = 100 + (niveau - 1) * 10
        self.pv = self.pv_max
        self.force = 10 + (niveau - 1) * 2
        self.cooldowns = {}
    
    def __str__(self):
        return f"{self.nom} (Type: {self.type}, PV: {self.pv}/{self.pv_max}, Force: {self.force}, Niveau: {self.niveau})"
    
    def attaquer(self, cible):
        """Attaque de base"""
        # Calculer les dégâts en fonction du type
        multiplicateur = 1.0
        
        # Avantages de type
        if (self.type == "Feu" and cible.type == "Plante") or \
           (self.type == "Eau" and cible.type == "Feu") or \
           (self.type == "Plante" and cible.type == "Eau"):
            multiplicateur = 1.5
            message = f"C'est super efficace! "
        else:
            message = ""
        
        degats = int(self.force * multiplicateur)
        cible.pv = max(0, cible.pv - degats)
        
        return f"{message}{self.nom} attaque {cible.nom} et inflige {degats} dégâts!"
    
    @abstractmethod
    def attaque_speciale(self, cible):
        """Attaque spéciale, à implémenter dans les sous-classes"""
        pass
    
    @cooldown(3)
    def soigner(self):
        """Soigne le Pokémon"""
        soin = int(self.pv_max * 0.3)
        self.pv = min(self.pv_max, self.pv + soin)
        return f"{self.nom} se soigne de {soin} PV!"
    
    def gagner(self):
        """Gagne un combat"""
        self.niveau += 1
        self.pv_max += 10
        self.force += 2
        self.pv = self.pv_max
        return f"{self.nom} gagne un niveau! Niveau actuel: {self.niveau}"
    
    def afficher_statistiques(self):
        """Affiche les statistiques du Pokémon"""
        return {
            "nom": self.nom,
            "type": self.type,
            "niveau": self.niveau,
            "pv": self.pv,
            "pv_max": self.pv_max,
            "force": self.force
        }
    
    def est_vivant(self):
        """Vérifie si le Pokémon est encore en vie"""
        return self.pv > 0


class PokemonFeu(Pokemon):
    """Classe pour les Pokémon de type Feu"""
    
    def __init__(self, nom, pv=100, force=10, niveau=1):
        super().__init__(nom, "Feu", pv, force, niveau)
    
    @cooldown(4)
    def attaque_speciale(self, cible):
        """Attaque spéciale de type Feu: Lance-Flammes"""
        multiplicateur = 1.5
        if cible.type == "Plante":
            multiplicateur = 2.0
        
        degats = int(self.force * multiplicateur * 1.5)  # 50% plus fort qu'une attaque normale
        cible.pv = max(0, cible.pv - degats)
        
        # Chance de brûlure (réduit la force de la cible)
        if random.random() < 0.3:
            cible.force = max(5, cible.force - 2)
            return f"{self.nom} utilise Lance-Flammes sur {cible.nom} et inflige {degats} dégâts! {cible.nom} est brûlé et perd de la force!"
        
        return f"{self.nom} utilise Lance-Flammes sur {cible.nom} et inflige {degats} dégâts!"


class PokemonEau(Pokemon):
    """Classe pour les Pokémon de type Eau"""
    
    def __init__(self, nom, pv=100, force=10, niveau=1):
        super().__init__(nom, "Eau", pv, force, niveau)
    
    @cooldown(4)
    def attaque_speciale(self, cible):
        """Attaque spéciale de type Eau: Hydrocanon"""
        multiplicateur = 1.5
        if cible.type == "Feu":
            multiplicateur = 2.0
        
        degats = int(self.force * multiplicateur * 1.5)
        cible.pv = max(0, cible.pv - degats)
        
        # Chance de réduire la précision (simulé par une réduction de force)
        if random.random() < 0.3:
            self.pv = min(self.pv_max, self.pv + int(degats * 0.2))
            return f"{self.nom} utilise Hydrocanon sur {cible.nom} et inflige {degats} dégâts! {self.nom} récupère {int(degats * 0.2)} PV!"
        
        return f"{self.nom} utilise Hydrocanon sur {cible.nom} et inflige {degats} dégâts!"


class PokemonPlante(Pokemon):
    """Classe pour les Pokémon de type Plante"""
    
    def __init__(self, nom, pv=100, force=10, niveau=1):
        super().__init__(nom, "Plante", pv, force, niveau)
    
    @cooldown(4)
    def attaque_speciale(self, cible):
        """Attaque spéciale de type Plante: Fouet Lianes"""
        multiplicateur = 1.5
        if cible.type == "Eau":
            multiplicateur = 2.0
        
        degats = int(self.force * multiplicateur * 1.5)
        cible.pv = max(0, cible.pv - degats)
        
        # Chance de vol de vie
        vol_vie = int(degats * 0.3)
        self.pv = min(self.pv_max, self.pv + vol_vie)
        
        return f"{self.nom} utilise Fouet Lianes sur {cible.nom} et inflige {degats} dégâts! {self.nom} absorbe {vol_vie} PV!"