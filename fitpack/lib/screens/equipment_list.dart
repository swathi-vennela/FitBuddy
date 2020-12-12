import 'dart:convert';
import 'package:fitpack/models/product.dart';
import 'package:fitpack/screens/add_product.dart';
import 'package:fitpack/screens/equipment_detail.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';

class ProductListView extends StatefulWidget {
  @override
  _ProductListViewState createState() => _ProductListViewState();
}

// Dont forget to add the empty screen in the conditionals while integrating with the api
class _ProductListViewState extends State<ProductListView> {

  Future< List<Product> > products;

  List<Product> getProductList(List data){
    List<Product> products = new List<Product>();
    for(int i=0;i < data.length;i++){
      String title = data[i]["title"];
      String description = data[i]["description"];
      String directionsToUse = data[i]["directions_to_use"];
      String composition = data[i]["composition"];
      double price = data[i]["price"];
      Product product = Product(
        title: title,
        description: description,
        directionsToUse: directionsToUse,
        composition: composition,
        price: price
      );
      products.add(product);
    }
    
    return products;
  }

  Future< List<Product> > getProducts() async {
    print("here");
    try{
      final String url = "http://10.0.2.2:8000/ads/fitness-product-list";
      final response = await http.get(url);
      print("here and");
      print(response);
      if(response.statusCode == 200){
        var data = jsonDecode(response.body);
        print(data);
        List<Product> products = getProductList(data);
        return products;
      }
      else{
        throw Exception("Failed to load!");
      }
    }
    catch(e){
      print(e);
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: getProducts(),
      builder: (BuildContext context, AsyncSnapshot<List> snapshot){
        if(!snapshot.hasData){
          return Scaffold(
            body: CircularProgressIndicator(),
          );
        }
        List products = snapshot.data;
        return Scaffold(
          appBar: AppBar(
            title: Text("FitPack"),
            backgroundColor: Colors.black,
          ),
          endDrawer: Drawer(
            child: ListView(
              children: <Widget>[
                DrawerHeader(
                  child: Text("Drawer Header"),
                  decoration: BoxDecoration(
                    color: Colors.yellow[50]
                  ),
                ),
                ListTile(
                  title: Text("Profile"),
                  onTap: (){}
                ),
                ListTile(
                  title: Text("Products"),
                  onTap: (){}
                ),
                ListTile(
                  title: Text("Stats"),
                  onTap: (){}
                ),
                ListTile(
                  title: Text("Sign Out"),
                  onTap: (){}
                ),
              ]
            ),
          ),
          floatingActionButton: FloatingActionButton(
            onPressed: (){
              Navigator.push(context, MaterialPageRoute(builder: (context)=>AddProduct()));
            },
            child: Icon(
              Icons.add,
              size: 30,
            ),
            backgroundColor: Colors.black,
          ),
          body: ProductList(products),
        );
      },
    );
  }
}

class ProductList extends StatefulWidget {
  final List<Product> products;
  ProductList(this.products);
  @override
  _ProductListState createState() => _ProductListState(this.products);
}

class _ProductListState extends State<ProductList> {
    List<Product> products;
  _ProductListState(this.products);

  Widget _slideAtIndex(int index){
    return Container(
      width: 200,
      height: 150,
      child: Card(
        color: Colors.yellow,
        elevation: 7,
        child: Column(
          children: [
            // Image.asset("assets/images/temp.jpg")
            ListTile(
              leading: Image.asset("assets/images/temp.jpg"),
              title: Text(this.products[index].title),
              subtitle: Text(this.products[index].description),
            ),
            ButtonBar(
                children: <Widget>[
                  FlatButton(child: Text("More"),onPressed: (){
                    Navigator.push(context, MaterialPageRoute(builder: (context)=>ProductDetailView(this.products[index])));
                  },)
                ]
              ),
          ],
        )
      )
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: ListView.builder(
        itemCount: this.products.length,
        itemBuilder: (context,index){
          return _slideAtIndex(index);
        },
      ),
    );
  }
}