using System;
using RabbitMQ.Client;
using System.Text;
using RabbitMQ.Client.Events;

class Receive
{
    public static void Main()
    {
        var factory = new ConnectionFactory() { HostName = "localhost" };
        using(var connection = factory.CreateConnection())
        using(var channel = connection.CreateModel())
        {
            channel.QueueDeclare(queue: "extract", durable: false, exclusive: false, autoDelete: false, arguments: null);

            var consumer = new EventingBasicConsumer(channel);
            consumer.Received += (model, ea) =>
            {
                Console.WriteLine("Receive a message!");
                var body = ea.Body;
                var message = Encoding.UTF8.GetString(body);
                // extract dates and amounts using regex
                channel.BasicPublish(exchange: "", routingKey: "result", basicProperties: null, body:body);
                Console.WriteLine("Sent a message! " + message);
            };
            channel.BasicConsume(queue: "extract", autoAck: true, consumer: consumer);
            Console.ReadLine();
        }
    }
}
