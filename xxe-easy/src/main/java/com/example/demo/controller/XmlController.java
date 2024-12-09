package com.example.demo.controller;

import com.example.demo.model.Location;
import com.example.demo.service.SnowService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

@RestController
public class XmlController {

    @Autowired
    private SnowService snowService;

    @PostMapping(value = "/process-xml", 
                consumes = "application/xml", 
                produces = "application/json")
    public Location processXml(@RequestBody String xml) {
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setFeature("http://xml.org/sax/features/external-general-entities", true);
            factory.setFeature("http://xml.org/sax/features/external-parameter-entities", true);
            factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", true);
            
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.parse(new java.io.ByteArrayInputStream(xml.getBytes()));
            
            Location location = new Location();
            String latContent = document.getElementsByTagName("latitude").item(0).getTextContent();
            String lonContent = document.getElementsByTagName("longitude").item(0).getTextContent();
            
            try {
                location.setLatitude(Double.parseDouble(latContent));
            } catch (NumberFormatException e) {
                location.setLatitude(0);
                location.setSnowStatus(latContent);
                return location;
            }
            
            location.setLongitude(Double.parseDouble(lonContent));
            boolean hasSnow = snowService.checkSnowPresence(location.getLatitude(), location.getLongitude());
            location.setHasSnow(hasSnow);
            
            return location;
        } catch (Exception e) {
            throw new RuntimeException("Ошибка при обработке XML: " + e.getMessage());
        }
    }
}
