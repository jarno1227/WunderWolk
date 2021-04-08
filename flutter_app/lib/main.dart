import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:flutter_app/mqtt_client.dart';
import 'package:cupertino_setting_control/cupertino_setting_control.dart';
import 'package:flutter_swipe_action_cell/flutter_swipe_action_cell.dart';

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
      home: WunderWolkModes(),
    );
  }
}

class WunderWolkModes extends StatefulWidget {
  @override
  _WunderWolkModes createState() => _WunderWolkModes();
}

class _WunderWolkModes extends State<WunderWolkModes> {
  MqttClient client;
  var topic = "topic/test";

  void _publish(String message) {
    final builder = MqttClientPayloadBuilder();
    builder.addString('Hello from flutter_client');
    client?.publishMessage(topic, MqttQos.atLeastOnce, builder.payload);
  }

  final controller = PageController(initialPage: 0);
  double _brightnessValue = 100;
  double _forecastTimeValue = 1;

  updateForecastTime(double data) {
    setState(() {
      _forecastTimeValue = data;
    });
  }

  updateBrightness(double data) {
    setState(() {
      _brightnessValue = data;
    });
  }

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
                TitleSection('🌥', 200),
                Spacer(),
                SettingsSlider('Weather forecast time', ' hour(s)', 1, 24,
                    _forecastTimeValue, updateForecastTime),
                TestDropdown(),
                Container(
                  margin: EdgeInsets.only(bottom: 50),
                  child: SettingsSlider('Brightness', '%', 10, 100,
                      _brightnessValue, updateBrightness),
                )
              ],
            ),
          ),
          Center(
            child: Column(
              //mainAxisAlignment: MainAxisAlignment.center,
              children: [
                TitleSection('Mood Mode', 42),
                TitleSection('😄', 200),
                Spacer(),
                SubjectButton(),
                Container(
                  margin: EdgeInsets.only(bottom: 50),
                  child: SettingsSlider('Brightness', '%', 10, 100,
                      _brightnessValue, updateBrightness),
                )
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

class TestDropdown extends StatelessWidget {
  String _tempType = "°C";

  void onTempTypeChange(String data) {}

  @override
  Widget build(BuildContext context) {
    return new SettingRow(
      rowData: SettingsDropDownConfig(
          title: 'Temperature type',
          initialKey: _tempType,
          choices: {
            '°': '°C',
            '°F': '°F',
          }),
      onSettingDataRowChange: onTempTypeChange,
      config: const SettingsRowConfiguration(
          showAsTextField: false,
          showTitleLeft: true,
          showAsSingleSetting: false),
    );
  }
}

class SettingsSlider extends StatelessWidget {
  final String sliderTitle;
  final String sliderUnit;
  final double sliderStartValue;
  final double sliderEndValue;
  final double sliderInitialValue;
  final updateValue;

  const SettingsSlider(this.sliderTitle, this.sliderUnit, this.sliderStartValue,
      this.sliderEndValue, this.sliderInitialValue, this.updateValue);

  @override
  Widget build(BuildContext context) {
    return new SettingRow(
      rowData: SettingsSliderConfig(
        title: sliderTitle,
        from: sliderStartValue,
        to: sliderEndValue,
        initialValue: sliderInitialValue,
        justIntValues: true,
        unit: sliderUnit,
      ),
      onSettingDataRowChange: updateValue,
      config: SettingsRowConfiguration(
          showAsTextField: false,
          showTitleLeft: true,
          showTopTitle: false,
          showAsSingleSetting: false),
    );
  }
}

class SubjectButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new SettingRow(
      rowData: SettingsButtonConfig(
        title: 'Manage topic',
        tick: true,
        functionToCall: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => ManageTopicsPage()),
          );
        },
      ),
      config: const SettingsRowConfiguration(
          showAsTextField: false,
          showTitleLeft: true,
          showTopTitle: false,
          showAsSingleSetting: false),
    );
  }
}

class ManageTopicsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Manage topics"),
      ),
      body: Center(
        child: SubjectList(),
      ),
    );
  }
}

class SubjectList extends StatefulWidget {
  @override
  _SubjectList createState() => _SubjectList();
}

class _SubjectList extends State<SubjectList> {
  final List<String> entries = <String>[
    'Max Verstappen',
    'Red Bull',
    'Formula 1',
    'Bahrain'
  ];

  void updateEntries(int index) {
    entries.removeAt(index);
  }

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(8),
      itemCount: entries.length,
      itemBuilder: (BuildContext context, int index) {
        return SwipeActionCell(
          key: ObjectKey(entries[index]),

          ///this key is necessary
          trailingActions: <SwipeAction>[
            SwipeAction(
                title: "delete",
                onTap: (CompletionHandler handler) async {
                  updateEntries(index);
                  setState(() {});
                },
                color: Colors.red),
          ],
          child: Container(
            height: 50,
            child: Center(child: Text('${entries[index]}')),
          ),
        );
      },
      separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }
}
