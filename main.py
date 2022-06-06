from phue import Bridge
from pygame import midi

from hue_commands import (
    Command,
)

from midi_message import (
    MidiMessage
)

from constants import (
    START_BUTTON,
    STOP_BUTTON
)


class Potentiometer(object):
    _last_change_time = -1
    _last_value = -1

    def get_delta_change(self, message: MidiMessage):
        if message.timestamp - self._last_change_time > 5000:
            delta = 0
        else:
            delta = message.velocity - self._last_value

        self._last_value = message.velocity
        self._last_change_time = message.timestamp
        return delta


class Application(object):
    _bridge_ip = '192.168.178.157'
    _hue_bridge = None
    _midi_device = None
    _potentiometer = None

    def setup(self):
        self._setup_hue_bridge()
        self._setup_midi_device()

    def _setup_hue_bridge(self):
        self._hue_bridge = Bridge(self._bridge_ip)
        self._hue_bridge.connect()
        self._hue_bridge.get_api()
        print(f"HUE Bridge is connected successfully.")
        print(f"Current installed lights:")
        for light in self._hue_bridge.lights:
            print(f"Name: {light.name}, ID: {light.light_id}")
            light.brightness = 0

    def _setup_midi_device(self):
        midi.init()
        default_id = midi.get_default_input_id()
        print(f'Default ID for MIDI device is {default_id}')
        self._midi_device = midi.Input(device_id=default_id)
        self._potentiometer = Potentiometer()

    def _process_midi_message(self, message: MidiMessage):
        if message.note == 90:
            return Command(self._hue_bridge.set_light, light_id=1, parameter='bri', value=254)
        if message.note == 7:
            _delta = self._potentiometer.get_delta_change(message)
            light_ids = [light.light_id for light in self._hue_bridge.lights]
            current_brightness = self._hue_bridge.lights[0].brightness
            new_brightness = current_brightness + _delta * 2
            print(f'new brightness : {new_brightness}')
            return Command(self._hue_bridge.set_light, light_id=light_ids, parameter='bri', value=new_brightness)
        elif message.note == START_BUTTON:
            light_ids = [light.light_id for light in self._hue_bridge.lights]
            return Command(self._hue_bridge.set_light, light_id=light_ids, parameter='on', value=True)
        elif message.note == STOP_BUTTON:
            light_ids = [light.light_id for light in self._hue_bridge.lights]
            return Command(self._hue_bridge.set_light, light_id=light_ids, parameter='on', value=False)
        else:
            return Command(None)

    def run(self):
        try:
            while True:
                if self._midi_device.poll():
                    _midi_message = MidiMessage(self._midi_device.read(num_events=4))
                    print(_midi_message)
                    command_to_execute = self._process_midi_message(_midi_message)
                    command_to_execute.execute()
        except KeyboardInterrupt as err:
            print("Stopping...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = Application()
    app.setup()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
