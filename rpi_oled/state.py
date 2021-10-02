

class ApplicationState:

    def __init__(self, config):
        self.config = config
        self.config.initialize()
        self.settings = self.config.settings
        self.components = self.config.components
        self.component = self.config.initial_component

        self.emit_image = lambda image: None

    def initialize(self, emit_image):
        self.emit_image = emit_image
        self._set_component(self.component)

    def reset(self):
        self.config.initialize()
        self.settings = self.config.settings
        self.components = self.config.components
        self.component = self.config.initial_component
        self.initialize(self.emit_image)

    def update(self, button):
        self.component.update(button)

    def _set_component(self, component):
        self.component.emit_event = lambda event, *args: None
        self.component.unmounted()
        self.component = component
        self.component.emit_event = self._listen_event
        self.component.mounted()

    def _event_image(self, image):
        self.component.image = image
        self.emit_image(image)

    def _event_component(self, id):
        component = self.components[id]
        if isinstance(component, Page):
            component.parent = self.component.id

        self._set_component(component)

    def _event_back(self):
        parent = self.component.parent
        if parent is not None:
            component = self.components[parent]
            self._set_component(component)

    def _event_setting(self, key, value):
        self.settings[key] = value

    def _listen_event(self, event, *args):
        event_map = {
            'image': self._event_image,
            'component': self._event_component,
            'back': self._event_back,
            'setting': self._event_setting
        }
        event_function = event_map.get(event, None)
        if not event_function:
            raise ValueError(f'Invalid event type: "{event}"')
        event_function(*args)
