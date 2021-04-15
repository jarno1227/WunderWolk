import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:flutter_app/mqtt_client.dart';
import 'package:cupertino_setting_control/cupertino_setting_control.dart';
import 'package:flutter_swipe_action_cell/flutter_swipe_action_cell.dart';
import 'package:flutter_app/settings.dart';

void main() {
  MqttClient client;
  String mqttTopicPublish = "pacotinie@gmail.com/rpi";
  String mqttTopicSubscribe = "pacotinie@gmail.com/app";
  Settings settings;

  void _publish(String message) {
    final builder = MqttClientPayloadBuilder();
    builder.addString(message);
    client?.publishMessage(
        mqttTopicPublish, MqttQos.atLeastOnce, builder.payload);
  }

  void init() async {
    await connect().then((value) {
      client = value;
    });
    client?.subscribe(mqttTopicSubscribe, MqttQos.atLeastOnce);
    _publish('request|settings');
    client?.onSubscribed(mqttTopicSubscribe);

    client.updates.listen((List<MqttReceivedMessage<MqttMessage>> c) {
      final MqttPublishMessage message = c[0].payload;
      final payload =
          MqttPublishPayload.bytesToStringAsString(message.payload.message);
      if (c[0].topic == mqttTopicSubscribe) {
        settings = Settings.fromJson(jsonDecode(payload.replaceAll("'", '"')));
      }
      runApp(MyApp(
          client, mqttTopicPublish, mqttTopicSubscribe, _publish, settings));
    });
  }

  init();
}

class MyApp extends StatelessWidget {
  final MqttClient client;
  final String mqttTopicPublish;
  final String mqttTopicSubscribe;
  final _publish;
  final Settings settings;

  const MyApp(this.client, this.mqttTopicPublish, this.mqttTopicSubscribe,
      this._publish, this.settings);
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
      home: WunderWolkModes(
          client,
          mqttTopicPublish,
          mqttTopicSubscribe,
          _publish,
          settings,
          PageController(initialPage: settings?.mode == "weather" ? 0 : 1)),
    );
  }
}

class WunderWolkModes extends StatefulWidget {
  final MqttClient client;
  final String mqttTopicPublish;
  final String mqttTopicSubscribe;
  final _publish;
  final Settings settings;
  final controller;

  const WunderWolkModes(this.client, this.mqttTopicPublish,
      this.mqttTopicSubscribe, this._publish, this.settings, this.controller);

  @override
  _WunderWolkModes createState() => _WunderWolkModes();
}

class _WunderWolkModes extends State<WunderWolkModes> {
  double _brightnessValue = 100;
  double _forecastTimeValue = 1;
  List<String> topics = ['Max Verstappen', 'Red Bull', 'Formula 1', 'Bahrain'];

  updateForecastTime(double data) {
    setState(() {
      _forecastTimeValue = data;
      widget._publish("future_forecast_time|" + (data.round()).toString());
    });
  }

  updateBrightness(double data) {
    setState(() {
      _brightnessValue = data;
      widget._publish("brightness|" + (data.round()).toString());
    });
  }

  //Set values first time the widget gets put in the tree.
  @override
  void initState() {
    topics = widget.settings?.subjects;
    _forecastTimeValue = widget.settings?.future_forecast_time?.toDouble();
    _brightnessValue = widget.settings?.brightness?.toDouble();
    super.initState();
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
        controller: widget.controller,
        onPageChanged: (int page) {
          String modeValue = page == 0 ? "weather" : "social";
          widget._publish("mode|" + modeValue);
        },
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
                SubjectButton(topics, widget._publish),
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
  final dynamic updateValue;

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
  final List<String> topics;
  final _publish;

  const SubjectButton(this.topics, this._publish);

  @override
  Widget build(BuildContext context) {
    return new SettingRow(
      rowData: SettingsButtonConfig(
        title: 'Manage topic',
        tick: true,
        functionToCall: () {
          Navigator.push(
            context,
            MaterialPageRoute(
                builder: (context) => ManageTopicsPage(topics, _publish)),
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

class ManageTopicsPage extends StatefulWidget {
  final List<String> topics;
  final newTopicTextController = TextEditingController();
  final _publish;

  ManageTopicsPage(this.topics, this._publish);

  @override
  _ManageTopicsPage createState() => _ManageTopicsPage();
}

class _ManageTopicsPage extends State<ManageTopicsPage> {
  void publishTopics() {
    String topicString = "";
    widget.topics.forEach((topic) {
      if (widget.topics.length - 1 != widget.topics.indexOf(topic)) {
        topicString += topic + ",";
      } else {
        topicString += topic;
      }
    });
    widget._publish("subjects|" + topicString);
  }

  void updateEntries(int index) {
    widget.topics.removeAt(index);
    setState(() {});
    publishTopics();
  }

  void addNewEntry(String entry) {
    widget.topics.add(entry.replaceAll(RegExp(","), ""));
    setState(() {});
    publishTopics();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Manage topics"),
      ),
      body: Center(
          child: Column(
        children: [
          Container(
              height: 350, child: SubjectList(widget.topics, updateEntries)),
          if (widget.topics.length < 5)
            CupertinoButton(
              child: Text('Add topic'),
              onPressed: () {
                showDialog<bool>(
                  context: context,
                  builder: (context) {
                    return CupertinoAlertDialog(
                        title: Text('Add topic'),
                        content: Card(
                          elevation: 0.0,
                          child: Column(
                            children: <Widget>[
                              CupertinoTextField(
                                controller: widget.newTopicTextController,
                                placeholder: 'Topic you are interested in',
                              ),
                            ],
                          ),
                        ),
                        actions: [
                          CupertinoDialogAction(
                            isDefaultAction: true,
                            child: Text("Cancel"),
                            onPressed: () {
                              //close the dialog
                              Navigator.pop(context);
                              //empty the textfield
                              widget.newTopicTextController.text = "";
                            },
                          ),
                          CupertinoDialogAction(
                            child: Text("Add"),
                            onPressed: () {
                              //update the list state
                              addNewEntry(widget.newTopicTextController.text);
                              //close the dialog
                              Navigator.pop(context);
                              //empty the textfield
                              widget.newTopicTextController.text = "";
                            },
                          )
                        ]);
                  },
                );
              },
            )
        ],
      )),
    );
  }
}

class SubjectList extends StatefulWidget {
  final List<String> topics;
  final updateEntries;

  SubjectList(this.topics, this.updateEntries);

  @override
  _SubjectList createState() => _SubjectList();
}

class _SubjectList extends State<SubjectList> {
  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(8),
      itemCount: widget.topics.length,
      itemBuilder: (BuildContext context, int index) {
        return SwipeActionCell(
          key: ObjectKey(widget.topics[index]),

          ///this key is necessary
          trailingActions: <SwipeAction>[
            SwipeAction(
                title: "delete",
                onTap: (CompletionHandler handler) async {
                  widget.updateEntries(index);
                  setState(() {});
                },
                color: Colors.red),
          ],
          child: Container(
            height: 50,
            child: Center(child: Text('${widget.topics[index]}')),
          ),
        );
      },
      separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }
}
