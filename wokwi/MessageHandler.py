from MQTT import MQTT
from Message import Message, MessageDestinationError, MessageEchoError
from CommandMessage import CommandMessage
from DataMessage import DataMessage
from NetworkMessage import NetworkMessage
from machine import Timer, Pin
from LogTime import LogTime
from Time import now
from uuid import uuid4
from MatrixSparseDOK import MatrixSparseDOK
from time import sleep

class MessageHandler:
    LED_PIN = 3
    TIMER_PERIOD = 10000
    # In simulator, It gives 20 seconds, but in reality it gives 47 seconds period.
    # If timer period pass 60s in reality, then MQTT server kicks out our node.
    # So that we had to set timer 20 seconds in simulation.

    EDGE_COMP_PERIOD = 12000
    ECHO_PERIOD = 5000

    def __init__(self, matrix_engine, communication_protocol=MQTT):
        Message.CLIENT_ID = communication_protocol.CLIENT_ID # Sharing CLIENT_ID with all message types
        self._is_edge_computing = False
        self._is_edge_computing_done = False
        self._is_echo_received = False
        self._edge_computing_requester = None
        self._edge_computing_matrix = None
        self._edge_computing_receive_id = None

        self._communication_protocol = communication_protocol()
        self._matrix_engine = matrix_engine
        self._communication_protocol.set_callback(self._cmd_receive, self._data_receive, self._net_receive)
        self._timer = Timer(3)
        self._edge_computing_timer = Timer(2) # All the edges must be give response within 1 minute!
        self._echo_timer = Timer(1)  # If node sends a message, it must receive its echo. If not, reconnect (like WDT)
        self._led = Pin(MessageHandler.LED_PIN,Pin.OUT)
        self._led_state = 0

    def initialize(self):
        print("Start")
        self._communication_protocol.connect()
        self._send_alive()
        self._timer.init(period=MessageHandler.TIMER_PERIOD, callback=self._send_alive)

    def run(self):
        self._communication_protocol.run()

    def reconnect(self):
        """ WokWi aborts connection when you open different application. Hence, connection gets lost.
            We tried reconnection by disconnecting and connecting. However, it did not work for WokWi.
            Therefore, we reset the ESP32 in a fail of connection.
            Reset is not working. When we reset, device keeps resetting.
        """
        print("Need to  reconnect. Please Reset WokWi.")
        # Save the current Log

    def stop(self):
        self._communication_protocol.disconnect()

    def _cmd_receive(self, message_str):
        """ Handle messages coming from CMD topic. """
        try:
            message = CommandMessage(message_str)

            if message.cmd == "GET-ALL-LOG-FULL":
                self._edge_computing_requester = message.source_node_id
                self._edge_computing_id = message.message_id
                # Read its log before requesting other matrices
                self._edge_computing_matrix = self._matrix_engine.read_one_day(message.day)

                self._is_edge_computing = True # Receive incoming data and sum them all.

                self._request_all_log(message.day)
                self._edge_computing_timer.init(period=MessageHandler.EDGE_COMP_PERIOD, mode=Timer.ONE_SHOT,
                                                callback=self._edge_computing_done)

            else:
                data = None
                if message.cmd == 'GET-NODE-LOG-FULL':
                    print("[DEBUG]: LOG FULL")
                    try:
                        data = self._matrix_engine.read_one_day(message.day).compress()
                    except ValueError:
                        data = "Sparsity < 0.5"
                elif message.cmd == "GET-NODE-LOG-BY-HOUR":
                    print("[DEBUG]: LOG HOUR")
                    try:
                        data = self._matrix_engine.read_one_hour(message.day, message.hour).compress()
                    except ValueError:
                        data = "Sparsity < 0.5"
                elif message.cmd == "GET-NODE-LOG-BY-MINUTE":
                    print("[DEBUG]: LOG MINUTE")
                    try:
                        data = self._matrix_engine.read_one_minute(message.day, message.minute).compress()
                    except ValueError:
                        data = "Sparsity < 0.5"

                response = MessageHandler._create_response(message.cmd, data, message.source_node_id, message.message_id)
                self._communication_protocol.send_data(str(response))

        except MessageDestinationError:
            # Do nothing, wrong node (This node is not supposed to reply
            print("[DEBUG]: Wrong Source")
            return None
        except MessageEchoError:
            self._is_echo_received = True
        except ValueError as err:
            print(err)

    def _data_receive(self, message_str):
        """ Handle messages coming from DATA topic. """
        try:
            if not self._is_edge_computing:
                if self._is_edge_computing_done:
                    # Echo
                    self._is_echo_received = True
                    self._is_edge_computing_done = False
                return None

            message = DataMessage(message_str)

            if message.source_node_id == Message.CLIENT_ID:
                # Echo Message
                self._is_echo_received = True
                return None

            if message.message_id != self._edge_computing_receive_id:
                # Wrong Message ID response
                return None
            # Since Json does not have tuple, convert data to tuple
            tuple_data = tuple([tuple(item) if isinstance(item, list) else item for item in message.data])
            received_matrix = MatrixSparseDOK.decompress(tuple_data)
            self._edge_computing_matrix = received_matrix + self._edge_computing_matrix
            # Add all coming matrix to one matrix.

        except MessageDestinationError:
            # Do nothing, wrong node
            return None
        except MessageEchoError:
            self._is_echo_received = True
        except ValueError as err:
            print(err)

    def _net_receive(self, message_str):
        """ Handle messages coming from NET topic. """
        try:
            message = NetworkMessage(message_str)
            if message.source_node_id == Message.CLIENT_ID:
                self._is_echo_received = True

        except MessageDestinationError:
            # Do nothing, wrong node
            return None
        except MessageEchoError:
            self._is_echo_received = True
            return None
        except ValueError as err:
            print(err)

    def _check_echo(self, value=None):
        if not self._is_echo_received:
            self.reconnect()
        self._is_echo_received = False

    def _echo_timer_set(self):
        self._is_echo_received = False
        self._echo_timer.init(period=MessageHandler.ECHO_PERIOD, mode=Timer.ONE_SHOT,
                                        callback=self._check_echo)

    def _send_alive(self, value=None):
        print("[DEBUG]: ALIVE")
        self._echo_timer_set()

        self._led_state = 0 if self._led_state else 1
        self._led.value(self._led_state)
        msg = NetworkMessage(None, "NODE ALIVE", self._communication_protocol.CLIENT_ID, sending=True)
        self._communication_protocol.send_network_info(str(msg))

    @staticmethod
    def _create_response(cmd, data, dest_id, msg_id):
        present_time = now()
        log_time = LogTime(hour=present_time.hour, minute=present_time.minute)
        source_id = Message.CLIENT_ID

        response = DataMessage(cmd=cmd, data=data, log_time=log_time, destination_node_id=dest_id,
                               source_node_id=source_id, message_id=msg_id, sending=True)
        return response

    def _request_all_log(self, day):
        msg_id = str(uuid4())
        response = CommandMessage(cmd="GET-NODE-LOG-FULL", day= day, destination_node_id="ANY",
                                  source_node_id=Message.CLIENT_ID, message_id=msg_id, sending=True)

        self._echo_timer_set()
        self._is_edge_computing_done = False
        self._edge_computing_receive_id = msg_id
        self._communication_protocol.send_command(str(response))

    def _edge_computing_done(self, value=None):
        try:
            data=self._edge_computing_matrix.compress()
        except ValueError:
            data = "Sparsity < 0.5"

        response = MessageHandler._create_response(cmd="GET-LOG-FULL-EDGE", data=data,
                                                   dest_id=self._edge_computing_requester,
                                                   msg_id=self._edge_computing_id)

        self._is_edge_computing_done = True
        self._echo_timer_set()
        self._communication_protocol.send_data(str(response))
        self._is_edge_computing = False
