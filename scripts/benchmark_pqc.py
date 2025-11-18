# scripts/benchmark_pqc.py

"""
This script provides a baseline performance benchmark for NIST-selected
Post-Quantum Cryptography (PQC) algorithms using the OQS library.

It measures:
1.  Execution time for key generation, encapsulation/decapsulation (KEMs),
    and signing/verification (Signatures).
2.  The size of public keys, secret keys, and ciphertexts/signatures.

These metrics are crucial for evaluating the feasibility of PQC algorithms
in resource-constrained environments like satellites.
"""

import oqs
import time
import statistics
import csv
import os

# --- Configuration ---
# Number of iterations for each algorithm to get a stable average time.
NUM_ITERATIONS = 100
# Define the algorithms we want to test. These are the primary NIST standards.
KEM_ALGORITHMS = ["Kyber768"]
SIGNATURE_ALGORITHMS = ["Dilithium3", "Falcon-512", "SPHINCS+-SHA2-128f-simple"]
# Output file for the results
RESULTS_DIR = "results/tables"
OUTPUT_CSV_FILE = os.path.join(RESULTS_DIR, "pqc_benchmark_results.csv")

def benchmark_kem(kem_name: str, num_iterations: int) -> dict:
    """
    Benchmarks a Key Encapsulation Mechanism (KEM) algorithm.

    Args:
        kem_name: The name of the KEM algorithm to benchmark.
        num_iterations: The number of times to run the operations.

    Returns:
        A dictionary containing the benchmark results.
    """
    print(f"\n--- Benchmarking KEM: {kem_name} ---")
    
    # Use a context manager to handle the OQS object lifecycle
    with oqs.KeyEncapsulation(kem_name) as kem:
        # --- 1. Get Algorithm Details (Sizes in bytes) ---
        details = kem.details
        
        # --- 2. Benchmark Operations ---
        keygen_times = []
        encaps_times = []
        decaps_times = []

        print(f"Running {num_iterations} iterations...")
        for _ in range(num_iterations):
            # Key Generation
            start_time = time.perf_counter()
            public_key = kem.generate_keypair()
            secret_key = kem.export_secret_key()
            end_time = time.perf_counter()
            keygen_times.append((end_time - start_time) * 1000)  # Convert to milliseconds

            # Encapsulation
            start_time = time.perf_counter()
            ciphertext, shared_secret_client = kem.encap_secret(public_key)
            end_time = time.perf_counter()
            encaps_times.append((end_time - start_time) * 1000)

            # Decapsulation
            start_time = time.perf_counter()
            shared_secret_server = kem.decap_secret(secret_key, ciphertext)
            end_time = time.perf_counter()
            decaps_times.append((end_time - start_time) * 1000)

            # Sanity check to ensure correctness
            assert shared_secret_client == shared_secret_server

        # --- 3. Compile Results ---
        results = {
            "Algorithm": kem_name,
            "Type": "KEM",
            "Public Key (bytes)": details['length_public_key'],
            "Secret Key (bytes)": details['length_secret_key'],
            "Ciphertext (bytes)": details['length_ciphertext'],
            "Signature (bytes)": "N/A",
            "Keygen (ms)": statistics.mean(keygen_times),
            "Encaps/Sign (ms)": statistics.mean(encaps_times),
            "Decaps/Verify (ms)": statistics.mean(decaps_times),
        }
        return results

def benchmark_sig(sig_name: str, num_iterations: int) -> dict:
    """
    Benchmarks a Signature algorithm.

    Args:
        sig_name: The name of the signature algorithm to benchmark.
        num_iterations: The number of times to run the operations.

    Returns:
        A dictionary containing the benchmark results.
    """
    print(f"\n--- Benchmarking Signature: {sig_name} ---")
    
    with oqs.Signature(sig_name) as sig:
        details = sig.details
        
        keygen_times = []
        sign_times = []
        verify_times = []
        message = b"This is a sample message for signing."

        print(f"Running {num_iterations} iterations...")
        for _ in range(num_iterations):
            # Key Generation
            start_time = time.perf_counter()
            public_key = sig.generate_keypair()
            secret_key = sig.export_secret_key()
            end_time = time.perf_counter()
            keygen_times.append((end_time - start_time) * 1000)

            # Signing
            start_time = time.perf_counter()
            signature = sig.sign(message, secret_key)
            end_time = time.perf_counter()
            sign_times.append((end_time - start_time) * 1000)

            # Verification
            start_time = time.perf_counter()
            is_valid = sig.verify(message, signature, public_key)
            end_time = time.perf_counter()
            verify_times.append((end_time - start_time) * 1000)

            assert is_valid

        results = {
            "Algorithm": sig_name,
            "Type": "Signature",
            "Public Key (bytes)": details['length_public_key'],
            "Secret Key (bytes)": details['length_secret_key'],
            "Ciphertext (bytes)": "N/A",
            "Signature (bytes)": details['length_signature'],
            "Keygen (ms)": statistics.mean(keygen_times),
            "Encaps/Sign (ms)": statistics.mean(sign_times),
            "Decaps/Verify (ms)": statistics.mean(verify_times),
        }
        return results

def main():
    """
    Main function to run the benchmarks and save the results.
    """
    print("="*50)
    print("Starting PQC Algorithm Benchmark")
    print("="*50)
    
    all_results = []

    # Benchmark KEMs
    for alg in KEM_ALGORITHMS:
        try:
            result = benchmark_kem(alg, NUM_ITERATIONS)
            all_results.append(result)
        except oqs.MechanismNotEnabledError:
            print(f"Algorithm {alg} is not enabled in this build of liboqs. Skipping.")

    # Benchmark Signatures
    for alg in SIGNATURE_ALGORITHMS:
        try:
            result = benchmark_sig(alg, NUM_ITERATIONS)
            all_results.append(result)
        except oqs.MechanismNotEnabledError:
            print(f"Algorithm {alg} is not enabled in this build of liboqs. Skipping.")

    # --- Save results to CSV ---
    if not all_results:
        print("No results to save. Exiting.")
        return

    # Create directory if it doesn't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)

    header = all_results[0].keys()
    with open(OUTPUT_CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(all_results)
    
    print("\n" + "="*50)
    print(f"Benchmark finished. Results saved to '{OUTPUT_CSV_FILE}'")
    print("="*50)

    # --- Print a summary table to the console ---
    print("\nBenchmark Summary:")
    header_str = "{:<25} | {:<10} | {:>10} | {:>10} | {:>10} | {:>10}"
    print(header_str.format("Algorithm", "Type", "Keygen(ms)", "Sign(ms)", "Verify(ms)", "SigSize(B)"))
    print("-" * 85)
    for res in all_results:
        print(header_str.format(
            res["Algorithm"],
            res["Type"],
            f"{res['Keygen (ms)']:.3f}",
            f"{res['Encaps/Sign (ms)']:.3f}",
            f"{res['Decaps/Verify (ms)']:.3f}",
            res.get('Signature (bytes)', 'N/A')
        ))

if __name__ == "__main__":
    main()
