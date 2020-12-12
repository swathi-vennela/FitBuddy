class Program{
  String title;
  String category;
  int number_of_sessions;
  double hours_per_session;
  int price;
  String description;

  Program({this.title,this.category,this.number_of_sessions,this.hours_per_session,this.price,this.description});
  factory Program.fromJSON(Map<String, dynamic> json){
    return Program(
      title: json["title"],
      category: json["category"],
      number_of_sessions: json["number_of_sessions"],
      hours_per_session: json["hours_per_session"],
      price: json["price"],
      description: json["description"]
    );
  }
}