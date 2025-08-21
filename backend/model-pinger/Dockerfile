FROM maven:3.9.11 AS build

WORKDIR /app

COPY pom.xml /app/pom.xml
COPY src /app/src

RUN mvn clean package


FROM eclipse-temurin:21

WORKDIR /app

COPY --from=build /app/target/model-pinger-1.0-SNAPSHOT.jar ./model-pinger-app.jar

CMD ["java", "-jar", "model-pinger-app.jar"]
