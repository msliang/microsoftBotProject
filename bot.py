from sys import exit
import http.client, urllib.parse, json, time, sys
class EchoBot():
    async def on_turn(self, context):
        # Check to see if this activity is an incoming message.
        # (It could theoretically be another type of activity.)
        if (context.activity.type == 'message' and context.activity.text):
            # Check to see if the user sent a simple "quit" message.
            if (context.activity.text.lower() == 'quit'):
                # Send a reply.
                await context.send_activity('Bye!')
                exit(0)
            else:
                # Echo the message text back to the user.
                await context.send_activity(f'I heard you say {context.activity.text}')

    async def qnaCaller (self, context):

            host = "qnamakerbotproject-ml.azurewebsites.net";
            # Authorization endpoint key
            # From Publish Page
           # endpoint_key = <INSERT KEY> ;

            # Management APIs postpend the version to the route
            # Part of HOST is prepended to route to work with http library
            route = "/qnamaker/knowledgebases/19dd10f9-a648-4f0c-bfc7-b4cb617090f5/generateAnswer";

            # JSON format for passing question to service
            question = "{'question':'{" + context.activity.text + "}'}"
            #"{'question': {context.activity.text}}"
            headers = {
                'Authorization': 'EndpointKey ' + endpoint_key,
                'Content-Type': 'application/json'
              }

            conn = http.client.HTTPSConnection(host,port=443)
            try:

                conn.request ("POST", route, question, headers)

                response = conn.getresponse ()

                answer = response.read ()

                print(json.dumps(json.loads(answer), indent=4))

            except :
                print ("Unexpected error:", sys.exc_info()[0])
                print ("Unexpected error:", sys.exc_info()[1])
# hiiiiiiiii