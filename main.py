import pygame as pg

import matplotlib as mpl
import numpy as np



class Button:
    def __init__(self, screen, left, top, width, height, text="", func=None):
        self.rect = pg.Rect(left, top, width, height)
        self.screen = screen
        self.text = text
        self.func = func

    def draw(self):
        pg.draw.rect(self.screen, (0, 0, 0), self.rect, 1)
        if self.text:
            self.screen.blit(pg.font.SysFont('Arial', self.rect.height//3).render(self.text, False, (0,0,0)), (self.rect.x + 2, self.rect.y + self.rect.height//3))

    def clicked(self):
        x,y = pg.mouse.get_pos()
        return x >= self.rect.x and x <= self.rect.x + self.rect.width and y >= self.rect.y and y <= self.rect.y + self.rect.height


class Vector:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.pos = (p1.pos[0] - p2.pos[0], p1.pos[1] - p2.pos[1])

    def scalar_multiplication(self, a):
        new_vector = Vector(self.p1, self.p2)
        new_vector.pos = (new_vector.pos[0] * a, new_vector.pos[1] * a)

        return(new_vector)



class Point:
    def __init__(self, screen, pos, r, w):
        self.screen = screen
        self.pos = pos
        self.r = r
        self.w = w

    def draw(self):
        pg.draw.circle(self.screen, (0,0,0), self.pos, self.r, self.w )

    def add_vector(self, vector):
        return Point(self.screen, (self.pos[0] + vector.pos[0], self.pos[1] + vector.pos[1]), self.r, self.w)








def vector(p1, p2):
    return(p2.x - p1.x, p2.y - p1.y)




class GraphicApp:

    def __init__(self):

        # priprava rozhrani
        pg.init()
        pg.display.set_caption('Graphic tools GUI')
        self.screen = pg.display.set_mode((900, 1600))


        self.create_buttons()
        self.create_points()


    def create_buttons(self):
        self.buttons = [Button(self.screen, 25, 25, 30, 30, 'RESET', func=lambda: self.reset())]
        self.buttons.append(Button(self.screen, 60, 25, 30, 30, 'BEZIER', func=lambda: self.bezier()))

    def create_points(self):
        self.points = list()

    def reset(self):
        self.points = []

    def add_point(self, p):
        self.points.append(p)

    def bezier(self):

        result = list()

        for r in np.arange(0, 1.01, 0.01):
            b = list()
            b.append(self.points)
            if r == 0.9:
                print()
            for i in range(1, len(self.points)):
                b.append([])

                for j in range(i, len(self.points)):
                    p1 = b[i - 1][j - i]
                    p2 = b[i - 1][j + 1 - i]
                    v1 = Vector(p1, p1)
                    v2 = Vector(p2, p1)

                    convex_combination = p1.add_vector(v1.scalar_multiplication(1 - r)).add_vector(
                        v2.scalar_multiplication(r))
                    b[i].append(convex_combination)

            result_point = b[-1][-1]
            result_point.pos = (int(np.ceil(result_point.pos[0])), int(np.ceil(result_point.pos[1])))
            result.append(result_point)

        self.points.extend(result)


    def draw_points(self):

        for p in self.points:
            p.draw()

    def draw_buttons(self):

        for b in self.buttons:
            b.draw()


def main():

    app = GraphicApp()
    clock = pg.time.Clock()
    while True:
        app.screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                p = True
                for b in app.buttons:
                    if b.clicked():
                        p = False
                        b.func()
                        print('baba')
                if p:
                    app.add_point(Point(app.screen, pg.mouse.get_pos(), 3, 1))


        app.draw_points()
        app.draw_buttons()

        pg.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()


