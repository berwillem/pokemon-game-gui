import functools

def cooldown(tours):
    """Décorateur pour empêcher l'utilisation d'une capacité pendant un certain nombre de tours"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Nom de la fonction comme identifiant pour le cooldown
            func_name = func.__name__
            
            # Vérifier si la fonction est en cooldown
            if func_name in self.cooldowns and self.cooldowns[func_name] > 0:
                remaining = self.cooldowns[func_name]
                raise Exception(f"Cette capacité sera disponible dans {remaining} tour(s)")
            
            # Exécuter la fonction
            result = func(self, *args, **kwargs)
            
            # Mettre en place le cooldown
            self.cooldowns[func_name] = tours
            
            return result
        return wrapper
    return decorator