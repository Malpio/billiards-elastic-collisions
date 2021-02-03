from vpython import *

scene.center = vector(0, 0, 0)

scene.forward = vector(-1, -1, -1)
scene.width = 1200
scene.height = 650

main = box(pos=vector(0, 0, 0), size=vector(10, 0.1, 7), color=color.green)

main_band_x1 = box(pos=vector(4.95, 0.3, 0), size=vector(0.1, 0.5, 7), color=color.green)
main_band_x2 = box(pos=vector(-4.95, 0.3, 0), size=vector(0.1, 0.5, 7), color=color.green)
main_band_z1 = box(pos=vector(0, 0.3, 3.45), size=vector(9.8, 0.5, 0.1), color=color.green)
main_band_z2 = box(pos=vector(0, 0.3, -3.45), size=vector(9.8, 0.5, 0.1), color=color.green)

out_box = box(pos=vector(0, -0.1, 0), size=vector(10.2, 0.1, 7.2), texture=textures.wood)

out_box_band_x1 = box(pos=vector(5.05, 0.3, 0), size=vector(0.1, 0.7, 7), texture=textures.wood)
out_box_band_x2 = box(pos=vector(-5.05, 0.3, 0), size=vector(0.1, 0.7, 7), texture=textures.wood)
out_box_band_z1 = box(pos=vector(0, 0.3, 3.55), size=vector(10.2, 0.7, 0.1), texture=textures.wood)
out_box_band_z2 = box(pos=vector(0, 0.3, -3.55), size=vector(10.2, 0.7, 0.1), texture=textures.wood)

positions = [vector(-3, 0.3, 0),
             vector(2, 0.3, 0),
             vector(2.5, 0.3, 0.25),
             vector(2.5, 0.3, -0.25),
             vector(3, 0.3, -0.5),
             vector(3, 0.3, 0),
             vector(3, 0.3, 0.5),
             vector(3.5, 0.3, 0.25),
             vector(3.5, 0.3, -0.25),
             vector(3.5, 0.3, 0.75),
             vector(3.5, 0.3, -0.75)]

balls = [sphere(pos=x, radius=0.25, color=color.yellow) for x in positions]

for ball in balls:
    ball.velocity = vector(0, 0, 0)
    ball.collision = None

balls[0].velocity = vector(3, 0, 0)
balls[0].color = color.white
dt = 0.01

while True:
    rate(200)
    main_ball_index = 0
    for ball in balls:
        if ball.pos.z + ball.radius >= main_band_z1.pos.z - 0.05 or ball.pos.z - ball.radius <= main_band_z2.pos.z + 0.05:
            ball.velocity = vector(ball.velocity.x, ball.velocity.y, -ball.velocity.z)
        if ball.pos.x + ball.radius >= main_band_x1.pos.x - 0.05 or ball.pos.x - ball.radius <= main_band_x2.pos.x + 0.05:
            ball.velocity = vector(-ball.velocity.x, ball.velocity.y, ball.velocity.z)

        ball_index = main_ball_index + 1
        for ball2 in balls[ball_index:]:
            vector_difference = ball.pos - ball2.pos
            distance = mag(vector_difference)
            if not ball.collision == ball_index and distance <= ball.radius * 2:
                v1v2diff = ball.velocity - ball2.velocity
                x1x2diff = ball.pos - ball2.pos
                v1v2diff_x1x2diff_scalar = v1v2diff.x * x1x2diff.x + v1v2diff.z * x1x2diff.z
                first_new_velocity = ball.velocity - (
                            v1v2diff_x1x2diff_scalar / sqrt(x1x2diff.x ** 2 + x1x2diff.z ** 2) ** 2) * x1x2diff

                v2v1diff = ball2.velocity - ball.velocity
                x2x1diff = ball2.pos - ball.pos
                v2v1diff_x2x1diff_scalar = v2v1diff.x * x2x1diff.x + v2v1diff.z * x2x1diff.z
                second_new_velocity = ball2.velocity - v2v1diff_x2x1diff_scalar / sqrt(
                    x2x1diff.x ** 2 + x2x1diff.z ** 2) ** 2 * x2x1diff
                ball.velocity = first_new_velocity
                ball2.velocity = second_new_velocity

                ball.collision = ball_index
            elif ball.collision == ball_index and distance > ball.radius * 2:
                ball.collision = None

            ball_index += 1
        ball.pos = ball.pos + ball.velocity * dt
        main_ball_index += 1
