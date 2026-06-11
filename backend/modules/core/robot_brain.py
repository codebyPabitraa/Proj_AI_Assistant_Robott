from backend.modules.core.state_manager import StateManager
from backend.modules.core.event_bus import EventBus

from backend.utils.config_loader import config
from backend.utils.logger import logger


class RobotBrain:
    """
    Central controller for the AI Assistant Robot.

    All modules communicate through RobotBrain.
    """

    def __init__(self):

        logger.info("Initializing RobotBrain...")

        # Configuration
        self.settings = config.get_settings()
        self.models = config.get_models()

        # Core Components
        self.state_manager = StateManager()
        self.event_bus = EventBus()

        # Runtime Information
        self.current_user = None
        self.session_id = None

        # Module Registry
        self.modules = {}

        # Service Registry
        self.services = {}

        logger.info("RobotBrain initialized successfully.")

    def startup(self):

        logger.info("Robot startup sequence initiated.")

        self.state_manager.set_state("starting")

        self.event_bus.publish("Robot Booting")

        self.state_manager.set_state("idle")

        self.event_bus.publish("Robot Ready")

        logger.info("Robot is ready.")

    def register_module(self, name: str, module):

        self.modules[name] = module

        logger.info(f"Module registered: {name}")

    def register_service(self, name: str, service):

        self.services[name] = service

        logger.info(f"Service registered: {name}")

    def get_status(self):

        return {

            "state": self.state_manager.get_state(),

            "registered_modules": list(self.modules.keys()),

            "registered_services": list(self.services.keys()),

            "events": self.event_bus.get_events(),

            "session_id": self.session_id,

            "current_user": self.current_user,

            "settings_loaded": True,

            "models_loaded": True

        }