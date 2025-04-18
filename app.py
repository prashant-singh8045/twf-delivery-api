from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define product locations
product_locations = {
    "A": "C1", "B": "C1", "C": "C1",
    "D": "C2", "E": "C2", "F": "C2",
    "G": "C3", "H": "C3", "I": "C3"
}

# Define travel costs
travel_costs = {
    ("C1", "L1"): 20,
    ("C2", "L1"): 30,
    ("C3", "L1"): 25,
    ("C1", "C2"): 15,
    ("C2", "C1"): 15,
    ("C1", "C3"): 10,
    ("C3", "C1"): 10,
    ("C2", "C3"): 15,
    ("C3", "C2"): 15,
    ("L1", "C1"): 20,
    ("L1", "C2"): 30,
    ("L1", "C3"): 25
}

def calculate_min_cost(order):
    centers_needed = set()
    for product, quantity in order.items():
        if quantity > 0:
            centers_needed.add(product_locations.get(product))

    if not centers_needed:
        return 0

    start_center = min(centers_needed, key=lambda center: travel_costs.get((center, "L1"), float('inf')))
    centers_needed.remove(start_center)

    total_cost = travel_costs.get((start_center, "L1"), 0)
    current_center = start_center

    while centers_needed:
        next_center = min(centers_needed, key=lambda center: travel_costs.get((current_center, center), float('inf')))
        total_cost += travel_costs.get((current_center, next_center), 0)
        current_center = next_center
        centers_needed.remove(next_center)

    total_cost += travel_costs.get((current_center, "L1"), 0)

    return total_cost

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    data = request.get_json()
    min_cost = calculate_min_cost(data)

    return jsonify({
        "message": "Delivery cost calculated!",
        "minimum_cost": min_cost
    })

if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)  # Use dynamic port or default to 5000
    app.run(host="0.0.0.0", port=int(port), debug=False)  # Debug turned off
