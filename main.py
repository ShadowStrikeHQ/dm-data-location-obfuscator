import argparse
import logging
import random
import math
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Obfuscates geographic coordinates by adding random noise.")

    parser.add_argument("latitude", type=float, help="The latitude of the location.")
    parser.add_argument("longitude", type=float, help="The longitude of the location.")
    parser.add_argument("radius", type=float, help="The radius (in meters) within which to add noise.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG level)")
    parser.add_argument("-n", "--num-points", type=int, default=1, help="Number of obfuscated points to generate.")

    return parser

def add_noise_to_coordinates(latitude, longitude, radius_meters):
    """
    Adds random noise to geographic coordinates.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        radius_meters (float): The radius (in meters) within which to add noise.

    Returns:
        tuple: A tuple containing the obfuscated latitude and longitude.
    """
    try:
        # Input validation
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a number.")
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a number.")
        if not isinstance(radius_meters, (int, float)):
            raise TypeError("Radius must be a number.")
        if radius_meters < 0:
            raise ValueError("Radius must be a non-negative number.")


        # Earth's radius in meters
        earth_radius = 6371000

        # Convert radius from meters to degrees
        radius_degrees = radius_meters / earth_radius

        # Generate random angle in radians
        random_angle = random.uniform(0, 2 * math.pi)

        # Calculate the change in latitude and longitude
        delta_latitude = radius_degrees * math.sin(random_angle)
        delta_longitude = radius_degrees * math.cos(random_angle)

        # Calculate the new latitude and longitude
        new_latitude = latitude + delta_latitude
        new_longitude = longitude + delta_longitude

        return new_latitude, new_longitude

    except (TypeError, ValueError) as e:
        logging.error(f"Error during coordinate obfuscation: {e}")
        raise  # Re-raise the exception for handling in main()

def main():
    """
    Main function to parse arguments, add noise to coordinates, and print the result.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose logging enabled.")

    try:
        for _ in range(args.num_points):
            new_latitude, new_longitude = add_noise_to_coordinates(args.latitude, args.longitude, args.radius)
            print(f"Original Coordinates: Latitude={args.latitude}, Longitude={args.longitude}")
            print(f"Obfuscated Coordinates: Latitude={new_latitude}, Longitude={new_longitude}")
            print("-" * 30)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    """
    Entry point of the script.
    """
    main()