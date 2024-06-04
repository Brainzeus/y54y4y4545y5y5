import random
import secp256k1 as ice
import time
import os
from concurrent.futures import ThreadPoolExecutor

address_to_find = input("Which keyword do you want to find ? ")
start = time.time()
i = 0
generated_keys = 0  # Contor pentru cheile generate
num_threads = 8  # Numărul de fire de execuție (ajustabil în funcție de CPU)

# Funcție pentru a genera un număr întreg aleatoriu într-un interval specificat
def RandomInteger(minN, maxN):
    return random.randrange(minN, maxN)

# Funcție pentru a codifica un număr în format binar (codificare simplă)
def custom_encode(number):
    return format(number, '0256b')  # Codificare binară de 256 de caractere

# Funcție pentru a genera și verifica o adresă
def generate_and_check_address():
    global generated_keys, i
    while True:
        dec = RandomInteger(1157920892373161954235709850086879078528375642790749043826, 115792089237316195423570985008687907852837564279074904382605163141518161494336)
        HEX = "%064x" % dec
        generated_keys += 1

        # Generăm adrese Bitcoin pentru cheile private în format normal și comprimat
        address_uncompressed = ice.privatekey_to_address(0, False, dec)
        address_compressed = ice.privatekey_to_address(0, True, dec)
        
        # Verificăm dacă adresele generate conțin cuvântul cheie dorit
        if address_to_find in address_uncompressed:
            print(f"[{i}] Uncompressed: {address_uncompressed}")
            print(f"   => Eureka !!! Private key : {ice.btc_pvk_to_wif(HEX, False)}")
            return True
        if address_to_find in address_compressed:
            print(f"[{i}] Compressed: {address_compressed}")
            print(f"   => Eureka !!! Private key : {ice.btc_pvk_to_wif(HEX, True)}")
            return True

        i += 1

# Funcție pentru a calcula și afișa numărul de chei generate pe secundă
def print_keys_per_second():
    global start, generated_keys
    while True:
        time.sleep(1)  # Așteptăm un interval de o secundă
        current_time = time.time()
        elapsed_time = current_time - start
        keys_per_second = generated_keys / elapsed_time if elapsed_time > 0 else 0
        print(f"Keys generated: {generated_keys} | Keys per second: {keys_per_second:.2f}")

# Funcție principală
def main():
    global generated_keys, i
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Lansăm un fir de execuție separat pentru a calcula și afișa cheile generate pe secundă
        executor.submit(print_keys_per_second)
        
        futures = [executor.submit(generate_and_check_address) for _ in range(num_threads)]
        for future in futures:
            if future.result():
                break

    end = time.time()
    elapsed_time = end - start
    keys_per_second = generated_keys / elapsed_time if elapsed_time > 0 else 0
    print(f'Running time: {elapsed_time} Seconds')
    print(f'Keys generated: {generated_keys} | Keys per second: {keys_per_second:.2f}')
    os.system("pause")

if __name__ == "__main__":
    main()
