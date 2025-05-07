import pygame
import sys

class GUI:
    """Classe pour gérer l'interface graphique du jeu"""
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_large = pygame.font.SysFont('Arial', 32)
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)
        
        # Couleurs
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
        # Couleurs pour les types de Pokémon
        self.TYPE_COLORS = {
            "Feu": (255, 69, 0),    # Rouge-orange
            "Eau": (30, 144, 255),   # Bleu
            "Plante": (50, 205, 50)  # Vert
        }
        
        # Charger les images (utiliser des rectangles colorés pour l'instant)
        self.pokemon_images = {
            "Feu": pygame.Surface((100, 100)),
            "Eau": pygame.Surface((100, 100)),
            "Plante": pygame.Surface((100, 100))
        }
        
        self.pokemon_images["Feu"].fill(self.TYPE_COLORS["Feu"])
        self.pokemon_images["Eau"].fill(self.TYPE_COLORS["Eau"])
        self.pokemon_images["Plante"].fill(self.TYPE_COLORS["Plante"])
    
    def draw_text(self, text, font, color, x, y, centered=False):
        """Dessine du texte à l'écran"""
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_button(self, text, x, y, width, height, color, hover_color):
        """Dessine un bouton et renvoie True s'il est cliqué"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(x, y, width, height)
        
        # Vérifier si la souris est sur le bouton
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, button_rect)
            if pygame.mouse.get_pressed()[0]:  # Clic gauche
                pygame.time.delay(200)  # Petit délai pour éviter les doubles clics
                return True
        else:
            pygame.draw.rect(self.screen, color, button_rect)
        
        # Dessiner le texte du bouton
        text_surf = self.font_medium.render(text, True, self.BLACK)
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return False
    
    def display_menu(self, title, options):
        """Affiche un menu avec des options et renvoie l'option sélectionnée"""
        selected = None
        
        while selected is None:
            self.screen.fill(self.WHITE)
            
            # Titre
            self.draw_text(title, self.font_large, self.BLACK, self.width // 2, 50, True)
            
            # Options
            button_height = 60
            button_width = 400
            button_y_start = 150
            button_spacing = 20
            
            for i, option in enumerate(options):
                y_pos = button_y_start + i * (button_height + button_spacing)
                if self.draw_button(option, (self.width - button_width) // 2, y_pos, 
                                   button_width, button_height, self.BLUE, (100, 100, 255)):
                    selected = i
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()
        
        return selected
    
    def create_pokemon_interface(self, create_function, title="Créer votre Pokémon"):
        """Interface pour créer un Pokémon"""
        nom = ""
        type_selected = None
        pokemon_types = ["Feu", "Eau", "Plante"]
        
        input_active = True
        
        while True:
            self.screen.fill(self.WHITE)
            
            # Titre
            self.draw_text(title, self.font_large, self.BLACK, self.width // 2, 50, True)
            
            # Champ de saisie du nom
            self.draw_text("Nom du Pokémon:", self.font_medium, self.BLACK, 200, 150)
            pygame.draw.rect(self.screen, (200, 200, 200), (200, 180, 400, 40))
            self.draw_text(nom, self.font_medium, self.BLACK, 210, 190)
            
            # Sélection du type
            self.draw_text("Type du Pokémon:", self.font_medium, self.BLACK, 200, 250)
            
            for i, type_name in enumerate(pokemon_types):
                x_pos = 200 + i * 150
                color = self.TYPE_COLORS[type_name]
                hover_color = tuple(min(c + 50, 255) for c in color)
                
                if self.draw_button(type_name, x_pos, 280, 120, 40, color, hover_color):
                    type_selected = type_name
            
            # Afficher le type sélectionné
            if type_selected:
                self.draw_text(f"Type sélectionné: {type_selected}", self.font_medium, 
                              self.TYPE_COLORS[type_selected], 200, 350)
                
                # Bouton de confirmation
                if self.draw_button("Créer Pokémon", 300, 400, 200, 50, self.GREEN, (100, 255, 100)):
                    if nom.strip() != "":
                        return create_function(nom, type_selected)
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            nom = nom[:-1]
                        else:
                            # Limiter la longueur du nom
                            if len(nom) < 15:
                                nom += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    input_active = True
            
            pygame.display.flip()
    
    def battle_interface(self, battle):
        """Interface de combat"""
        clock = pygame.time.Clock()
        
        while True:
            self.screen.fill(self.WHITE)
            
            # Vérifier si le combat est terminé
            if battle.is_battle_over():
                winner = battle.get_winner()
                if winner == battle.pokemon1:
                    return "victory"
                else:
                    return "defeat"
            
            # Afficher les Pokémon
            self.draw_pokemon_info(battle.pokemon1, 50, 350)
            self.draw_pokemon_info(battle.pokemon2, 550, 150)
            
            # Afficher le journal de combat
            self.draw_battle_log(battle.battle_log, 50, 50, 700, 100)
            
            # Afficher les actions disponibles
            if battle.current_turn == 1:  # Tour du joueur
                actions = [
                    ("Attaque", lambda: battle.attack()),
                    ("Attaque Spéciale", lambda: battle.special_attack()),
                    ("Soigner", lambda: battle.heal()),
                    ("Utiliser Potion", lambda: battle.use_item(0)),
                    ("Utiliser Boost", lambda: battle.use_item(1))
                ]
                
                for i, (action_text, action_func) in enumerate(actions):
                    x_pos = 50 + (i % 3) * 250
                    y_pos = 450 + (i // 3) * 60
                    
                    if self.draw_button(action_text, x_pos, y_pos, 200, 50, self.BLUE, (100, 100, 255)):
                        try:
                            action_func()
                        except Exception as e:
                            print(f"Erreur: {e}")
            else:
                # Tour de l'IA
                battle.ai_turn()
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
            
            pygame.display.flip()
            clock.tick(30)
    
    def draw_pokemon_info(self, pokemon, x, y):
        """Affiche les informations d'un Pokémon"""
        # Image du Pokémon
        pokemon_img = self.pokemon_images[pokemon.type]
        self.screen.blit(pokemon_img, (x, y))
        
        # Informations
        info_x = x + 120
        self.draw_text(pokemon.nom, self.font_medium, self.BLACK, info_x, y)
        self.draw_text(f"Type: {pokemon.type}", self.font_small, self.TYPE_COLORS[pokemon.type], info_x, y + 30)
        self.draw_text(f"Niveau: {pokemon.niveau}", self.font_small, self.BLACK, info_x, y + 50)
        
        # Barre de vie
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(self.screen, self.RED, (info_x, y + 80, bar_width, bar_height))
        health_width = max(0, int(bar_width * (pokemon.pv / pokemon.pv_max)))
        pygame.draw.rect(self.screen, self.GREEN, (info_x, y + 80, health_width, bar_height))
        
        self.draw_text(f"{pokemon.pv}/{pokemon.pv_max} PV", self.font_small, self.BLACK, info_x + bar_width // 2, y + 80 + bar_height // 2, True)
    
    def draw_battle_log(self, log, x, y, width, height):
        """Affiche le journal de combat"""
        pygame.draw.rect(self.screen, (240, 240, 240), (x, y, width, height))
        pygame.draw.rect(self.screen, self.BLACK, (x, y, width, height), 2)
        
        for i, message in enumerate(log):
            self.draw_text(message, self.font_small, self.BLACK, x + 10, y + 10 + i * 20)
    
    def display_statistics(self, stats):
        """Affiche les statistiques du joueur"""
        waiting = True
        
        while waiting:
            self.screen.fill(self.WHITE)
            
            # Titre
            self.draw_text("Statistiques du Joueur", self.font_large, self.BLACK, self.width // 2, 50, True)
            
            # Statistiques
            y_pos = 150
            for key, value in stats.items():
                self.draw_text(f"{key.capitalize()}: {value}", self.font_medium, self.BLACK, 300, y_pos)
                y_pos += 50
            
            # Bouton retour
            if self.draw_button("Retour au menu", 300, 400, 200, 50, self.BLUE, (100, 100, 255)):
                waiting = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()
    
    def display_battle_result(self, result):
        """Affiche le résultat d'une bataille"""
        waiting = True
        
        while waiting:
            self.screen.fill(self.WHITE)
            
            if result == "victory":
                self.draw_text("Victoire !", self.font_large, self.GREEN, self.width // 2, 200, True)
                message = "Félicitations ! Votre Pokémon a gagné le combat."
            else:
                self.draw_text("Défaite...", self.font_large, self.RED, self.width // 2, 200, True)
                message = "Votre Pokémon a perdu le combat. Entraînez-vous davantage !"
            
            self.draw_text(message, self.font_medium, self.BLACK, self.width // 2, 250, True)
            
            # Bouton retour
            if self.draw_button("Retour au menu", 300, 350, 200, 50, self.BLUE, (100, 100, 255)):
                waiting = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()