import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'WünderWolk app',
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
        primaryColor: Color(0xff1B4060),
        primarySwatch: Colors.indigo,
      ),
      home: WeatherMode(),
    );
  }
}

class WeatherMode extends StatefulWidget {
  @override
  _WeatherMode createState() => _WeatherMode();
}

final controller = PageController(initialPage: 0);

class _WeatherMode extends State<WeatherMode> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Image.asset(
          'assets/Logo_Wunderwolk.png',
          fit: BoxFit.cover,
          width: 80,
        ), //Text(widget.title),
      ),
      body: Center(
          child: PageView(
        scrollDirection: Axis.horizontal,
        controller: controller,
        children: [
          Center(
            child: Column(
              //mainAxisAlignment: MainAxisAlignment.center,
              children: [
                TitleSection('Weather Mode', 42),
                TitleSection('🌥', 200)
              ],
            ),
          ),
          Center(
            child: Column(
              //mainAxisAlignment: MainAxisAlignment.center,
              children: [
                TitleSection('Mood Mode', 42),
                TitleSection('😄', 200)
              ],
            ),
          ),
        ],
      )),
    );
  }
}

Widget textSection = Container(
  padding: const EdgeInsets.all(32),
  child: Text(
    'Lake Oeschinen lies at the foot of the Blüemlisalp in the Bernese '
    'Alps. Situated 1,578 meters above sea level, it is one of the '
    'larger Alpine Lakes. A gondola ride from Kandersteg, followed by a '
    'half-hour walk through pastures and pine forest, leads you to the '
    'lake, which warms to 20 degrees Celsius in the summer. Activities '
    'enjoyed here include rowing, and riding the summer toboggan run.',
    softWrap: true,
  ),
);

class TitleSection extends StatelessWidget {
  final String title;
  final double size;

  const TitleSection(this.title, this.size);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(top: 10.0),
      child: Text(
        title,
        style: TextStyle(fontWeight: FontWeight.bold, fontSize: size),
      ),
    );
  }
}
