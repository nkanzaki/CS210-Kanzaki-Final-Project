class PageNavigator:
    def __init__(self):
        self.forward_stack = []  # Stack for next pages
        self.back_stack = []    # Stack for previous pages
        self.current_page = None

    def visit_page(self, page):
        # Add current page to back stack before navigating
        if self.current_page is not None:
            self.back_stack.append(self.current_page)
        self.current_page = page
        self.forward_stack.clear()  # Clear forward stack after visiting a new page

    def go_back(self):
        # Go back to the previous page if possible
        if not self.back_stack:
            return None
        self.forward_stack.append(self.current_page)
        self.current_page = self.back_stack.pop()
        return self.current_page

    def go_forward(self):
        # Go forward to the next page if possible
        if not self.forward_stack:
            return None
        self.back_stack.append(self.current_page)
        self.current_page = self.forward_stack.pop()
        return self.current_page
