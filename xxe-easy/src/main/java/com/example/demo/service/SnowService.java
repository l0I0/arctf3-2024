package com.example.demo.service;

import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.time.Month;

@Service
public class SnowService {
    
    public boolean checkSnowPresence(double latitude, double longitude) {
        Month currentMonth = LocalDate.now().getMonth();
        
        // Проверка для Антарктиды (южное полушарие)
        if (latitude < -60.0) {
            return true;
        }
        
        // Проверка для северного полушария
        if (latitude > 60.0) {
            return true;
        }
        
        // Проверка для горных регионов
        if (isHighAltitudeRegion(latitude, longitude)) {
            return true;
        }
        
        return false;
    }
    
    private boolean isHighAltitudeRegion(double latitude, double longitude) {
        // Основные горные системы
        return isInAlps(latitude, longitude) ||
               isInCaucasus(latitude, longitude) ||
               isInHimalayas(latitude, longitude) ||
               isInAndes(latitude, longitude);
    }
    
    private boolean isInAlps(double latitude, double longitude) {
        return latitude >= 45.0 && latitude <= 48.0 && 
               longitude >= 5.0 && longitude <= 16.0;
    }
    
    private boolean isInCaucasus(double latitude, double longitude) {
        return latitude >= 41.0 && latitude <= 44.0 && 
               longitude >= 38.0 && longitude <= 48.0;
    }
    
    private boolean isInHimalayas(double latitude, double longitude) {
        return latitude >= 27.0 && latitude <= 35.0 && 
               longitude >= 72.0 && longitude <= 95.0;
    }
    
    private boolean isInAndes(double latitude, double longitude) {
        return latitude >= -55.0 && latitude <= -15.0 && 
               longitude >= -75.0 && longitude <= -65.0;
    }
} 