import tenseal as ts
import numpy as np



# ----------------------------
# Client-Side Preparation
# ----------------------------

def create_ckks_context():
    poly_modulus_degree = 8192 # N=8192 : can encode up to N/2 values, Determines security and computational cost
    coeff_mod_bit_sizes = [60, 40, 60] 
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=poly_modulus_degree,
        coeff_mod_bit_sizes=coeff_mod_bit_sizes,
    )
    context.global_scale = 2**40  # Scaling factor for approximate computations
    context.generate_galois_keys()
    return context

def encrypt_client_samples(context, samples):
    encrypted_samples = []
    for sample in samples:
        encrypted_sample = ts.ckks_vector(context, sample)
        encrypted_samples.append(encrypted_sample)
    return encrypted_samples

np.random.seed(42) 
client_samples = np.random.randint(0, 101, size=(10, 256)).astype(np.float64)

context = create_ckks_context()
encrypted_samples = encrypt_client_samples(context, client_samples)


public_context = context.serialize(save_public_key=True, save_galois_keys=True)



# # ----------------------------
# # Server-Side Computation
# # ----------------------------

def encrypt_weights(public_context, weights):
    server_context = ts.context_from(public_context)
    encrypted_weights = ts.ckks_vector(server_context, weights)
    return encrypted_weights


server_weights = np.random.uniform(0, 1, size=256).astype(np.float64)
encrypted_weights = encrypt_weights(public_context, server_weights)


def server_compute_dot_products(encrypted_samples, encrypted_weights):
    encrypted_results = [encrypted_sample.dot(encrypted_weights) for encrypted_sample in encrypted_samples]
    return encrypted_results

encrypted_results = server_compute_dot_products(encrypted_samples, encrypted_weights)

# ----------------------------
# Client-Side Decryption
# ----------------------------

def decrypt_results(context, encrypted_results):
    decrypted_results = [encrypted_result.decrypt() for encrypted_result in encrypted_results]
    return decrypted_results


decrypted_results = decrypt_results(context, encrypted_results)

# Print the results
print("Client's Results (Predictions):")
for i, result in enumerate(decrypted_results):
    print(f"Sample {i + 1}: {result}")

actual_results = np.dot(client_samples, server_weights)
errors = np.array(decrypted_results).flatten() - actual_results
mae = np.mean(np.abs(errors))
print(f"Mean Absolute Error (MAE): {mae}")


