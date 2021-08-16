using System;
using System.Collections.Generic;
using System.Text;
using System.Numerics;

namespace RARPG_Server
{
    class ServerHandle
    {
        public static void WelcomeReceived(int _fromClient, Packet _packet)
        {
            int _clientIdCheck = _packet.ReadInt();
            string _username = _packet.ReadString();

            Console.WriteLine($"{Server.clients[_fromClient].tcp.socket.Client.RemoteEndPoint} connected successfully and is now player {_fromClient}.");
            if (_fromClient != _clientIdCheck)
            {
                Console.WriteLine($"Player \"{_username}\" (ID: {_fromClient}) has assumed the wrong client ID ({_clientIdCheck})!");
            }
            Server.clients[_fromClient].SendIntoGame(_username);
        }

        public static void PlayerMovement(int _fromClient, Packet _packet)
        {
            Vector3 position = _packet.ReadVector3();
            Quaternion rotation = _packet.ReadQuaternion();

            Server.clients[_fromClient].player.SetTransform(position, rotation);
        }

        public static void FlagRequest(int _fromClient, Packet _packet)
        { 
            Player player = Server.clients[_fromClient].player;
            int flagId = _packet.ReadInt();

            // other flag: ractf{Y0uB3tt3rN0tHav3De0bfusc4ted...}
            // is generated on client and not sent.

            if (flagId == 7)
            {
                // Teleport inside box flag
                // <-17.551188, 1.0799998, 0.07314894>
                // < -14.216297, 1.0799998, 4.244825 >
                if (player.position.X > -17.552f && player.position.X < -14.217f && player.position.Z > 0.07f && player.position.Z < 4.244 && player.position.Y < 3.2)
                {
                    ServerSend.FlagInformation(player, 7, "ractf{T3l3port1ng_iS_fuN!}");
                } else
                {
                    Console.WriteLine(player.position.ToString());
                }
            }

            if (flagId == 9)
            {
                ServerSend.FlagInformation(player, 9, "ractf{N3tw0rking_L1ke_4_B0ss!}");
            }
        }
    }
}
