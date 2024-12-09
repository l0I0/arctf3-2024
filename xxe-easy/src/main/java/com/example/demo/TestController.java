package com.example.demo.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class TestController {
    
    @GetMapping("/")
    public String home() {
        return "index";
    }
    
    @GetMapping("/test")
    public String test() {
        return "test";
    }
}