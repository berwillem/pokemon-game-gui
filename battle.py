import random
from items import Potion, BoostAttaque

class Battle:
    """Classe gérant les combats entre Pokémon"""
    
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1  # Pokémon du joueur 1
        self.pokemon2 = pokemon2  # Pokémon du joueur 2 ou sauvage
        self.current_turn = 1     # 1 pour joueur 1, 2 pour joueur 2
        self.tour = 1             # Compteur de tours
        self.battle_log = []      # Journal de combat
        self.items = [Potion(), BoostAttaque()]  # Objets disponibles
        
    def log(self, message):
        """Ajoute un message au journal de combat"""
        self.battle_log.append(message)
        if len(self.battle_log) > 10:  # Garder seulement les 10 derniers messages
            self.battle_log.pop(0)
    
    def get_current_pokemon(self):
        """Renvoie le Pokémon dont c'est le tour"""
        return self.pokemon1 if self.current_turn == 1 else self.pokemon2
    
    def get_opponent_pokemon(self):
        """Renvoie le Pokémon adverse"""
        return self.pokemon2 if self.current_turn == 1 else self.pokemon1
    
    def attack(self):
        """Effectue une attaque normale"""
        attacker = self.get_current_pokemon()
        defender = self.get_opponent_pokemon()
        
        message = attacker.attaquer(defender)
        self.log(message)
        
        self.next_turn()
        return message
    
    def special_attack(self):
        """Effectue une attaque spéciale"""
        attacker = self.get_current_pokemon()
        defender = self.get_opponent_pokemon()
        
        try:
            message = attacker.attaque_speciale(defender)
            self.log(message)
        except Exception as e:
            self.log(f"Impossible d'utiliser l'attaque spéciale: {e}")
            return f"Impossible d'utiliser l'attaque spéciale: {e}"
        
        self.next_turn()
        return message
    
    def heal(self):
        """Soigne le Pokémon actuel"""
        pokemon = self.get_current_pokemon()
        
        try:
            message = pokemon.soigner()
            self.log(message)
        except Exception as e:
            self.log(f"Impossible de se soigner: {e}")
            return f"Impossible de se soigner: {e}"
        
        self.next_turn()
        return message
    
    def use_item(self, item_index):
        """Utilise un objet"""
        if 0 <= item_index < len(self.items):
            item = self.items[item_index]
            pokemon = self.get_current_pokemon()
            
            message = item.utiliser(pokemon)
            self.log(message)
            
            self.next_turn()
            return message
        else:
            return "Objet invalide"
    
    def next_turn(self):
        """Passe au tour suivant"""
        self.current_turn = 3 - self.current_turn  # Alterne entre 1 et 2
        
        if self.current_turn == 1:
            self.tour += 1
            self.log(f"--- Tour {self.tour} ---")
    
    def is_battle_over(self):
        """Vérifie si le combat est terminé"""
        return not self.pokemon1.est_vivant() or not self.pokemon2.est_vivant()
    
    def get_winner(self):
        """Renvoie le Pokémon gagnant"""
        if not self.pokemon1.est_vivant():
            return self.pokemon2
        elif not self.pokemon2.est_vivant():
            return self.pokemon1
        return None
    
    def ai_turn(self):
        """IA pour les Pokémon sauvages"""
        if self.current_turn == 2:  # Si c'est le tour du Pokémon sauvage
            pokemon = self.get_current_pokemon()
            opponent = self.get_opponent_pokemon()
            
            # Logique simple: soigner si PV bas, attaque spéciale si possible, sinon attaque normale
            if pokemon.pv < pokemon.pv_max * 0.3 and random.random() < 0.7:
                try:
                    return self.heal()
                except:
                    pass
            
            if random.random() < 0.4:
                try:
                    return self.special_attack()
                except:
                    pass
            
            return self.attack()
        
        return None