# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import datetime
# asyncio provides event loops
import asyncio
import warnings
from typing import List, Callable

from botbuilder.schema import (Activity, ActivityTypes,
                               ChannelAccount, ConversationAccount,
                               ResourceResponse, ConversationReference)
from botbuilder.core.turn_context import TurnContext
from botbuilder.core.bot_adapter import BotAdapter


class ConsoleAdapter(BotAdapter):
    """
    Lets a user communicate with a bot from a console window.

    :Example:
    import asyncio
    from botbuilder.core import ConsoleAdapter

    async def logic(context):
        await context.send_activity('Hello World!')

    adapter = ConsoleAdapter()
    loop = asyncio.get_event_loop()
    if __name__ == "__main__":
        try:
            loop.run_until_complete(adapter.process_activity(logic))
        except KeyboardInterrupt:
            pass
        finally:
            loop.stop()
            loop.close()
    """
    def __init__(self, reference: ConversationReference = None):

        #calling method ConsoleAdapter and initializes attributes of ConsoleAdapter class
        super(ConsoleAdapter, self).__init__()
        #setting paramaeters for ConversationReference. Setting ConversationReferences and paarameters = to self.reference
        #ConversationReference defines a particular point in a conversations
        self.reference = ConversationReference(channel_id='console',
                                               user=ChannelAccount(id='user', name='User1'),
                                               bot=ChannelAccount(id='bot', name='Bot'),
                                               conversation=ConversationAccount(id='convo1', name='', is_group=False),
                                               service_url='')

        # Warn users to pass in an instance of a ConversationReference, otherwise the parameter will be ignored.
        if reference is not None and not isinstance(reference, ConversationReference):
            warnings.warn('ConsoleAdapter: `reference` argument is not an instance of ConversationReference and will '
                          'be ignored.')
        else:
            #getattr returns value of the named attribute of an object
            #sets self.reference attributes to initial values
            self.reference.channel_id = getattr(reference, 'channel_id', self.reference.channel_id)
            self.reference.user = getattr(reference, 'user', self.reference.user)
            self.reference.bot = getattr(reference, 'bot', self.reference.bot)
            self.reference.conversation = getattr(reference, 'conversation', self.reference.conversation)
            self.reference.service_url = getattr(reference, 'service_url', self.reference.service_url)
            # The only attribute on self.reference without an initial value is activity_id, so if reference does not
            # have a value for activity_id, default self.reference.activity_id to None
            self.reference.activity_id = getattr(reference, 'activity_id', None)
        # setting _next_id variable to zero
        self._next_id = 0
    #Callable  checks if its able to pass- if pass: is True
    # defining of a courotine function- simultaneous fuctions
    async def process_activity(self, logic: Callable):
        """
        Begins listening to console input.
        :param logic:
        :return:
        """
        while True:
            #user's input is set as variable msg
            msg = input()
            #Nothing happens if the user inputs a blank input
            if msg is None:
                pass
            else:
                #increases _next_id value by one
                self._next_id += 1
                # creating an object for communication with the Bot. Used as an initial message for a new conversation
                activity = Activity(text=msg,
                                    channel_id='console',
                                    #Uniquely identifies ID of user and their name
                                    from_property=ChannelAccount(id='user', name='User1'),
                                    #identifies the bot as recipient and their name as Bot
                                    recipient=ChannelAccount(id='bot', name='Bot'),
                                    #identification of the conversation
                                    conversation=ConversationAccount(id='Convo1'),

                                    type=ActivityTypes.message,
                                    timestamp=datetime.datetime.now(),
                                    id=str(self._next_id))
                #send to the bot
                activity = TurnContext.apply_conversation_reference(activity, self.reference, True)
                context = TurnContext(self, activity)
                # output of the function
                #logs message from user
                await self.run_middleware(context, logic)

    async def send_activities(self, context: TurnContext, activities: List[Activity]):
        """
        Logs a series of activities to the console.
        :param context:
        :param activities:
        :return:
        """
        #makes sure that there is something in context
        if context is None:
            raise TypeError('ConsoleAdapter.send_activities(): `context` argument cannot be None.')
        #Makes sure that activities is a list, in JSON format
        if type(activities) != list:
            raise TypeError('ConsoleAdapter.send_activities(): `activities` argument must be a list.')
        #Makes sure that there is something inside the list
        if len(activities) == 0:
            raise ValueError('ConsoleAdapter.send_activities(): `activities` argument cannot have a length of 0.')

        async def next_activity(i: int):
            responses = []

            if i < len(activities):
                #adds to list a new resource - ResourceResponse() defines a new resorce
                responses.append(ResourceResponse())

                # var a is set to the object in the activities JSON at the given iteration
                a = activities[i]

                if a.type == 'delay':
                    # .sleep suspends execution for the amount of time at a.delay
                    await asyncio.sleep(a.delay)
                    # return to the beginning of function at next i value
                    await next_activity(i + 1)
                # elif checks responds if there is a message
                elif a.type == ActivityTypes.message:
                    # Checks if there are attachments and if the length of the the attachments is greater than zero
                    if a.attachments is not None and len(a.attachments) > 0:
                        print("there's an attatchment")
                        append = '(1 attachment)' if len(a.attachments) == 1 else f'({len(a.attachments)} attachments)'
                        print(f'{a.text} {append}')
                    else:
                        print(a.text)
                    # after going through either if or else, param for next_activity will increase by 1
                    await next_activity(i + 1)
                else:
                    print(f'[{a.type}]')
                    await next_activity(i + 1)
            # if i is larger than the length of the activities list, it will return what is in the response list
            else:
                return responses
        #returns next_activity param,i, back to zero
        await next_activity(0)

    async def delete_activity(self, context: TurnContext, reference: ConversationReference):
        """
        Not supported for the ConsoleAdapter. Calling this method or `TurnContext.delete_activity()`
        will result an error being returned.
        :param context:
        :param reference:
        :return:
        """
        raise NotImplementedError('ConsoleAdapter.delete_activity(): not supported.')

    async def update_activity(self, context: TurnContext, activity: Activity):
        """
        Not supported for the ConsoleAdapter. Calling this method or `TurnContext.update_activity()`
        will result an error being returned.
        :param context:
        :param activity:
        :return:
        """
        raise NotImplementedError('ConsoleAdapter.update_activity(): not supported.')
