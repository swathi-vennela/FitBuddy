import 'package:flutter/material.dart';

class ProductListView extends StatefulWidget {
  @override
  _ProductListViewState createState() => _ProductListViewState();
}

// Dont forget to add the empty screen in the conditionals while integrating with the api
class _ProductListViewState extends State<ProductListView> {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
      appBar: AppBar(
        title: Text("FitPack"),
        bottom: TabBar(
          tabs: [
            Tab(child: Text("Your Products")),
            Tab(child: Text("Sold Products")),
          ],
        ),
      ),
      endDrawer: Drawer(),
      floatingActionButton: FloatingActionButton(
        onPressed: null,
        child: Icon(
          Icons.add,
          size: 30,
        ),
      ),
      body: TabBarView(
        children: [
          ProductList(),
          SoldProducts()
        ],
      ),
    ),
    );
  }
}

class ProductList extends StatefulWidget {
  @override
  _ProductListState createState() => _ProductListState();
}

class _ProductListState extends State<ProductList> {

  Widget _slideAtIndex(int index){
    return Card(
      child: Row(
        children: [
          Image.asset("assets/images/temp.jpg")
        ],
      )
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: ListView.builder(
        itemCount: 2,
        itemBuilder: (context,index){
          return _slideAtIndex(index);
        },
      ),
    );
  }
}

class SoldProducts extends StatefulWidget {
  @override
  _SoldProductsState createState() => _SoldProductsState();
}

class _SoldProductsState extends State<SoldProducts> {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text("Sold!"),
    );
  }
}