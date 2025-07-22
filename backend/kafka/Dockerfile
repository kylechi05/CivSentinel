FROM maven:3.9.11 AS build

WORKDIR /app

COPY pom.xml /app/pom.xml
COPY src /app/src

RUN mvn clean package


FROM eclipse-temurin:21

WORKDIR /app

COPY --from=build /app/target/kafka-1.0-SNAPSHOT.jar ./kafka-app.jar

CMD ["java", "-jar", "kafka-app.jar"]
