import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings=Settings()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        #Create an instance to store game statistics.
        self.stats=GameStats(self)
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        #Set the background color.
        self.bg_color=self.settings.bg_color
        #Start Alien Invasion in an inactive state.
        self.stats.game_active=False
        #Make the Play button.
        #self.play_button=Button(self,"Play")

        self.easy_button=Button(self,"Easy")
        self.medium_button=Button(self,"Medium")
        self.hard_button=Button(self,"Hard")
        self.easy_button.rect.center=(self.screen.get_rect().centerx,self.screen.get_rect().centery-100)
        self.easy_button._prep_msg("Easy")
        self.medium_button.rect.center=(self.screen.get_rect().centerx,self.screen.get_rect().centery)
        self.medium_button._prep_msg("Medium")
        self.hard_button.rect.center=(self.screen.get_rect().centerx,self.screen.get_rect().centery+100)
        self.hard_button._prep_msg("Hard")
    
    def _check_difficulty_buttons(self,mouse_pos):
        """Check if a difficulty button is clicked and set the difficulty."""
        if self.easy_button.rect.collidepoint(mouse_pos):
            self.settings.set_easy_mode()
            self.stats.game_active=True
        elif self.medium_button.rect.collidepoint(mouse_pos):
            self.settings.set_medium_mode()
            self.stats.game_active=True
        elif self.easy_button.rect.collidepoint(mouse_pos):
            self.settings.set_hard_mode()
            self.stats.game_active=True

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
                #self._check_play_button(mouse_pos)
                if not self.stats.game_active:
                    self._check_difficulty_buttons(mouse_pos)

    
    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active=True
            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            #Hide the mouse cursor.
            pygame.mouse.set_visible(False)


    def check_keydown_events(self,event):
        """Respond to keypresses."""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
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
                self.aliens.empty()
                self.bullets.empty()
                #Create a new fleet and center the ship.
                self._create_fleet()
                self.ship.center_ship()
                #Hide the mouse cursor.
                pygame.mouse.set_visible(False)

    def check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False

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
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
    
    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        #Remove any bullets and aliens that have collided.
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            #Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions."""
        self._check_fleet_edges()
        self.aliens.update()
        #Check for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left>0:
            #Decrement ships_left.
            self.stats.ships_left-=1
            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            #Pause.
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        #Create an alien and keep track of the number of aliens until there is no room left.
        #Spacing between each alien is equal to one alien width and one alien height.
        alien=Alien(self)
        alien_width, alien_height=alien.rect.size
        current_x,current_y=alien_width,alien_height
        while current_y<(self.settings.screen_height-3*alien_height):
            while current_x<(self.settings.screen_width-2*alien_width):
                self._create_alien(current_x,current_y)
                current_x+=2*alien_width
            #Finished a row; reset x value, and increment y value.
            current_x=alien_width
            current_y+=2*alien_height

    def _create_alien(self,x_position,y_position):
            """Create an alien and place it in the fleet."""
            new_alien=Alien(self)
            new_alien.x=x_position
            new_alien.rect.x=x_position
            new_alien.rect.y=y_position
            self.aliens.add(new_alien)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=self.settings.screen_height:
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
        pygame.display.flip()

if __name__ == "__main__":
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
   