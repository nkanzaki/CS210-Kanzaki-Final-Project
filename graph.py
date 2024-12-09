class Graph:
    def __init__(self):
        # Store trails with attributes and connections
        self.trails = {}

    def add_trail(self, trail_name, attributes=None):
        # Add trail with default values if attributes are missing
        default_attributes = {
            "Location": "Unknown",
            "Distance (miles)": "Unknown",
            "Elevation Gain (feet)": "Unknown",
            "Difficulty (1-3)": "Unknown",
        }
        attributes = attributes or {}
        trail_data = {key: attributes.get(key, default) for key, default in default_attributes.items()}

        # Add or update the trail
        if trail_name not in self.trails:
            self.trails[trail_name] = {"attributes": trail_data, "connections": []}
        else:
            self.trails[trail_name]["attributes"] = trail_data

        # Write the new trail to the text file
        self.write_trail_to_file(trail_name, trail_data)

    def write_trail_to_file(self, trail_name, trail_data):
        # Open trails.txt in append mode
        with open("trails.txt", "a") as file:
            # Format the new trail data correctly for the file
            trail_line = f"\n{trail_name}|{trail_data['Location']}|{trail_data['Distance (miles)']}|{trail_data['Elevation Gain (feet)']}|{trail_data['Difficulty (1-3)']}"
            file.write(trail_line)

    def connect_trails(self, trail1, trail2):
        # Create a bidirectional connection
        if trail1 in self.trails and trail2 in self.trails:
            if trail2 not in self.trails[trail1]["connections"]:
                self.trails[trail1]["connections"].append(trail2)
            if trail1 not in self.trails[trail2]["connections"]:
                self.trails[trail2]["connections"].append(trail1)

    def get_trails(self):
        # Return all trails
        return self.trails

    def get_trail(self, trail_name):
        # Return a single trail by name
        return self.trails.get(trail_name)

    def display_trail(self, trail_name):
        # Print trail details
        trail = self.trails.get(trail_name)
        if trail:
            print(f"Trail: {trail_name}")
            print(f"Attributes: {trail['attributes']}")
            print(f"Connections: {', '.join(trail['connections'])}")
        else:
            print(f"Trail '{trail_name}' not found.")
