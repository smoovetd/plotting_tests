from flask import Flask, render_template, request
from triangle import run


app = Flask(__name__, template_folder='ui')

@app.route('/home')
def get_homepage():
    return render_template('triangle_template.html')

@app.route('/triangle', methods=['POST'])
def post_triangle_by_sides():
    point_a = [float(request.form.get('point_a_x')), float(request.form.get('point_a_y'))]
    point_b = [float(request.form.get('point_b_x')), float(request.form.get('point_b_y'))]
    point_c = [float(request.form.get('point_c_x')), float(request.form.get('point_c_y'))]

    result = run(point_a, point_b, point_c, False)

    pic = result[0]
    points = result[1]
    print(points)

    return render_template('pic.html', image_path= pic, a_x=point_a[0], a_y = point_a[1], b_x=point_b[0], b_y = point_b[1], c_x=point_c[0], c_y = point_c[1], points = points )


if __name__ == '__main__':
    #print (run([0,0],[6,0],[3,5.19]))
    app.run(debug=True)


