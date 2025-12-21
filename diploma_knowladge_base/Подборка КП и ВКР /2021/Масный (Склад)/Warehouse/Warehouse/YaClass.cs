using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Security;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Threading;
using System.Threading.Tasks;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Client.Connecting;
using MQTTnet.Client.Disconnecting;
using MQTTnet.Client.Options;

namespace YaClass
{
    public enum EntityType
    {
        Registry = 0,
        Device = 1
    }

    public enum TopicType
    {
        Events = 0,
        Commands = 1
    }

    public class YaClient 
    {
        public const string MqttServer = "mqtt.cloud.yandex.net";
        public const int MqttPort = 8883;

        private static X509Certificate2 rootCrt = new X509Certificate2("C:/Users/dmasn/source/repos/Warehouse/rootCA.crt"); // путь до сертификата

        public static string TopicName(string entityId, EntityType entity, TopicType topic)
        {
            string result = (entity == EntityType.Registry) ? "$registries/" : "$devices/";
            result += entityId;
            result += (topic == TopicType.Events) ? "/events" : "/commands";
            return result;
        }

        public delegate void OnSubscribedData(string topic, byte[] payload);
        public event OnSubscribedData SubscribedData;

        private IMqttClient mqttClient = null;
        private ManualResetEvent oCloseEvent = new ManualResetEvent(false);
        private ManualResetEvent oConnectedEvent = new ManualResetEvent(false);



        public void Start(string id, string password)
        {
            //setup connection options
            MqttClientOptionsBuilderTlsParameters tlsOptions = new MqttClientOptionsBuilderTlsParameters
            {
                SslProtocol = SslProtocols.Tls12,
                UseTls = true
            };
            tlsOptions.CertificateValidationCallback += CertificateValidationCallback;

            // Create TCP based options using the builder.
            var options = new MqttClientOptionsBuilder()
                .WithClientId($"Test_C#_Client_Dmasny_PC")
                .WithTcpServer(MqttServer, MqttPort)
                .WithTls(tlsOptions)
                .WithCleanSession()
                .WithCredentials(id, password)
                .Build();
            var factory = new MqttFactory();
            mqttClient = factory.CreateMqttClient();
            mqttClient.UseApplicationMessageReceivedHandler(DataHandler);
            mqttClient.UseConnectedHandler(ConnectedHandler);
            mqttClient.UseDisconnectedHandler(DisconnectedHandler);
            mqttClient.ConnectAsync(options, CancellationToken.None);
        }
        public void Stop()
        {
            oCloseEvent.Set();
            mqttClient.DisconnectAsync();
        }
        public bool WaitConnected()
        {
            WaitHandle[] waites = { oCloseEvent, oConnectedEvent };
            return WaitHandle.WaitAny(waites) == 1;
        }
        public Task Subscribe(string topic, MQTTnet.Protocol.MqttQualityOfServiceLevel qos)
        {
            return mqttClient.SubscribeAsync(topic, qos);
        }

        public Task Publish(string topic, string payload, MQTTnet.Protocol.MqttQualityOfServiceLevel qos)
        {
            return mqttClient.PublishAsync(topic, payload, qos);
        }
        private Task ConnectedHandler(MqttClientConnectedEventArgs arg)
        {
            oConnectedEvent.Set();
            return Task.CompletedTask;
        }

        private static Task DisconnectedHandler(MqttClientDisconnectedEventArgs arg)
        {
            Console.WriteLine($"Disconnected mqtt.cloud.yandex.net.");
            return Task.CompletedTask;
        }

        private Task DataHandler(MqttApplicationMessageReceivedEventArgs arg)
        {

            SubscribedData(arg.ApplicationMessage.Topic, arg.ApplicationMessage.Payload);
            return Task.CompletedTask;
        }

        private static bool CertificateValidationCallback(X509Certificate cert, X509Chain chain, SslPolicyErrors errors, IMqttClientOptions opts)
        {
            try
            {
                if (errors == SslPolicyErrors.None)
                {
                    return true;
                }

                if (errors == SslPolicyErrors.RemoteCertificateChainErrors)
                {
                    chain.ChainPolicy.RevocationMode = X509RevocationMode.NoCheck;
                    chain.ChainPolicy.VerificationFlags = X509VerificationFlags.NoFlag;
                    chain.ChainPolicy.ExtraStore.Add(rootCrt);

                    chain.Build((X509Certificate2)rootCrt);
                    var res = chain.ChainElements.Cast<X509ChainElement>().Any(a => a.Certificate.Thumbprint == rootCrt.Thumbprint);
                    return res;
                }
            }
            catch { }

            return false;
        }

    }
}