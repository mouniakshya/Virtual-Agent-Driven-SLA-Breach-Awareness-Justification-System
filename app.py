
from flask import Flask, request, jsonify
import joblib

model = joblib.load('../ml_model/sla_model.joblib')
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    priority_map = {'Low': 0, 'Medium': 1, 'High': 2}
    priority = priority_map.get(data['priority'], 1)
    features = [[priority, data['created_hours']]]
    pred = model.predict(features)[0]
    risk = "High" if pred else "Low"
    assigned_team = "L2" if priority == 2 else "L1"
    return jsonify({
        "assigned_team": assigned_team,
        "sla_breach_risk": risk
    })

if __name__ == "__main__":
    app.run(debug=True)
