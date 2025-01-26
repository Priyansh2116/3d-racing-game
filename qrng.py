
import requests

def get_quantum_random_number():
    """
    Fetch a quantum random number from the ANU QRNG API.

    Returns:
        int: A random number generated using quantum randomness.
    """
    try:
        # ANU QRNG API endpoint
        api_url = "https://qrng.anu.edu.au/API/jsonI.php?length=5&type=uint16"

        # Send a GET request to the API
        response = requests.get(api_url, verify=False)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Extract the random number
        if data["success"]:
            random_number = data["data"][0]
            return random_number
        else:
            raise ValueError("Failed to fetch random number: {}".format(data["error"]))

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")
        return None
    except ValueError as e:
        print(f"Error processing API response: {e}")
        return None

# Example usage
if __name__ == "__main__":
    random_number = get_quantum_random_number()
    if random_number is not None:
        print(f"Quantum Random Number: {random_number}")
    else:
        print("Failed to generate a quantum random number.")

