from flask import Flask, render_template, request, jsonify

from top_products import top_product

app = Flask(__name__)

# Dummy recommendation function
def get_recommended_products(user_input):
    products = top_product(user_input)
    return products

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    recommendations = get_recommended_products(user_input)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, port=6866, host='0.0.0.0')
