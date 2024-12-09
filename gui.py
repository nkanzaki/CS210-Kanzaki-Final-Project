import customtkinter as ctk
from hashtable import HashTable  
from tree import BST  
from stack import PageNavigator  
from graph import Graph  

class TrailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trail Application")
        self.root.geometry("600x1100")

        # Initialize data structures
        self.trails_table = self.load_trails("trails.txt")
        self.trails_list = [self.trails_table.search(trail_name) for trail_name in self.trails_table.keys()]
        self.filtered_trails = self.trails_list.copy()  # Initially, all trails are shown
        self.navigator = PageNavigator()
        self.trails_per_page = 5

        # Initialize Graph to manage trails
        self.graph = Graph()

        # Initialize page
        self.current_page = 0
        self.update_total_pages()

        # GUI elements
        self.create_widgets()
        self.display_page(self.current_page)  # Start with the first page

    def create_widgets(self):
        # Search Section
        ctk.CTkLabel(self.root, text="Your Next Adventure", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.root, text="Search Criteria:", font=("Arial", 14)).pack(pady=5)

        # Search fields
        self.entries = {
            "Trail Name": ctk.CTkEntry(self.root, width=400),
            "Length (miles)": ctk.CTkEntry(self.root, width=400),
            "Elevation Gain (feet)": ctk.CTkEntry(self.root, width=400),
            "Difficulty (1-3)": ctk.CTkEntry(self.root, width=400)
        }
        for field, entry in self.entries.items():
            ctk.CTkLabel(self.root, text=field).pack(anchor="w", padx=20)
            entry.pack(pady=5)

        # Search Button
        self.search_button = ctk.CTkButton(self.root, text="Search", command=self.search_trail)
        self.search_button.pack(pady=10)

        # Add New Trail Button
        self.add_trail_button = ctk.CTkButton(self.root, text="Add New Trail", command=self.show_add_trail_page)
        self.add_trail_button.pack(pady=10)

        # Sorting Section
        ctk.CTkLabel(self.root, text="Sort By:").pack(anchor="w", padx=20)
        self.sort_option = ctk.StringVar(value="Distance (Min to Max)")  # Default value
        self.sort_menu = ctk.CTkOptionMenu(
            self.root, variable=self.sort_option,
            values=[
                "Distance (Min to Max)", "Distance (Max to Min)",
                "Elevation (Min to Max)", "Elevation (Max to Min)",
                "Difficulty (Min to Max)", "Difficulty (Max to Min)"
            ],
            command=self.show_all_trails
        )
        self.sort_menu.pack(pady=10)

        # Results Display Area
        self.result_textbox = ctk.CTkTextbox(self.root, wrap="word", width=500, height=400)
        self.result_textbox.pack(pady=10, padx=20, fill="both", expand=True)

        # Navigation Section
        nav_frame = ctk.CTkFrame(self.root)
        nav_frame.pack(pady=10)

        self.back_button = ctk.CTkButton(nav_frame, text="Previous", command=self.previous_page)
        self.back_button.pack(side="left", padx=10)

        self.forward_button = ctk.CTkButton(nav_frame, text="Next", command=self.next_page)
        self.forward_button.pack(side="right", padx=10)

        # Current Page Label
        self.current_page_label = ctk.CTkLabel(nav_frame, text="Page 1 of 1", font=("Arial", 12))
        self.current_page_label.pack(side="bottom", pady=10)

    def load_trails(self, file_path):
        # Load trails from the file into a HashTable
        trails_table = HashTable(capacity=20)
        with open(file_path, "r") as file:
            lines = file.readlines()
        headers = lines[0].strip().split("|")
        for line in lines[1:]:
            data = line.strip().split("|")
            trail = {headers[i]: data[i] for i in range(len(headers))}
            trails_table.insert(trail["Trail Name"], trail)
        return trails_table

    def update_total_pages(self):
        # Update the total number of pages based on the filtered trails
        self.total_pages = (len(self.filtered_trails) + self.trails_per_page - 1) // self.trails_per_page

    def display_page(self, page_index):
        # Display the trails for the given page index
        start_index = page_index * self.trails_per_page
        end_index = min(start_index + self.trails_per_page, len(self.filtered_trails))
        trails_on_page = self.filtered_trails[start_index:end_index]

        # Clear the textbox and display the trails
        self.result_textbox.delete("1.0", "end")
        if trails_on_page:
            for trail in trails_on_page:
                self.result_textbox.insert("end", f"Trail Name: {trail['Trail Name']}\n")
                self.result_textbox.insert("end", f"Location: {trail['Location']}\n")
                self.result_textbox.insert("end", f"Distance: {trail['Distance (miles)']} miles\n")
                self.result_textbox.insert("end", f"Elevation Gain: {trail['Elevation Gain (feet)']} feet\n")
                self.result_textbox.insert("end", f"Difficulty: {trail['Difficulty (1-3)']}/3\n")
                self.result_textbox.insert("end", "-" * 40 + "\n")
        else:
            self.result_textbox.insert("1.0", "No trails match the search criteria.")

        # Update the page label
        self.current_page_label.configure(text=f"Page {page_index + 1} of {self.total_pages}")

        # Enable/disable navigation buttons
        self.back_button.configure(state="normal" if page_index > 0 else "disabled")
        self.forward_button.configure(state="normal" if page_index + 1 < self.total_pages else "disabled")

    def search_trail(self):
        # Get search criteria from inputs
        criteria = {field: entry.get().strip().lower() for field, entry in self.entries.items()}

        # Find matching trails
        matching_trails = [
            self.trails_table.search(trail_name)
            for trail_name in self.trails_table.keys()
            if self.matches_criteria(self.trails_table.search(trail_name), criteria)
        ]

        # Display results
        self.filtered_trails = matching_trails
        self.update_total_pages()
        self.display_page(0)  # Reset to the first page after filtering

    def matches_criteria(self, trail, criteria):
        # Check if a trail matches search criteria
        if criteria["Trail Name"] and criteria["Trail Name"] not in trail["Trail Name"].lower():
            return False
        if criteria["Length (miles)"] and float(trail["Distance (miles)"]) != float(criteria["Length (miles)"]):
            return False
        if criteria["Elevation Gain (feet)"] and int(trail["Elevation Gain (feet)"]) != int(criteria["Elevation Gain (feet)"]):
            return False
        if criteria["Difficulty (1-3)"] and trail["Difficulty (1-3)"] != criteria["Difficulty (1-3)"]:
            return False
        return True

    def previous_page(self):
        # Go to the previous page
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)

    def next_page(self):
        # Go to the next page
        if self.current_page + 1 < self.total_pages:
            self.current_page += 1
            self.display_page(self.current_page)

    def show_all_trails(self, sort_key=None):
        # Get sort field and order
        sort_key = sort_key or self.sort_option.get()
        sort_map = {
            "Distance (Min to Max)": ("Distance (miles)", False),
            "Distance (Max to Min)": ("Distance (miles)", True),
            "Elevation (Min to Max)": ("Elevation Gain (feet)", False),
            "Elevation (Max to Min)": ("Elevation Gain (feet)", True),
            "Difficulty (Min to Max)": ("Difficulty (1-3)", False),
            "Difficulty (Max to Min)": ("Difficulty (1-3)", True),
        }
        field, reverse = sort_map.get(sort_key, ("Trail Name", False))

        # Prepare data for BST
        trails = [self.trails_table.search(trail_name) for trail_name in self.trails_table.keys()]
        values = [
            (float(trail[field]) if field != "Trail Name" else trail[field], trail)
            for trail in trails
        ]

        # Insert values into BST
        bst = BST()
        for value, trail in values:
            bst.insert(value, trail)

        # Get sorted values
        sorted_trails = bst.sortmintomax() if not reverse else bst.sort_max_to_min()

        # Display results
        self.filtered_trails = [trail for _, trail in sorted_trails]
        self.update_total_pages()
        self.display_page(0)  # Reset to the first page after sorting

    def show_add_trail_page(self):
        # Switch to add trail page
        self.clear_widgets()
        self.create_add_trail_page()

    def clear_widgets(self):
        # Remove all widgets
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_add_trail_page(self):
        # Add New Trail page UI
        ctk.CTkLabel(self.root, text="Add New Trail", font=("Arial", 16)).pack(pady=10)

        # Input fields for new trail
        self.new_trail_entries = {
            "Trail Name": ctk.CTkEntry(self.root, width=400),
            "Location": ctk.CTkEntry(self.root, width=400),
            "Distance (miles)": ctk.CTkEntry(self.root, width=400),
            "Elevation Gain (feet)": ctk.CTkEntry(self.root, width=400),
            "Difficulty (1-3)": ctk.CTkEntry(self.root, width=400)
        }
        for field, entry in self.new_trail_entries.items():
            ctk.CTkLabel(self.root, text=field).pack(anchor="w", padx=20)
            entry.pack(pady=5)

        # Submit Button
        self.submit_button = ctk.CTkButton(self.root, text="Submit", command=self.submit_new_trail)
        self.submit_button.pack(pady=10)

        # Return to main page button
        self.return_button = ctk.CTkButton(self.root, text="Return to Main Page", command=self.return_to_main_page)
        self.return_button.pack(pady=10)

    def submit_new_trail(self):
        # Get new trail data
        trail_data = {field: entry.get().strip() for field, entry in self.new_trail_entries.items()}

        # Add the trail to the graph
        self.graph.add_trail(trail_data["Trail Name"], trail_data)

        # Return to the main page
        self.clear_widgets()
        self.create_widgets()
        self.display_page(self.current_page)

    def return_to_main_page(self):
        # Go back to the main page
        self.clear_widgets()
        self.create_widgets()
        self.display_page(self.current_page)
