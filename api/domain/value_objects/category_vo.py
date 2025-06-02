class CategoryVO:
    def __init__(self, name: str):
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty")
        self.name = name.strip()

    def __str__(self):
        return self.name
