package app.vercel.civsentinel;

import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.NewTopic;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class KafkaTopicsApp {
    public static void main(String[] args) {
        String bootstrapServers = System.getenv("KAFKA_BOOTSTRAP_SERVERS");
        String topicsStr = System.getenv("KAFKA_TOPICS");
        int partitions = Integer.parseInt(System.getenv("KAFKA_PARTITIONS"));
        int retentionFactor = Integer.parseInt(System.getenv("KAFKA_RETENTION_FACTOR"));
        short replicationFactor = Short.parseShort(System.getenv("KAFKA_REPLICATION_FACTOR"));

        Map<String, String> topicsConfig = new HashMap<>();

        String[] topics = topicsStr.split(",");

        Properties config = new Properties();

        topicsConfig.put("retention.ms", Integer.toString(retentionFactor));
        config.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);

        try (AdminClient adminClient = AdminClient.create(config)) {
            for (String topic : topics) {
                NewTopic newTopic = new NewTopic(topic, partitions, replicationFactor);
                adminClient.createTopics(Collections.singleton(newTopic)).all().get();
                System.out.println("Created topic: " + topic);
            }
            System.out.println("All topics created successfully.");
            Thread.sleep(Long.MAX_VALUE);
            System.out.println("Topics created. Sleeping...");
        } catch (ExecutionException e) {
            System.err.println("Error creating topics: " + e.getMessage());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Topic creation interrupted: " + e.getMessage());
        }
    }
}
