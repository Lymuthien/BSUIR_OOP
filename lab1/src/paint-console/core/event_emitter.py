from interfaces import EventBus


class EventEmitter(EventBus):
    def __init__(self):
        self.__subscribers = {}

    def on(self, event_type: str, callback: callable):
        """Subscribe on an event."""
        if event_type not in self.__subscribers:
            self.__subscribers[event_type] = []
        self.__subscribers[event_type].append(callback)

    def off(self, event_type: str, callback: callable):
        """Unsubscribe from an event."""
        if event_type in self.__subscribers:
            self.__subscribers[event_type].remove(callback)

    def emit(self, event_type: str, *data):
        """Initiates an event and broadcasts data to all subscribers."""
        if event_type in self.__subscribers:
            for callback in self.__subscribers[event_type]:
                try:
                    callback(*data)
                except Exception as e:
                    print(f"Error in callback {callback}: {e}")
