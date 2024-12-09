package com.example.demo.model;

import lombok.Data;
import jakarta.xml.bind.annotation.XmlRootElement;

@Data
@XmlRootElement
public class User {
    private String name;
    private String email;
} 