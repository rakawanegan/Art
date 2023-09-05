# imitation of https://qiita.com/kurumaebi65/items/7e31b762fb529ad98739
import math
import time

window_width = 100
window_height = 100
K2 = 5
div1 = 50
div2 = 50
R1 = 1
R2 = 2
K1 = window_width*K2*3/(8*(R1+R2))

characters = ".,-~:;=!*#$@"


def calc_surface(A, B):
    # よく使う変数をあらかじめ計算
    sinA = math.sin(A)
    sinB = math.sin(B)
    cosA = math.cos(A)
    cosB = math.cos(B)
    # ターミナル上に投影する文字を格納する配列
    display = [[" " for i in range(window_width)]for j in range(window_height)]
    # z_bufferを管理するための配列
    z_buffer = [[0 for i in range(window_width)] for j in range(window_height)]
    # ターミナル上に投影する文字を格納する配列
    for theta in [(2*math.pi*x)/div1 for x in range(div1)]:
        for phi in [(2*math.pi*x)/div2 for x in range(div2)]:
            # よく使う変数をあらかじめ計算その2
            cosphi = math.cos(phi)
            costheta = math.cos(theta)
            sinphi = math.sin(phi)
            sintheta = math.sin(theta)
            circlex = R2+R1*costheta
            circley = R1*sintheta
            # ドーナツの表面上の点を計算
            x = (circlex)*(cosB*cosphi+sinA*sinB*sinphi)-circley*cosA*sinB
            y = (circlex)*(cosphi*sinB-cosB*sinA*sinphi)+circley*cosA*cosB
            z = K2 + (cosA*circlex*sinphi + circley*sinA)
            # ドーナツをターミナル上に投影した時の位置を計算
            display_x = int(window_width/2 + (K1 * x) / (K2 + z))
            display_y = int(window_height/2 - (K1 * y) / (K2 + z))
            # zバッファーの計算
            if z_buffer[display_y][display_x] < 1/z:
                z_buffer[display_y][display_x] = 1/z
                # 光の反射を計算
                L = cosphi*costheta*sinB - cosA*costheta*sinphi - sinA * \
                    sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi)
                # 計算された光の反射をもとに文字に変換する
                display[display_y][display_x] = characters[int(L*8)]
    return "\n".join(["".join(line) for line in display])

# ターミナル上でアニメーションを表現するための下準備
# あらかじめ表示する行数だけカーソルを下に移動させる
print(f"\033[{window_height}S", end="")
# 最初の行へ戻す
print(f"\033[{window_height}A", end="")
# 最初の行の位置を記憶しておく
print("\033[s", end="")

A = 0
B = 0

while True:
    A += 0.15
    B += 0.1
    img = calc_surface(A, B)
    # 記憶された情報をもとに最初の行の位置へ移動する
    print("\033[u", end="")
    print(img, flush=True)
    time.sleep(0.05)
