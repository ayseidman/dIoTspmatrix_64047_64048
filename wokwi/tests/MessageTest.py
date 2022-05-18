from Message import Message, MessageDestinationError
from CommandMessage import CommandMessage
#from wokwi.DataMessage import DataMessage
import unittest
from tests.example_messages import CMD, CLIENT_ID

Message.CLIENT_ID = CLIENT_ID


class TestMessage(unittest.TestCase):

    def test_00(self):
        m1 = Message()

    def test_01(self):
        m1 = Message(CMD.GET_LOG_PROPER)

    def test_02(self):
        try:
            m1 = Message(CMD.JSON_ERR1)
            self.assertTrue(False, "Failed to Raise Exception")
        except ValueError:
            pass

    def test_03(self):
        try:
            m1 = Message(CMD.JSON_ERR2)
            self.assertTrue(False, "Failed to Raise Exception")
        except ValueError:
            pass

    def test_04(self):
        try:
            m1 = Message(CMD.JSON_ERR3)
            self.assertTrue(False, "Failed to Raise Exception")
        except ValueError:
            pass

    def test_05(self):
        try:
            m1 = Message(CMD.JSON_ERR4)
            self.assertTrue(False, "Failed to Raise Exception")
        except ValueError:
            pass


class TestCommandMessage(unittest.TestCase):

    def test_00(self):
        try:
            m1 = CommandMessage()
            self.assertTrue(False, "Failed to Raise Exception")
        except ValueError as error:
            self.assertEqual(str(error), "Wrong Command Format!")

    def test_02(self):
        Message.CLIENT_ID = CLIENT_ID
        try:
            m1 = CommandMessage(CMD.GET_LOG_PROPER_WRONG_NODE)
            self.assertTrue(False, "Failed to Raise Exception")
        except MessageDestinationError as error:
            self.assertEqual(str(error), "Wrong Message Destination")
        except:
            self.assertTrue(False, "Exception Catch Error")

    def test_03(self):
        Message.CLIENT_ID = CLIENT_ID
        m1 = CommandMessage(CMD.GET_LOG_PROPER)
        self.assertEqual(m1.message_id, "0")
        self.assertEqual(m1.day, 0)
        self.assertEqual(m1.source_node_id, "12ewde123")
        self.assertEqual(m1.destination_node_id, CLIENT_ID)

    def test_04(self):
        Message.CLIENT_ID = CLIENT_ID
        m1 = CommandMessage(None, "GET-NODE-LOG-FULL", 0, destination_node_id="sadad", source_node_id=CLIENT_ID, message_id="2")

    def test_05(self):
        Message.CLIENT_ID = CLIENT_ID
        try:
            m1 = CommandMessage(None, "GET-NODE-LOG-BY-HOUR", 0, hour=50, minute=0, destination_node_id="sadad", source_node_id=CLIENT_ID, message_id="2")
            self.assertTrue(False, "Failed to assertion")
        except ValueError as err:
            self.assertEqual(str(err), "Wrong Hour Format!")

    def test_05(self):
        Message.CLIENT_ID = CLIENT_ID
        try:
            m1 = CommandMessage(None, "GET-NODE-LOG-BY-HOUR", 0, hour=0, minute=100, destination_node_id="sadad", source_node_id=CLIENT_ID, message_id="2")
            self.assertTrue(False, "Failed to assertion")
        except ValueError as err:
            self.assertEqual(str(err), "Wrong Minute Format!")

    def test_06(self):
        Message.CLIENT_ID = CLIENT_ID
        m1 = CommandMessage(None, "GET-NODE-LOG-BY-HOUR", destination_node_id="sadad", source_node_id=CLIENT_ID, message_id="2")
        self.assertEqual(m1.message_id, "2")
        self.assertEqual(m1.day, 0)
        self.assertEqual(m1.hour, 0)
        self.assertEqual(m1.minute, 0)
        self.assertEqual(m1.source_node_id, CLIENT_ID)
        self.assertEqual(m1.destination_node_id, "sadad")

    def test_07(self):
        try:
            m1 = CommandMessage(CMD.GET_LOG_ERR_MSG_ID)
            self.assertTrue(False,"Failed to Assert")
        except:
            pass

    def test_08(self):
        try:
            m1 = CommandMessage(CMD.GET_LOG_ERR_DEST)
            self.assertTrue(False,"Failed to Assert")
        except:
            pass

    def test_09(self):
        try:
            m1 = CommandMessage(CMD.GET_LOG_ERR_SRC)
            self.assertTrue(False,"Failed to Assert")
        except:
            pass

    def test_10(self):
        try:
            m1 = CommandMessage(CMD.GET_LOG_ERR_DAY3)
            self.assertTrue(False,"Failed to Assert")
        except:
            pass

    def test_11(self):
        try:
            m1 = CommandMessage(CMD.GET_LOG_ERR_DAY2)
            self.assertTrue(False, "Failed to Assert")
        except:
            pass

    def test_11(self):
        try:
            m1 = CommandMessage(CMD.GET_LOG_ERR_DAY1)
            self.assertTrue(False, "Failed to Assert")
        except:
            pass

    def test_12(self):
        m1 = CommandMessage(CMD.GET_LOG_PROPER_ANY)

    def test_13(self):
        Message.CLIENT_ID = CLIENT_ID
        try:
            m1 = CommandMessage(None, "GET-NODE-LOG-BY-HOUR", 1, hour=23, minute=0, destination_node_id="sadad", source_node_id=CLIENT_ID, message_id="2")
            self.assertTrue(False, "Failed to assertion")
        except ValueError as err:
            self.assertEqual(str(err), "Wrong Day Format!")


class TestDataMessage(unittest.TestCase):
    pass

class TestNetworkMessage(unittest.TestCase):
    pass
