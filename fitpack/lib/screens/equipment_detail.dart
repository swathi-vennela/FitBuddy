import 'package:fitpack/models/product.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ProductDetailView extends StatefulWidget {
  Product product;
  ProductDetailView(this.product);
  @override
  _ProductDetailViewState createState() => _ProductDetailViewState(this.product);
}

class _ProductDetailViewState extends State<ProductDetailView> {

  Product product;

  _ProductDetailViewState(this.product);


  // Future<Product> _deleteProduct(String title) async{
  //   try{
  //     final String url = "http://10.0.2.2:8000/ads/fitness-product-list";
  //     final response = await http.delete(url,
  //       headers: <String,String>{
  //         "Content-Type": "application/json;charset=UTF-8",
  //       }
  //     );
  //     if(response.statusCode == 200){
  //       return Product.fromJSON(jsonDecode(response.body));
  //     }
  //     else{
  //       throw Exception("Failed!!!");
  //     }
  //   }
  //   catch(e){
  //     print(e);
  //   }
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("FitPack"),
        backgroundColor: Colors.black,
      ),
      body: Container(
      child: Column(
        children: <Widget>[
          SizedBox(height: 20),
          Text(this.product.title),
          SizedBox(height: 20),
          Image.asset("assets/images/temp.jpg"),
          SizedBox(height: 20),
          Text(this.product.description),
          Text(this.product.price.toString()),
          ButtonBar(
            children: <Widget>[
              FlatButton(
                onPressed: (){},
                child: Text("Edit")
              ),
              FlatButton(
                onPressed: (){
                  // _deleteProduct(this.product.title);
                },
                child: Text("Delete")
              ),
            ]
          )
        ]
      ),
    ),
    );
  }
}