### FitBuddy

#### Motivation

Everybody is worried about how fit they are. Many of us would want detalied analysis of our food intake, water consumption etc.,. We might want to know nearest fitness centers to exercise at a new place. Here, our project FitBuddy comes to the rescue.

#### What is FitBuddy?

Our project consists of three parts:

Fitness Centers Section
Nutrition section
Discussion Forum Section

##### We provide services to equipment stores/ fitness products store/ other clients to advertise their products and attract potential fitness centers for business
##### We provide fitness job lists for other job hunting sites to connect fitness trainers with their respective interests

#### Services Consumed & Why?

- Edamam API for nutritional analysis to obtain accurate nutritional content in food
- Stripe payment service for possible payments in fitness center section

#### Services exposed

Fitness Center Section:

- View list of programs - GET, Endpoint: /programs
- View list of reviews - GET

Discussion Forum section:

- View list of questions - GET
- View list of answers - GET
- View list of recent questions - GET
- View list of recent answers - GET
- Views list of answers sorted based on number of votes - GET

Equipment store/ Fitness product section

- Products/Equipments - GET, POST, PUT, DELETE

#### Mock Application

- A Flutter app is developed for three endpoints of GET, POST on products, GET on programs endpoint

### Guidelines for developers

```
flutter run
```

Run the above command from fitpack folder to run the mock app locally. Before that you need Flutter and Android Studio installed

```
python manage.py makemigrations
```

```
python manage.py migrate
```
```
python manage.py runserver
```

If you find any migrations or db file initially, remove it and run the above commands to start the development server smoothly without any errors

#### If you are interested to contribute, feel free to raise an issue!

#### Contributors

- Swathi Kedharsetty
- Rukmini Meda
- Haneesha Vakkalagadda
- Hari Chandana Akula
- Sai Saankhya Katari


