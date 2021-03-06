import pygame

class Spritesheet(object):
    def __init__(self, filename, width, height, max_img_num=None):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.width = width
        self.height = height

        if max_img_num is not None:
            self.max_img_num = max_img_num
        else:
            self.max_img_num = (self.sheet.get_width()/self.width) * (self.sheet.get_height()/self.height)

        assert self.sheet.get_width() % self.width == 0
        assert self.sheet.get_height() % self.height == 0

        # Load a specific image from a specific rectangle

    def image_at(self, rectangle):
        # "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def get_image(self, img_x, img_y):
        '''
        Returns the nth image in the spritesheet
        :param img_num: number image in spritesheet
        :type img_num: int
        :return:
        '''


        chosen_img = self.image_at((img_x*self.width, img_y*self.height, self.width, self.height))

        return chosen_img # type: pygame.Surface

    def strip_image_at(self, rectangle):
        # "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        rect_image_key = pygame.Rect(0, 0, 32, 32)
        image_for_key = pygame.Surface(rect_image_key.size).convert()
        image_for_key.blit(self.sheet, (0, 0), rect)
        colorkey = image_for_key.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def get_strip(self, img_y):

        chosen_img = self.strip_image_at((0, img_y * 32, self.width, 32))

        return chosen_img  # type: pygame.Surface