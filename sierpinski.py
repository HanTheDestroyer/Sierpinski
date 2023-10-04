import sys
import pygame as pg
import numpy as np


class Simulation:
    def __init__(self, shapes):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(screen_size)
        self.screen.fill(pg.Color('black'))
        self.shapes = shapes
        self.is_increasing_generations = True
        self.generation_counter = -1

    def update(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.logic()
            self.screen.fill(pg.Color('black'))
            self.draw()
            pg.display.update()
            self.clock.tick(3)

    def logic(self):
        if self.is_increasing_generations:
            self.generation_counter += 1
            if self.generation_counter >= max_generations:
                self.is_increasing_generations = False
        else:
            self.generation_counter -= 1
            if self.generation_counter <= 0:
                self.is_increasing_generations = True

    def draw(self):
        for shape in self.shapes:
            shape.draw(self.screen, self.generation_counter)


class SierpinskiTriangle:
    def __init__(self, vertices, generation=0):
        self.vertices = vertices
        self.generation = generation
        self.children = []
        if self.generation < max_generations:
            vertex0 = (self.vertices[1] + self.vertices[2]) / 2
            vertex1 = (self.vertices[0] + self.vertices[2]) / 2
            vertex2 = (self.vertices[0] + self.vertices[1]) / 2
            child0 = SierpinskiTriangle(np.array([vertex1, vertex0, self.vertices[2]]), generation=self.generation+1)
            child1 = SierpinskiTriangle(np.array([self.vertices[0], vertex2, vertex1]), generation=self.generation+1)
            child2 = SierpinskiTriangle(np.array([vertex2, self.vertices[1], vertex0]), generation=self.generation+1)
            self.children = [child0, child1, child2]

    def draw(self, screen, target_generation):

        if self.generation <= target_generation:
            pg.draw.line(screen, pg.Color('white'), self.vertices[0], self.vertices[1])
            pg.draw.line(screen, pg.Color('white'), self.vertices[0], self.vertices[2])
            pg.draw.line(screen, pg.Color('white'), self.vertices[1], self.vertices[2])
            if self.children:
                for child in self.children:
                    child.draw(screen, target_generation)


class SierpinskiCarpet:
    def __init__(self, vertices, generation=0):
        self.vertices = vertices
        self.generation = generation
        self.children = []
        self.s = []
        if self.generation < max_generations:
            height_vector = self.vertices[1] - self.vertices[0]
            width_vector = self.vertices[2] - self.vertices[1]
            k = np.zeros([8, 2])
            s = np.zeros([4, 2])

            k[0] = self.vertices[0] + height_vector / 3
            k[1] = self.vertices[0] + 2 * height_vector / 3
            k[2] = self.vertices[1] + width_vector / 3
            k[3] = self.vertices[1] + 2 * width_vector / 3

            k[4] = self.vertices[3] + 2 * height_vector / 3
            k[5] = self.vertices[3] + height_vector / 3
            k[6] = self.vertices[0] + 2 * width_vector / 3
            k[7] = self.vertices[0] + width_vector / 3

            s[0] = self.vertices[0] + height_vector / 3 + width_vector / 3
            s[1] = self.vertices[0] + 2 * height_vector / 3 + width_vector / 3
            s[2] = self.vertices[0] + 2 * height_vector / 3 + 2 * width_vector / 3
            s[3] = self.vertices[0] + height_vector / 3 + 2 * width_vector / 3

            child0 = SierpinskiCarpet(np.array([self.vertices[0], k[0], s[0], k[7]]), generation=self.generation+1)
            child1 = SierpinskiCarpet(np.array([k[0], k[1], s[1], s[0]]), generation=self.generation+1)
            child2 = SierpinskiCarpet(np.array([k[1], self.vertices[1], k[2], s[1]]), generation=self.generation+1)
            child3 = SierpinskiCarpet(np.array([s[1], k[2], k[3], s[2]]), generation=self.generation+1)
            child4 = SierpinskiCarpet(np.array([s[2], k[3], self.vertices[2], k[4]]), generation=self.generation+1)
            child5 = SierpinskiCarpet(np.array([s[3], s[2], k[4], k[5]]), generation=self.generation+1)
            child6 = SierpinskiCarpet(np.array([k[6], s[3], k[5], self.vertices[3]]), generation=self.generation+1)
            child7 = SierpinskiCarpet(np.array([k[7], s[0], s[3], k[6]]), generation=self.generation+1)

            self.children = [child0, child1, child2, child3, child4, child5, child6, child7]
            self.s = s

    def draw(self, screen, target_generation):
        if self.generation == 0:
            pg.draw.line(screen, pg.Color('white'), self.vertices[0], self.vertices[1])
            pg.draw.line(screen, pg.Color('white'), self.vertices[1], self.vertices[2])
            pg.draw.line(screen, pg.Color('white'), self.vertices[2], self.vertices[3])
            pg.draw.line(screen, pg.Color('white'), self.vertices[3], self.vertices[0])
        if self.generation < target_generation:
            pg.draw.line(screen, pg.Color('white'), self.s[0], self.s[1])
            pg.draw.line(screen, pg.Color('white'), self.s[1], self.s[2])
            pg.draw.line(screen, pg.Color('white'), self.s[2], self.s[3])
            pg.draw.line(screen, pg.Color('white'), self.s[3], self.s[0])
            if self.children:
                for child in self.children:
                    child.draw(screen, target_generation)


if __name__ == '__main__':
    screen_size = np.array([640, 640])
    max_generations = 5
    triangle1 = SierpinskiTriangle(np.array([[100, 500], [500, 500], [300, 154]]))
    carpet1 = SierpinskiCarpet(np.array([[100, 500], [100, 100], [500, 100], [500, 500]]))
    simulation = Simulation([carpet1])
    simulation.update()
