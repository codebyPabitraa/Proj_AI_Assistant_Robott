from datetime import datetime


class EventBus:

    def __init__(self):

        self.events = []

    def publish(self, event: str):

        self.events.append(

            {

                "timestamp": datetime.now().isoformat(),

                "event": event

            }

        )

    def get_events(self):

        return self.events[-50:]