import pygame, random

from files.animatronics.animatronic_base import Animatronic

class Mangle(Animatronic):
    def __init__(self, App, activated:int=True):
        super().__init__(activated, 12, App.animations.mangle_jump, 12)
        self.time_to_scare = random.randint(12000, 30000)

    def movement(self, App):
        match self.locationId:
            case 12:
                if pygame.time.get_ticks() - self.timer > 5000:
                    self.change_location_id(App, 11, force=True)

            case 11:
                if pygame.time.get_ticks() - self.timer > 5000:
                    self.change_location_id(App, 10, force=True)

            case 10:
                if pygame.time.get_ticks() - self.timer > 5000:
                    self.change_location_id(App, 7, force=True)

            case 7:
                if pygame.time.get_ticks() - self.timer > 5000:
                    self.change_location_id(App, 1, force=True)

            case 1: # rare
                if pygame.time.get_ticks() - self.timer > 5000:
                    self.change_location_id(App, 2, force=True)

            case 2:
                if pygame.time.get_ticks() - self.timer > 5000:
                    self.change_location_id(App, 6, force=True)

            case 6:
                if pygame.time.get_ticks() - self.timer > 5000:
                    self.change_location_id(App, 101)

            case 101:
                if pygame.time.get_ticks() - self.timer > 5000:
                    self.change_location_id(App, 102)

            case 102:
                if pygame.time.get_ticks() - self.timer > 7000 and App.objects.open_monitor_button.inCamera:
                    self.change_location_id(App, -1, force=True)

                if App.objects.mask_button.inMask:
                    self.time_with_mask += 1
                if self.time_with_mask >= self.time_with_mask_goal:
                    self.change_location_id(App, 12)

            case -1:
                if pygame.time.get_ticks() - self.timer > self.time_to_scare and App.objects.open_monitor_button.inCamera:
                    self.jumpscare(App)