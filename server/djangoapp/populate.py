from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars"},
        {"name": "Mercedes", "description": "Great cars"},
        {"name": "Audi", "description": "Great cars"},
        {"name": "Kia", "description": "Great cars"},
        {"name": "Toyota", "description": "Great cars"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(
            CarMake.objects.create(
                name=data['name'],
                description=data['description']
            )
        )

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023,
         "make": car_make_instances[0]},
        {"name": "Qashqai", "type": "SUV", "year": 2023,
         "make": car_make_instances[0]},
        {"name": "Xtrail", "type": "SUV", "year": 2023,
         "make": car_make_instances[0]},
        {"name": "A-Class", "type": "SUV", "year": 2023,
         "make": car_make_instances[1]},
        {"name": "C-Class", "type": "SUV", "year": 2023,
         "make": car_make_instances[1]},
        {"name": "E-Class", "type": "SUV", "year": 2023,
         "make": car_make_instances[1]},
        {"name": "A4", "type": "SUV", "year": 2023,
         "make": car_make_instances[2]},
        {"name": "A5", "type": "SUV", "year": 2023,
         "make": car_make_instances[2]},
        {"name": "A6", "type": "SUV", "year": 2023,
         "make": car_make_instances[2]},
        {"name": "Sorrento", "type": "SUV", "year": 2023,
         "make": car_make_instances[3]},
        {"name": "Sportage", "type": "SUV", "year": 2023,
         "make": car_make_instances[3]},
        {"name": "Cerato", "type": "SUV", "year": 2023,
         "make": car_make_instances[3]},
        {"name": "Corolla", "type": "SUV", "year": 2023,
         "make": car_make_instances[4]},
        {"name": "Camry", "type": "SUV", "year": 2023,
         "make": car_make_instances[4]},
        {"name": "Kluger", "type": "SUV", "year": 2023,
         "make": car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['make'],
            type=data['type'],
            year=data['year']
        )
