{
    "name": "ADT Auto Urgent Priority from Source",
    "version": "1.0",
    "author": "Your Name",
    "category": "Inventory",
    "depends": ["stock", "sale"],
    "description": """
When a delivery order is created via a Sale Order whose “Source” matches your target,
and whose picking name begins with “PICK” or “PACK”, it will be set to Urgent.
    """,
    "installable": True,
    "application": False,
}
