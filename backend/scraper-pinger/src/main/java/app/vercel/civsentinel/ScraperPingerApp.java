package app.vercel.civsentinel;

import org.apache.kafka.clients.producer.*;

import java.util.Properties;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ScheduledExecutorService;

public class ScraperPingerApp {
    public static void main(String[] args) {
        String bootstrapServers = System.getenv("KAFKA_BOOTSTRAP_SERVERS");
        int pingInterval = Integer.parseInt(System.getenv("PING_INTERVAL"));
        String scraperPingTopic = "scraper-ping";

        Properties props = new Properties();
        props.put("bootstrap.servers", bootstrapServers);
        props.put("linger.ms", 1);
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        Producer<String, String> producer = new KafkaProducer<>(props);
        startPingInterval(producer, scraperPingTopic, pingInterval);

        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Main thread interrupted: " + e.getMessage());
        }
    }

    private static void startPingInterval(Producer<String, String> producer, String topic, long interval) {
        Runnable sendPingTask = () -> {
            sendScraperPing(producer, topic);
        };

        ScheduledExecutorService scheduledExecutor = Executors.newSingleThreadScheduledExecutor();
        scheduledExecutor.scheduleAtFixedRate(sendPingTask, 0, interval, java.util.concurrent.TimeUnit.MILLISECONDS);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Shutting down...");
            scheduledExecutor.shutdown();
            producer.close();
        }));
    }

    private static void sendScraperPing(Producer<String, String> producer, String topic) {
        try {
            ProducerRecord<String, String> record = new ProducerRecord<>(topic, "ping");
            producer.send(record).get();
            System.out.println("Ping sent to topic: " + topic);
        } catch (ExecutionException e) {
            System.err.println("Error sending ping: " + e.getMessage());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Ping sending interrupted: " + e.getMessage());
        }
    }
}
