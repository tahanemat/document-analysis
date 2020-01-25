using System;
using RabbitMQ.Client;
using System.Text;
using System.Text.RegularExpressions;
using System.Globalization;
using RabbitMQ.Client.Events;
using System.Threading;

class Receive
{
    public static void Main()
    {
        var factory = new ConnectionFactory() { HostName = "localhost" };
        var epoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        using (var connection = factory.CreateConnection())
        using (var channel = connection.CreateModel())
        {
            channel.QueueDeclare(queue: "extract", durable: false, exclusive: false, autoDelete: false, arguments: null);

            var consumer = new EventingBasicConsumer(channel);
            consumer.Received += (model, ea) =>
            {
                Console.WriteLine("Receive a message!");
                var body = ea.Body;
                var message = Encoding.UTF8.GetString(body);
                Console.WriteLine(message);
                var regex = new Regex(@"\b\d{2}\.\d{2}.\d{4}\b");
                foreach (Match m in regex.Matches(message))
                {
                    DateTime dt;
                    if (DateTime.TryParseExact(m.Value, "dd.MM.yyyy", null, DateTimeStyles.None, out dt))
                    {
                        var unixDateTime = (dt.ToUniversalTime() - epoch).TotalSeconds;
                        byte[] singleDate = BitConverter.GetBytes(unixDateTime);
                        channel.BasicPublish(exchange: "", routingKey: "result", basicProperties: null, body: singleDate);
                        Console.WriteLine("Sent a message! " + dt.ToString());
                    }
                }
            };
            channel.BasicConsume(queue: "extract", autoAck: true, consumer: consumer);
            Thread.Sleep(Timeout.Infinite);
        }
    }
}