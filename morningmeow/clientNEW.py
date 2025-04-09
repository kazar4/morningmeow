#!/usr/bin/env python

# WS server that sends messages at random intervals

import traceback
import sys

import asyncio

import websockets as websockets

import fileManage2
import lookup
import myapp

import ssl

import time as t

import stripe

from util import readAuthFiles

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

server_crt_path = readAuthFiles("./authFiles.txt")["server_crt_path"]
server_key_path = readAuthFiles("./authFiles.txt")["server_key_path"]

ssl_context.load_cert_chain(server_crt_path, server_key_path)

stripe.api_key = readAuthFiles("./authFiles.txt")["stripe_secret_key"]

#remember to add handlers for errors to send back if something weird happens

async def time(websocket, path):
    while True:
        #try:
            #now = datetime.datetime.utcnow().isoformat() + "Z"
            #print("It go here")
            # number = int(await websocket.recv())
            number = await websocket.recv()
            preimumVal = await websocket.recv() #'NP' vs 'P'
            clientIntentVal = await websocket.recv()
            #print("phone number: " + str(number))
            numberPresent = fileManage2.checkNumber(number)
            Carrier = "none"
            needPreimum = True
            ID = "none"
            #print(str(number) + " needs premium: " + str(needPreimum))

            socketRun = False;

            try:
                if (numberPresent):
                    fileManage2.cancelPaymentAndRemove(clientIntentVal)
                    raise Exception('1')
                elif (preimumVal == 'P'):
                    #Code for checking that they actually have premium
                    t_end = t.time() + 60 * 0.2
                    while t.time() < t_end:
                        foundPayIntent = fileManage2.checkConfirmedPaymentIntent(clientIntentVal)
                        print(foundPayIntent, clientIntentVal)
                        if foundPayIntent:

                            ID = fileManage2.getConfirmedPaymentIntentID(clientIntentVal)
                            print("Trying to confirm payment with: " + ID)

                            if (ID != ""):
                                try:

                                    intent = stripe.PaymentIntent.capture(
                                        ID,
                                        amount_to_capture=40000
                                    )
                                except:
                                    intent = stripe.PaymentIntent.cancel(ID)
                                    raise Exception('6')

                            fileManage2.removeConfirmedPaymentIntent(clientIntentVal)
                            raise Exception('3')

                    raise Exception('5')
                cacheCarrier = fileManage2.checkPhoneCache(number)
                if (cacheCarrier != None):
                    print("Found {} in the cache".format(number))
                    Carrier = cacheCarrier[1]
                else:
                    print("Could not find {} in the cache".format(number))
                    Carrier = lookup.look(number)
                    fileManage2.addPhoneCache(number, Carrier)

                needPreimum = not (Carrier in fileManage2.listOfCarriersNoPremium)

                #needPremium is the only boolean that matters here as premiumVal has already been checked
                if (needPreimum and (preimumVal == 'NP')):
                    raise Exception('2')
                else:
                    raise Exception('3')

            except Exception as inst:
                print(traceback.format_exc())
                value = inst.args[0]
                print("value for {} is {}".format(number, value))
                await websocket.send(value)
                socketRun = True if value == '3' else False

            if (socketRun):
                #number = int(await websocket.recv())
                number = await websocket.recv()
                name = await websocket.recv()
                message = await websocket.recv()
                maxCharLength = 900;
                message = (message[:maxCharLength]) if len(message) > maxCharLength else message
                timezone = await websocket.recv()
                carrier = Carrier
                premium = await websocket.recv()

                print("Adding {} to Database".format(number))
                fileManage2.addData(number, name, message, timezone, carrier, premium, ID)

            #await websocket.send(sendback)
            #await websocket.close()
            #await websocket.send(now)
            #await asyncio.sleep(random.random() * 3)
        # except Exception as inst:
        #     print(type(inst))  # the exception instance
        #     print(inst)
        #     await websocket.send("4")
        # finally:
        #     try:
        #         await websocket.wait_closed()
        #     except:
        #         print("trouble closing websocket")



start_server = websockets.serve(time, "198.251.68.90", 5678, ssl=ssl_context)
#198.251.68.90
#127.0.0.1
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
