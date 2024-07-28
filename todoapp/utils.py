import json
from .models import Task


def save_project_data_as_text(id,json_data):
    # Extract the project_id from the JSON data

    # Convert the entire JSON data to a string
    json_data_str = json.dumps(json_data)

    # Save the JSON data as text in the database
    Task.objects.update_or_create(
        id=id,
        defaults={'checklist': json_data_str}
    )
