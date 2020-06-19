import logging

from investing_bot_framework.core.exceptions import ImproperlyConfigured
from investing_bot_framework.core.states import BotState

logger = logging.getLogger(__name__)


class SetupState(BotState):

    from investing_bot_framework.core.states.templates.data_providing_state import DataProvidingState
    transition_state_class = DataProvidingState

    def __init__(self, context):
        super(SetupState, self).__init__(context)

    def run(self) -> None:
        """
        Running the setup state.

        During execution a validation will be performed on:

        - DataProviders
        """

        # Load the settings
        if not self.context.settings.configured:
            raise ImproperlyConfigured(
                "Settings module is not specified, make sure you have setup a investing_bot_framework project and "
                "the investing_bot_framework is valid or that you have specified the settings module in your "
                "manage.py file"
            )


