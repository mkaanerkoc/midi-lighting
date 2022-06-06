class MidiMessage(object):
    # https://www.midi.org/specifications-old/item/table-2-expanded-messages-list-status-bytes
    def __init__(self, message_array):
        self._status = message_array[0][0][0]
        self._data = message_array[0][0][1:]
        self._timestamp = message_array[0][1]

    @property
    def status(self):
        return self._status

    @property
    def note(self):
        return self._data[0]

    @property
    def velocity(self):
        return self._data[1]

    @property
    def timestamp(self):
        return self._timestamp

    def __repr__(self):
        return f"Status :{self.status}, Data : {self._data}, TimeStamp : {self.timestamp}"

    def __str__(self):
        return self.__repr__()
