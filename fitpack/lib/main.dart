import 'package:fitpack/screens/equipment_list.dart';
import 'package:fitpack/screens/view_programs.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FitPack',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
        // This makes the visual density adapt to the platform that you run
        // the app on. For desktop platforms, the controls will be smaller and
        // closer together (more dense) than on mobile platforms.
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MyHomePage(title: 'FitPack'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
 
  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        title: Text("FitStore"),
        backgroundColor: Colors.black,
      ),
      body: Container(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              // width: 200,
              margin: EdgeInsets.all(8),
              height: 150,
              child: Card(
                color: Colors.yellow,
                elevation: 7,
                child: Column(
                  children: [
                    Text("Are you a store or client looking to sell fitness equipments or products?",style: TextStyle(fontSize: 20),),
                    RaisedButton(onPressed: (){
                      Navigator.push(context, MaterialPageRoute(builder: (context)=>ProductListView()));
                    },
                    child: Text("Head Over Here!",style: TextStyle(color: Colors.white),),
                    color: Colors.black
                    )
                  ],
                )
              )
            ),
            Container(
              // width: 200,
              margin: EdgeInsets.all(8),
              height: 150,
              child: Card(
                color: Colors.yellow,
                elevation: 7,
                child: Column(
                  children: [
                    Text("Are you a trainer or a trainee looking for fitness programs?",style: TextStyle(fontSize: 20),),
                    RaisedButton(onPressed: (){
                      Navigator.push(context, MaterialPageRoute(builder: (context)=>ProgramsListView()));
                    },
                    child: Text("Head Over Here!",style: TextStyle(color: Colors.white),),
                    color: Colors.black
                    )
                  ],
                )
              )
            )
          ],
        ),
      ),
    );
  }
}
