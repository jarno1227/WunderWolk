import 'dart:ffi';

class Settings {
  final String mode;
  final int refresh_interval;
  final int future_forecast_time;
  final int brightness;
  final List<String> subjects;
  final List<double> location;

  Settings(this.mode, this.refresh_interval, this.future_forecast_time,
      this.brightness, this.subjects, this.location);

  Settings.fromJson(Map<String, dynamic> json)
      : mode = json['mode'],
        refresh_interval = json['refresh_interval'],
        future_forecast_time = json['future_forecast_time'],
        brightness = json['brightness'],
        subjects = json['subjects'].cast<String>(),
        location = [80.000, 5.050113150625251]; //json['location'];

  Map<String, dynamic> toJson() => {
        'mode': mode,
        'refresh_interval': refresh_interval,
        'future_forecast_time': future_forecast_time,
        'brightness': brightness,
        'subjects': stringListToString(subjects),
        'location': doubleListToString(location)
      };

  String stringListToString(List<String> list) {
    String stringOfList = "";
    list.forEach((item) {
      if (list.length - 1 != list.indexOf(item)) {
        stringOfList += item + ",";
      } else {
        stringOfList += item;
      }
    });
    return stringOfList;
  }

  String doubleListToString(List<double> list) {
    String stringOfList = "";
    list.forEach((item) {
      if (list.length - 1 != list.indexOf(item)) {
        stringOfList += item.toString() + ",";
      } else {
        stringOfList += item.toString();
      }
    });
    return stringOfList;
  }
}
