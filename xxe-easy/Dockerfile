FROM maven:3.8.4-openjdk-17-slim
WORKDIR /app
COPY pom.xml .
COPY src ./src
COPY .mvn ./.mvn
COPY mvnw .
COPY mvnw.cmd .

RUN chmod +x mvnw
EXPOSE 8080
CMD ["./mvnw", "spring-boot:run"]