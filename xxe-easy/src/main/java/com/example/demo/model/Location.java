package com.example.demo.model;

import lombok.Data;
import jakarta.xml.bind.annotation.XmlRootElement;

@Data
@XmlRootElement
public class Location {
    private double latitude;
    private double longitude;
    private boolean hasSnow;
    private String snowStatus;
} 