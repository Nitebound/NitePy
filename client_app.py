import pygame as pg
from netgame_client import NetgameClient

display = pg.display.set_mode((1024, 768))
pg.display.set_caption("Netgame Client")
client_handle = NetgameClient("192.168.0.159", 8081)
client_handle.connect()

if __name__ == "__main__":
    running = True
    frame_clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.type == pg.K_ESCAPE:
                    running = False

                if event.key == pg.K_SPACE:
                    client_handle.send("Hello server :)".encode("UTF-8"))

        frame_clock.tick(60)

pg.quit()
