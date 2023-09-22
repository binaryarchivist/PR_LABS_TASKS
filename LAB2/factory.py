from xml.etree import ElementTree
from io import BytesIO

from player import Player
import player_pb2 as pb



def dict_to_player(dict):
    return Player(dict['nickname'], dict['email'], dict['date_of_birth'], int(dict['xp']), dict['cls'])


class PlayerFactory:
    def to_json(self, players):
        try:
            formatted_players = []

            for player in players:
                player_dict = player.__dict__
                player_dict['date_of_birth'] = player_dict['date_of_birth'].strftime("%Y-%m-%d")
                formatted_players.append(player_dict)
            return formatted_players
        except:
            return 'err'

    def from_json(self, list_of_dict):
        try:
            formatted_players = []

            for obj in list_of_dict:
                formatted_players.append(dict_to_player(obj))

            return formatted_players
        except:
            return 'err'

    def from_xml(self, xml_string):
        try:
            players_data = []

            tree = ElementTree.fromstring(xml_string)
            root = tree.findall('player')

            for player in root:
                player_data = {}
                for child in player:
                    player_data[child.tag] = child.text
                players_data.append(dict_to_player(player_data))

            return players_data
        except:
            return 'err'

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''
        root = ElementTree.Element('data')
        for obj in list_of_players:
            player = ElementTree.SubElement(root, 'player')
            obj_dict = obj.__dict__

            for key, value in obj_dict.items():
                child = ElementTree.SubElement(player, key)
                if key == 'date_of_birth':
                    child.text = str(value.strftime("%Y-%m-%d"))
                else:
                    child.text = str(value)
        tree = ElementTree.ElementTree(root)

        xml_string_io = BytesIO()
        tree.write(xml_string_io, encoding='utf-8', xml_declaration=True)
        xml_string = xml_string_io.getvalue().decode('utf-8')

        return xml_string

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        player_list = pb.PlayersList()
        classes = pb.Class
        player_list.ParseFromString(binary)
        result = []

        for player in player_list.player:
            result.append(
                Player(player.nickname, player.email, player.date_of_birth, player.xp, classes.Name(player.cls)))
        return result

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects into a binary protobuf string.
        '''
        classes = pb.Class

        serialized_players = pb.PlayersList()
        for player in list_of_players:
            serialized_player = serialized_players.player.add()

            serialized_player.nickname = player.nickname
            serialized_player.email = player.email
            serialized_player.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            serialized_player.xp = player.xp
            serialized_player.cls = classes.Value(player.cls)

        return serialized_players.SerializeToString()
