import 'package:fitpack/models/product.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AddProduct extends StatefulWidget {
  @override
  _AddProductState createState() => _AddProductState();
}

class _AddProductState extends State<AddProduct> {

  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();
  final TextEditingController _directionsController = TextEditingController();
  final TextEditingController _compositionController = TextEditingController();
  final TextEditingController _priceController = TextEditingController();

  Future<Product> addProduct(Product product) async{
    try{
        print("posting here");
        final String url = "http://10.0.2.2:8000/ads/fitness-product-list";
        final response = await http.post(url,
          headers: <String,String>{
            "Content-Type": "application/json;charset=UTF-8",
          },
          body: jsonEncode(
            <String,String>{
              "title": product.title,
              "description": product.description,
              "directions_to_use": product.directionsToUse,
              "composition": product.composition,
              "price": product.price.toString(),
            }
          )
        );
        if(response.statusCode == 201 || response.statusCode == 200){
          return Product.fromJSON(jsonDecode(response.body));
        }
        else{
          throw Exception("Failed!");
        }
    }
    catch(e){
      print(e);
    }
  }

  Future<Product> _futureProduct;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("FitPack"),backgroundColor: Colors.black,),
      body: Container(
        alignment: Alignment.center,
        padding: EdgeInsets.all(8.0),
        child: (_futureProduct == null)?Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _titleController,
                decoration: InputDecoration(hintText: "Enter title"),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _descriptionController,
                decoration: InputDecoration(hintText: "Enter description"),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _directionsController,
                decoration: InputDecoration(hintText: "Enter directions to use"),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _compositionController,
                decoration: InputDecoration(hintText: "Enter Composition"),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                keyboardType: TextInputType.number,
                controller: _priceController,
                decoration: InputDecoration(hintText: "Enter Price"),
              ),
            ),
            RaisedButton(
              color: Colors.yellow,
              child: Text("Submit"),
              onPressed: (){
              setState((){
                Product product = Product(title:_titleController.text,description: _descriptionController.text,directionsToUse: _directionsController.text,composition: _compositionController.text,price: double.parse(_priceController.text));
                print(product);
                _futureProduct = addProduct(product);
              });
            })
          ]
        ):FutureBuilder<Product>(
        future: _futureProduct,
        builder: (context,snapshot){
          if(snapshot.hasData){
            return Column(
              children: <Widget>[
                Text("Added!"),
                Text(snapshot.data.title)
              ]
            );
          }
          else if(snapshot.hasError){
            return Text("${snapshot.error}");
          }
          return CircularProgressIndicator();
        }
      )
      )
    );
  }
}