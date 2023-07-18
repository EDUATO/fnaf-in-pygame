import pygame
from abc import ABC

class Animatronic(ABC):
    def __init__(self, activated:bool, locationId:int, jumpscare_animation:list):
        """
        locationId:
            - From 1 to 12 are room locations
            - Greater that 100 are office locations
            101: Office hallway
            102: Right vent
            103: Left vent
            104: In Office Desk

        """


        self.locationId = locationId
        self.secondPositionId = 1
        self.activated = activated
        self.timer = pygame.time.get_ticks()
        self.changing_position:bool = False
        self.action_error:bool = False # When the animatronic is moving
        self._previous_movement = [] # The changing and the location
        self._jumpscare:bool = False
        self.jumpscare_animation = jumpscare_animation
        self._gameOver = False
        self.occupied_camera_time = 5000
        self.inOfficeDesk:bool = False # If the animatronic is in office to attack
        self.name_id:str = "-"
        self._prepare_to_jumpscare = False # Get a random timer and jumpscare the player
        self.time_with_mask_goal = 120
        self.time_with_mask = 0

    def update(self, App):
        if self.activated:
            if self._jumpscare:
                self.jumpscare_animation.update(App.surface)
                App.objects.open_monitor_button.quitting_camera = True
                App.objects.mask_button.quitting_mask = True
                if self.jumpscare_animation.sprite_num == len(self.jumpscare_animation.sprites) - 1:
                    self._gameOver = True
                    
            else:
                if self._prepare_to_jumpscare:
                    self.jumpscare_time(App)
                else:
                    if not self.changing_position:
                        self.movement(App)
                    else:
                        self.change_location_id(App, self._previous_movement[0], self._previous_movement[2])

            # Static to camera
            if self.changing_position:
                self._change_occupied_camera_or_office(App, True)
            elif not self.changing_position and self.action_error:
                self._change_occupied_camera_or_office(App, False)
                self.action_error = False
            
    def jumpscare_time(self, App):
        self.change_location_id(App, -1)
        if pygame.time.get_ticks() - self.timer > 0 and App.objects.open_monitor_button.inCamera:
            self.jumpscare()

    def _change_occupied_camera_or_office(self, App, state:bool):
        """ Change occupied camera and office """
        # If previous_movement is below 100 its a camera
        if self._previous_movement[0] -1 < 100:
            App.objects.camera.occupied_camera[self._previous_movement[0] - 1] = state # Camera
        else:
            App.objects.office.occupied_office[self._previous_movement[0] - 101] = state # Office

        if self._previous_movement[1] -1 < 100:
            App.objects.camera.occupied_camera[self._previous_movement[1] - 1] = state # Camera
        else:
            App.objects.office.occupied_office[self._previous_movement[1] - 101] = state # Office

    def movement(self, App):
        pass

    def change_location_id(self ,App, room_location:int, secondPositionId=1):
            changing_to_location = room_location
            changing_to_position = secondPositionId
            self._previous_movement = [changing_to_location, self.locationId, changing_to_position, self.secondPositionId]

            if changing_to_location == 104 or self.change_location_id == -1:
                self._wait_movement_time(force=True)
            else:
                self._wait_movement_time()
            if App.objects.Animatronics.every_animatrionic_position[room_location] == []: # Is empty
                if not self.changing_position:
                    self.locationId = changing_to_location
                    self.secondPositionId = changing_to_position
                    changing_to_location = -1
                    self.time_with_mask = 0
            else:
                # We need more time !
                self.timer = pygame.time.get_ticks()

    def _wait_movement_time(self, force=False):
        """ Will provoke the static while moving """
        if not self.changing_position:
            self.timer = pygame.time.get_ticks()
            self.changing_position = True
            self.action_error = True

        elif self.changing_position:
            if not force:
                time_to_change = self.occupied_camera_time
            else:
                time_to_change = 0

            if pygame.time.get_ticks() - self.timer > time_to_change:
                self.changing_position = False
                self.timer = pygame.time.get_ticks()

    def isGameOver(self):
        return self._gameOver

    def get_prev_movement(self):
        if self.action_error and self.changing_position == False:
            self.prev_copy = self._previous_movement
            self._previous_movement = [-1, -1]
            self.action_error = False
            return self.prev_copy
        return [-1 , -1]

    def jumpscare(self):
        self._jumpscare = True

    def prepare_to_jumpscare(self):
        self.timer = pygame.time.get_ticks()
        self._prepare_to_jumpscare = True