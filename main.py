import pygame
import sys
from gui import GUI
from battle import Battle
from pokemon import PokemonFeu, PokemonEau, PokemonPlante
from player import PokemonJoueur
import os

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Jeu de Combat Pokémon")
        self.clock = pygame.time.Clock()
        self.gui = GUI(self.screen, self.width, self.height)
        self.running = True
        self.current_state = "main_menu"
        self.player_pokemon = None
        self.opponent_pokemon = None
        self.battle = None
        self.stats = self.load_statistics()
        
    def load_statistics(self):
        """Charge les statistiques depuis le fichier"""
        if not os.path.exists("statistiques.txt"):
            # Créer un fichier de statistiques par défaut
            with open("statistiques.txt", "w") as f:
                f.write("niveau:1\nvictoires:0\ndefaites:0")
            return {"niveau": 1, "victoires": 0, "defaites": 0}
        
        stats = {}
        try:
            with open("statistiques.txt", "r") as f:
                for line in f:
                    key, value = line.strip().split(":")
                    stats[key] = int(value)
            return stats
        except Exception as e:
            print(f"Erreur lors du chargement des statistiques: {e}")
            return {"niveau": 1, "victoires": 0, "defaites": 0}
    
    def save_statistics(self):
        """Sauvegarde les statistiques dans le fichier"""
        try:
            with open("statistiques.txt", "w") as f:
                for key, value in self.stats.items():
                    f.write(f"{key}:{value}\n")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des statistiques: {e}")
    
    def update_statistics(self, victory=False):
        """Met à jour les statistiques après une bataille"""
        if victory:
            self.stats["victoires"] += 1
            # Augmenter le niveau tous les 3 victoires
            if self.stats["victoires"] % 3 == 0:
                self.stats["niveau"] += 1
        else:
            self.stats["defaites"] += 1
        self.save_statistics()
    
    def main_menu(self):
        """Affiche le menu principal"""
        options = [
            "1. Joueur contre Pokémon sauvage",
            "2. Joueur contre Joueur (local)",
            "3. Voir les statistiques du joueur",
            "4. Quitter"
        ]
        selected = self.gui.display_menu("Menu Principal", options)
        
        if selected == 0:  # Joueur contre Pokémon sauvage
            self.current_state = "create_pokemon"
            self.battle_type = "wild"
        elif selected == 1:  # Joueur contre Joueur
            self.current_state = "create_pokemon"
            self.battle_type = "pvp"
        elif selected == 2:  # Voir les statistiques
            self.current_state = "show_stats"
        elif selected == 3:  # Quitter
            self.running = False
    
    def create_pokemon(self):
        """Interface pour créer un Pokémon"""
        if not self.player_pokemon:
            self.player_pokemon = self.gui.create_pokemon_interface(PokemonJoueur.creer_pokemon)
            
            if self.battle_type == "wild":
                # Générer un Pokémon sauvage
                self.opponent_pokemon = PokemonJoueur.generer_pokemon_sauvage(
                    min_level=max(1, self.stats["niveau"] - 1),
                    max_level=self.stats["niveau"] + 1
                )
                self.current_state = "battle"
                self.battle = Battle(self.player_pokemon, self.opponent_pokemon)
            else:  # PvP
                self.current_state = "create_opponent"
        
    def create_opponent(self):
        """Interface pour créer le Pokémon du deuxième joueur"""
        self.opponent_pokemon = self.gui.create_pokemon_interface(
            PokemonJoueur.creer_pokemon, 
            title="Créer le Pokémon du Joueur 2"
        )
        self.current_state = "battle"
        self.battle = Battle(self.player_pokemon, self.opponent_pokemon)
    
    def battle_screen(self):
        """Gère l'écran de bataille"""
        result = self.gui.battle_interface(self.battle)
        
        if result == "victory":
            self.update_statistics(victory=True)
            self.current_state = "battle_result"
            self.battle_result = "victory"
        elif result == "defeat":
            self.update_statistics(victory=False)
            self.current_state = "battle_result"
            self.battle_result = "defeat"
        elif result == "quit":
            self.current_state = "main_menu"
            self.player_pokemon = None
            self.opponent_pokemon = None
    
    def show_statistics(self):
        """Affiche les statistiques du joueur"""
        self.gui.display_statistics(self.stats)
        self.current_state = "main_menu"
    
    def battle_result_screen(self):
        """Affiche le résultat de la bataille"""
        self.gui.display_battle_result(self.battle_result)
        self.current_state = "main_menu"
        self.player_pokemon = None
        self.opponent_pokemon = None
    
    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            if self.current_state == "main_menu":
                self.main_menu()
            elif self.current_state == "create_pokemon":
                self.create_pokemon()
            elif self.current_state == "create_opponent":
                self.create_opponent()
            elif self.current_state == "battle":
                self.battle_screen()
            elif self.current_state == "show_stats":
                self.show_statistics()
            elif self.current_state == "battle_result":
                self.battle_result_screen()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()