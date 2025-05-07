import random
from pokemon import PokemonFeu, PokemonEau, PokemonPlante

class PokemonJoueur:
    """Classe pour gérer la création et génération de Pokémon"""
    
    @staticmethod
    def creer_pokemon(nom, type_pokemon, niveau=1):
        """Crée un Pokémon personnalisé"""
        if type_pokemon == "Feu":
            return PokemonFeu(nom, niveau=niveau)
        elif type_pokemon == "Eau":
            return PokemonEau(nom, niveau=niveau)
        elif type_pokemon == "Plante":
            return PokemonPlante(nom, niveau=niveau)
        else:
            raise ValueError(f"Type de Pokémon inconnu: {type_pokemon}")
    
    @staticmethod
    def generer_pokemon_sauvage(min_level=1, max_level=5):
        """Génère un Pokémon sauvage aléatoire"""
        noms_feu = ["Salamèche", "Goupix", "Caninos", "Ponyta", "Magby"]
        noms_eau = ["Carapuce", "Stari", "Magicarpe", "Krabby", "Poissirène"]
        noms_plante = ["Bulbizarre", "Germignon", "Tropius", "Tortipouss", "Vipélierre"]
        
        type_pokemon = random.choice(["Feu", "Eau", "Plante"])
        niveau = random.randint(min_level, max_level)
        
        if type_pokemon == "Feu":
            nom = random.choice(noms_feu)
            return PokemonFeu(nom, niveau=niveau)
        elif type_pokemon == "Eau":
            nom = random.choice(noms_eau)
            return PokemonEau(nom, niveau=niveau)
        else:  # Plante
            nom = random.choice(noms_plante)
            return PokemonPlante(nom, niveau=niveau)