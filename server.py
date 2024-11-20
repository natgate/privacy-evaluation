from flask import Flask, request, jsonify
import tenseal as ts
import numpy as np

app = Flask(__name__)

# Generate server weights (256 weights between 0 and 1)
server_weights = np.random.uniform(0, 1, size=256).astype(np.float64)

@app.route("/compute", methods=["POST"])
def compute():
    try:
        # Receive data from client
        data = request.json
        serialized_context = data["context"].encode("latin1")
        encrypted_samples_serialized = [s.encode("latin1") for s in data["samples"]]

        # Load context and encrypted samples
        context = ts.context_from(serialized_context)
        encrypted_samples = [ts.ckks_vector_from(context, sample) for sample in encrypted_samples_serialized]

        # Encrypt server weights
        encrypted_weights = ts.ckks_vector(context, server_weights)

        # Compute dot product for each sample
        encrypted_results = [sample.dot(encrypted_weights) for sample in encrypted_samples]

        # Serialize results and send back to client
        encrypted_results_serialized = [res.serialize().decode("latin1") for res in encrypted_results]
        return jsonify({"results": encrypted_results_serialized})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)