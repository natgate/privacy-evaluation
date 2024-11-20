import requests
import tenseal as ts
import numpy as np
import json

def create_ckks_context():
    poly_modulus_degree = 8192  # N=8192 : can encode up to N/2 values, Determines security and computational cost
    coeff_mod_bit_sizes = [60, 40, 60] 
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=poly_modulus_degree,
        coeff_mod_bit_sizes=coeff_mod_bit_sizes,
    )
    context.global_scale = 2**40 # Scaling factor for approximate computations
    context.generate_galois_keys() # Galois keys for all necessary rotations
    return context

def encrypt_client_samples(context, samples):
    encrypted_samples = [ts.ckks_vector(context, sample) for sample in samples]
    return encrypted_samples

# Generate 10 samples of random client data (10x256 samples)
np.random.seed(42)
client_samples = np.random.randint(0, 101, size=(10, 256)).astype(np.float64)

# Create context and encrypt data
context = create_ckks_context()
encrypted_samples = encrypt_client_samples(context, client_samples)

# Serialize context and encrypted data
serialized_context = context.serialize(save_public_key=True, save_galois_keys=True)
# print(len(serialized_context)) 17MB
# print(len(encrypted_samples_serialized[0])) #~229KB

# decrypted_sample = encrypted_samples[0].decrypt()  # Decrypt the first ciphertext
encrypted_samples_serialized = [sample.serialize() for sample in encrypted_samples]





# Send to server
url = "http://127.0.0.1:5000/compute"
payload = {
    "context": serialized_context.decode("latin1"),
    "samples": [sample.decode("latin1") for sample in encrypted_samples_serialized],
}
response = requests.post(url, json=payload)


if response.status_code == 200:
    encrypted_results_serialized = [res.encode("latin1") for res in response.json()["results"]]
    encrypted_results = [ts.ckks_vector_from(context, res) for res in encrypted_results_serialized]
    decrypted_results = [result.decrypt() for result in encrypted_results]

    # Display the results
    print("Client's Decrypted Results:")
    for i, res in enumerate(decrypted_results):
        print(f"Sample {i + 1}: {res}")
else:
    print("Error:", response.text)

