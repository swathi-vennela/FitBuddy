import 'dart:convert';
import 'package:fitpack/models/programs.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ProgramsListView extends StatelessWidget {

  List<Program> getProgramList(List data){
    List<Program> programs = List<Program>();
    for(int i=0;i < data.length; i++){
      Program program = Program(
        title: data[i]["title"],
        category: data[i]["category"],
        description: data[i]["description"],
        hours_per_session: data[i]["hours_per_session"],
        number_of_sessions: data[i]["number_of_sessions"],
        price: data[i]["price"],
      );
      programs.add(program);
    }
    return programs;
  }

  Future< List<Program> > getPrograms() async{
    try{
      final String url = "http://10.0.2.2:8000/programs";
      final response = await http.get(url);
      if(response.statusCode == 200){
        var data = jsonDecode(response.body);
        List<Program> programs = getProgramList(data);
        return programs;
      }
      else{
        throw Exception("Failed to load data!!");
      }
    }
    catch(e){
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("FitPack"),
        backgroundColor: Colors.black,
      ),
      body: FutureBuilder(
        future: getPrograms(),
        builder: (BuildContext context, AsyncSnapshot<List> snapshot){
          if(!snapshot.hasData){
            return CircularProgressIndicator();
          }
          List programs = snapshot.data;
          return Container(
            child: ListView.builder(
              itemCount: programs.length,
              itemBuilder: (context,index){
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
                          title: Text(programs[index].title),
                          subtitle: Text(programs[index].description),
                        ),
                        ButtonBar(
                            children: <Widget>[
                              FlatButton(child: Text("More"),onPressed: (){
                                // Navigator.pushReplacement(context, MaterialPageRoute(builder: (context)=>ProductDetailView(this.products[index])));
                              },)
                            ]
                          ),
                      ],
                    )
                  )
                );
              },
            ),
          );
        },
      ),
    );
  }
}