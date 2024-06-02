from flask import Flask, render_template, redirect, url_for
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time

app = Flask(__name__)

# Öğrenci bilgileri
name = "Osman Yusuf"
surname = "KURT"
student_number = "211220053"

def generate_plot():
    np.random.seed(int(time.time()))
    x_range = 1000
    y_range = 1000
    n_points = 500

    # Her bir hücrede rastgele noktalar oluşturmak için
    x = np.random.randint(0, x_range, n_points)
    y = np.random.randint(0, y_range, n_points)

    df = pd.DataFrame({
        'X Koordinatları': x,
        'Y Koordinatları': y
    })

    excel_path = './static/koordinatlar.xlsx'
    df.to_excel(excel_path, index=False)

    color_map = {
        'b': 'Mavi',
        'g': 'Yeşil',
        'r': 'Kırmızı',
        'c': 'Cyan',
        'm': 'Mor',
        'y': 'Sarı',
        'k': 'Siyah',
        'orange': 'Turuncu',
        'purple': 'Eflatun',
        'brown': 'Kahverengi'
    }
    colors = list(color_map.keys())

    plt.figure(figsize=(8, 6))

    # Grafiği ızgaralara bölmek için ızgara boyutunu belirleyelim
    grid_size = (3, 4)  # 3x4 bir ızgara oluşturalım
    cell_width = x_range / grid_size[1]
    cell_height = y_range / grid_size[0]

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            color = np.random.choice(colors)
            x_min = j * cell_width
            x_max = (j + 1) * cell_width
            y_min = i * cell_height
            y_max = (i + 1) * cell_height

            # Bu hücredeki noktalar için rastgele koordinatlar oluştur
            cell_x = np.random.uniform(x_min, x_max, n_points // (grid_size[0] * grid_size[1]))
            cell_y = np.random.uniform(y_min, y_max, n_points // (grid_size[0] * grid_size[1]))

            plt.scatter(cell_x, cell_y, c=color, label=color_map[color], s=25, alpha=0.6)

            # Her bir ızgarayı siyah çizgilerle ayıralım
            plt.plot([x_min, x_min], [0, y_range], 'k-', linewidth=0.5)
            plt.plot([x_max, x_max], [0, y_range], 'k-', linewidth=0.5)
            plt.plot([0, x_range], [y_min, y_min], 'k-', linewidth=0.5)
            plt.plot([0, x_range], [y_max, y_max], 'k-', linewidth=0.5)

    plt.title('Rastgele Koordinatlar ile Nokta Dağılımı')
    plt.xlabel('X Koordinatları')
    plt.ylabel('Y Koordinatları')
    plt.grid(True)
    plt.legend(title='Renk Grupları', loc='lower left')
    plt.axis([0, x_range, 0, y_range])

    plot_path = './static/koordinatlar_plot.png'
    plt.savefig(plot_path)
    plt.close()

@app.route('/')
def index():
    if not os.path.exists('./static/koordinatlar_plot.png'):
        generate_plot()
    return render_template('index.html', name=name, surname=surname, student_number=student_number)

@app.route('/refresh_plot')
def refresh_plot():
    generate_plot()
    return redirect(url_for('index'))

def main():
    if not os.path.exists('./static'):
        os.makedirs('./static')
    generate_plot()  # İlk görseli oluştur
    app.run(debug=True)

if __name__ == '__main__':
    main()
