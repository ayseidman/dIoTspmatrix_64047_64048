from umqtt.simple import MQTTClient
from CommunicationInterface import CommunicationInterface


class MQTT(CommunicationInterface, MQTTClient):
  CLIENT_ID = "dIoTspmatrix_64047_64048"
  BROKER = "broker.mqttdashboard.com"
  USER = ""
  PASSWORD = ""
  TOPIC_DATA = "dIoTspmatrix-data"
  TOPIC_CMD = "dIoTspmatrix-cmd"
  TOPIC_NET = "dIoTspmatrix-net"

  def __init__(self):
    CommunicationInterface.__init__(self)
    MQTTClient.__init__(self, MQTT.CLIENT_ID, MQTT.BROKER, user = MQTT.USER, password = MQTT.PASSWORD)
    self._handle_cmd = None
    self._handle_data = None
    self._handle_net = None

  def connect(self):
    CommunicationInterface.connect(self)
    MQTTClient.connect(self)

    try: 
      self._check_handlers()
    except ValueError:
      raise ValueError("Message handlers must be set first! (set_callback)")

    MQTTClient.set_callback(self, self._callback)
    self._subscribe_topics()

  def disconnect(self):
    CommunicationInterface.disconnect(self)
    MQTTClient.disconnect(self)

  def set_callback(self, handle_cmd, handle_data, handle_net):
    self._handle_cmd = handle_cmd
    self._handle_data = handle_data
    self._handle_net = handle_net
    self._check_handlers()

  def _check_handlers(self):
    if not (callable(self._handle_cmd) and callable(self._handle_data) and callable(self._handle_net)):
      raise ValueError("Arguments are not callable.")

  def _subscribe_topics(self):
    self.subscribe(MQTT.TOPIC_CMD)
    self.subscribe(MQTT.TOPIC_DATA)
    self.subscribe(MQTT.TOPIC_NET)

  def _callback(self, topic, message):
    topic = topic.decode("utf-8") 
    message = message.decode("utf-8") 
    
    if topic == MQTT.TOPIC_CMD:
      self._handle_cmd(message)
    elif topic == MQTT.TOPIC_DATA:
      self._handle_data(message)
    elif topic == MQTT.TOPIC_NET:
      self._handle_net(message)
    else:
      raise ValueError("Wrong Topic Message: can only be {}, {} or {}".format(MQTT.TOPIC_CMD, MQTT.TOPIC_DATA, MQTT.TOPIC_NET))
    