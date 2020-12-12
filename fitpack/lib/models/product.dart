class Product{
    String title;
    String description;
    String directionsToUse;
    String composition;
    double price;
    
    Product({this.title,this.description,this.directionsToUse,this.composition,this.price});

    factory Product.fromJSON(Map<String,dynamic> json){
      return Product(
        title: json["title"],
        description: json["description"],
        directionsToUse: json["directions_to_use"],
        composition: json["composition"],
        price: json["price"]
      );
    }
}