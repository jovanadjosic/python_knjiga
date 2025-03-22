import pygame
import sys
import pygame.font
from time import sleep
from pygame.sprite import Sprite

class Rect(Sprite):
    """A class to represent a single rectangle in the fleet."""
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.rect_color

        # TODO Jovana, udari razmak posle tarabe dole i uradi to sa svim komentarima
        # TODO Napravi direktorijum 14.2 i tamo podeli ovaj fajl u jedan fajl po klasi
        #Create a rect at (0,0) and then set correct position.
        # TODO Udari razmak posle svakog zareza dole i u svim ostalim linijama
        self.rect=pygame.Rect(0,0,self.settings.rect_width,self.settings.rect_height)
        self.rect.midright=ai_game.screen.get_rect().midright

        #Store the rect's position as a decimal value.
        # TODO Stavi razmak pre i posle jednako i u svim ostalim linijama
        self.y=float(self.rect.y)
        self.direction=1


    def update(self):
        """Move the rect up and down on the screen."""
        #Update the exact position of the rect.
        self.y+=self.settings.rect_speed*self.direction

        # Reverse direction if it hits the top or bottom of the screen.
        if self.y <= 0 or self.y+self.rect.height >= self.screen.get_rect().height:
            self.direction *= -1

        #Update the rect position.
        self.rect.y=self.y

    
    def draw_rect(self):
        """Draw the rect to the screen."""
        pygame.draw.rect(self.screen,self.color,self.rect)

class Settings:
    """A class to store all settings for 14.2."""

    def __init__(self):
        """Initialize the game's settings."""
        #Screen settings
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)
        #Ship settings
        self.ship_speed=1.5
        self.ship_limit=3
        #Bullet settings
        self.bullet_speed=2.5
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(0,255,0)
        self.bullets_allowed=3
        #Rect settings
        self.rect_width = 50
        self.rect_height = 200
        self.rect_color = (255, 0, 0)
        self.rect_speed = 2.0


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

class Ship:
    """A class to manage the ship."""

    def __init__(self,ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect.
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen.
        self.rect.midleft = self.screen_rect.midleft

        #Store a float for the ship's horizontal position.
        self.y=float(self.rect.y)

        #Movement flag;start with a ship that is not moving.
        self.moving_up=False
        self.moving_down=False

    def update(self):
        """Update the ship's position based on the movement flag."""
        #Update the ship's x value, not the rect.
        if self.moving_up and self.rect.top>0:
            self.y-=self.settings.ship_speed
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.y+=self.settings.ship_speed
        #Update rect object from self.x.
        self.rect.y=self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midleft=self.screen_rect.midleft
        self.y=float(self.rect.y)

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left=self.settings.ship_limit

class Button:
    """A class to build buttons for the game."""

    def __init__(self,ai_game,msg):
        """Initialize button attributes."""
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()

        #Set the dimensions and properties of the button.
        self.width,self.height=200,50
        self.button_color=(0,135,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)

        #Build the button's rect object and center it.
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center

        #The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

class TargetPractice:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings=Settings()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("TargetPractice")
        #Create an instance to store game statistics.
        self.stats=GameStats(self)
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.rects=pygame.sprite.Group()
        self._create_rect()
        #Set the background color.
        self.bg_color=self.settings.bg_color
        #Make the Play button.
        self.play_button=Button(self,"Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self.rects.update()
            self._update_screen()
            self.clock.tick(60)

            #Make the most recently drawn screen visible.
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active=True
            #Get rid of any remaining aliens and bullets.
            self.bullets.empty()
            #Create a new fleet and center the ship.
            self.ship.center_ship()
            #Hide the mouse cursor.
            pygame.mouse.set_visible(False)


    def check_keydown_events(self,event):
        """Respond to keypresses."""
        if event.key==pygame.K_UP:
            self.ship.moving_up=True
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
        elif event.key==pygame.K_p:
            if not self.stats.game_active:
                #Reset the game statistics.
                self.stats.reset_stats()
                self.stats.game_active=True
                #Get rid of any remaining aliens and bullets.
                self.bullets.empty()
                #Create a new fleet and center the ship.
                self.ship.center_ship()
                #Hide the mouse cursor.
                pygame.mouse.set_visible(False)

    def check_keyup_events(self,event):
        if event.key==pygame.K_UP:
            self.ship.moving_up=False
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet positions.
        self.bullets.update()
        #Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.top<=0:
                self.bullets.remove(bullet)
        self._check_bullet_rect_collision()
    
    def _check_bullet_rect_collision(self):
        """Update position of bullets and get rid of old bullets."""
        collisions=pygame.sprite.groupcollide(self.bullets,self.rects,True,True)
        # Check for bullet-rect collisions.
        # If a collision occurs, create a new rectangle.
        if collisions:
            self._create_rect()

        # Check if bullets missed the rectangles.
        for bullet in self.bullets.copy():
            missed = True
            for rect in self.rects:
                if bullet.rect.colliderect(rect.rect):  # Check collision with each rect
                    missed = False
                    break
            if missed:
                self.bullets.remove(bullet)
                self.stats.ships_left -= 1
                if self.stats.ships_left == 0:
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)


    def _create_rect(self):
        """Create a new rectangle."""
        new_rect = Rect(self)
        self.rects.add(new_rect)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        for rect in self.rects.sprites():
            rect.draw_rect()
        #Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == "__main__":
    #Make a game instance, and run the game.
    tp = TargetPractice()
    tp.run_game()