import numpy as np
from numpy.random import randint
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image, ImageFont, ImageDraw, ImageOps
from matplotlib import pyplot as plt
import matplotlib_fontja

def create_text_image(message, font_size, margin):
    """指定されたテキストを描画し、画像として返す"""
    font = ImageFont.truetype(matplotlib_fontja.get_font_ttf_path(), font_size)
    # 一旦大きな画像を作成
    img_width = int(font_size * len(message) * 1.5)  # 横長に調整
    img = Image.new("RGB", (img_width, font_size), "black")
    draw = ImageDraw.Draw(img)
    text_bbox = draw.textbbox((0, 0), message, font=font)

    # テキストサイズに応じて切り抜き
    img = img.crop((0, 0, text_bbox[2], text_bbox[3]))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), message, font=font, fill="white")  # ストロークを削除

    # マージンを付与
    img = ImageOps.expand(img, border=margin, fill="black")
    return img

def generate_random_points(mask, size):
    """マスク内の黒い部分にランダムな点を生成する"""
    return np.array([
        (size - x, y)
        for (x, y) in zip(
            randint(0, mask.shape[0], size=size),
            randint(0, mask.shape[1], size=size)
        ) if mask[x, y]
    ])

def setup_animation(data, frames, min_data, size):
    """アニメーションを設定する"""
    fig, ax = plt.subplots(figsize=(10, 6))  # 横長の図を作成
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    sc = ax.scatter(data[:min_data][:, 1], data[:min_data][:, 0])
    # 軸を消す
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    def update(frame):
        frame += 1
        sc.set_offsets(
            np.c_[
                data[:min_data + (size // frames) * frame][:, 1],
                data[:min_data + (size // frames) * frame][:, 0]
            ]
        )
        return sc,

    ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)
    return ani

def main():
    config = {
        "message": "GMO",
        "font_size": 2000,
        "margin": 200,
        "size": 10000,
        "frames": 100,
        "min_data": 100,
        "output_file": "gmo_plot.gif",
        "fps": 10
    }

    # テキスト画像を生成
    img = create_text_image(config["message"], config["font_size"], config["margin"])

    # マスクを生成
    mask = np.array(img.convert("L")) == 0

    # ランダムな点を生成
    data = generate_random_points(mask, config["size"])

    # アニメーションを作成
    ani = setup_animation(data, config["frames"], config["min_data"], config["size"])

    # GIFとして保存
    ani.save(config["output_file"], writer=PillowWriter(fps=config["fps"]))

if __name__ == "__main__":
    main()
