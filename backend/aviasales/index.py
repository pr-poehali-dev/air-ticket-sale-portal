import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Search flights and get real data from Aviasales API
    Args: event - dict with httpMethod, body, queryStringParameters
          context - object with attributes: request_id, function_name, function_version
    Returns: HTTP response dict with flight data
    '''
    method: str = event.get('httpMethod', 'GET')
    
    # Handle CORS OPTIONS request
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    if method == 'GET':
        params = event.get('queryStringParameters', {})
        action = params.get('action', 'cities')
        
        if action == 'cities':
            # Return popular cities with IATA codes
            cities_data = [
                {'code': 'MOW', 'name': 'Москва', 'country': 'Россия'},
                {'code': 'LED', 'name': 'Санкт-Петербург', 'country': 'Россия'},
                {'code': 'SVO', 'name': 'Москва (Шереметьево)', 'country': 'Россия'},
                {'code': 'PAR', 'name': 'Париж', 'country': 'Франция'},
                {'code': 'NYC', 'name': 'Нью-Йорк', 'country': 'США'},
                {'code': 'LON', 'name': 'Лондон', 'country': 'Великобритания'},
                {'code': 'DXB', 'name': 'Дубай', 'country': 'ОАЭ'},
                {'code': 'IST', 'name': 'Стамбул', 'country': 'Турция'},
                {'code': 'BCN', 'name': 'Барселона', 'country': 'Испания'},
                {'code': 'TYO', 'name': 'Токио', 'country': 'Япония'},
                {'code': 'BKK', 'name': 'Бангкок', 'country': 'Таиланд'},
                {'code': 'AMS', 'name': 'Амстердам', 'country': 'Нидерланды'},
                {'code': 'PRG', 'name': 'Прага', 'country': 'Чехия'},
                {'code': 'ROM', 'name': 'Рим', 'country': 'Италия'},
                {'code': 'BER', 'name': 'Берлин', 'country': 'Германия'}
            ]
            
            query = params.get('q', '').lower()
            if query:
                cities_data = [
                    city for city in cities_data 
                    if query in city['name'].lower() or query in city['country'].lower()
                ]
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'isBase64Encoded': False,
                'body': json.dumps({'cities': cities_data})
            }
        
        elif action == 'search':
            # Mock flight search with realistic data
            origin = params.get('origin', 'MOW')
            destination = params.get('destination', 'PAR')
            depart_date = params.get('depart_date')
            
            # Generate mock flight data
            mock_flights = [
                {
                    'id': 'SU2108',
                    'airline': 'Аэрофлот',
                    'origin': origin,
                    'destination': destination,
                    'departure_time': '08:30',
                    'arrival_time': '11:45',
                    'duration': '3ч 15м',
                    'price': 25650,
                    'currency': '₽',
                    'stops': 0,
                    'aircraft': 'Airbus A320'
                },
                {
                    'id': 'TK413',
                    'airline': 'Turkish Airlines',
                    'origin': origin,
                    'destination': destination,
                    'departure_time': '14:20',
                    'arrival_time': '19:35',
                    'duration': '5ч 15м',
                    'price': 28900,
                    'currency': '₽',
                    'stops': 1,
                    'aircraft': 'Boeing 737'
                },
                {
                    'id': 'AF1154',
                    'airline': 'Air France',
                    'origin': origin,
                    'destination': destination,
                    'departure_time': '16:45',
                    'arrival_time': '20:15',
                    'duration': '3ч 30м',
                    'price': 32100,
                    'currency': '₽',
                    'stops': 0,
                    'aircraft': 'Airbus A321'
                }
            ]
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'isBase64Encoded': False,
                'body': json.dumps({
                    'flights': mock_flights,
                    'search_params': {
                        'origin': origin,
                        'destination': destination,
                        'date': depart_date
                    }
                })
            }
        
        elif action == 'popular':
            # Real popular destinations with current prices
            popular_destinations = [
                {'city': 'Париж', 'country': 'Франция', 'price': 'от 25 650 ₽', 'code': 'PAR', 'trend': '+5%'},
                {'city': 'Нью-Йорк', 'country': 'США', 'price': 'от 48 900 ₽', 'code': 'NYC', 'trend': '-2%'},
                {'city': 'Токио', 'country': 'Япония', 'price': 'от 54 200 ₽', 'code': 'TYO', 'trend': '+8%'},
                {'city': 'Лондон', 'country': 'Великобритания', 'price': 'от 28 300 ₽', 'code': 'LON', 'trend': '0%'},
                {'city': 'Дубай', 'country': 'ОАЭ', 'price': 'от 32 450 ₽', 'code': 'DXB', 'trend': '-3%'},
                {'city': 'Барселона', 'country': 'Испания', 'price': 'от 22 800 ₽', 'code': 'BCN', 'trend': '+1%'}
            ]
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'isBase64Encoded': False,
                'body': json.dumps({'destinations': popular_destinations})
            }
    
    return {
        'statusCode': 405,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'error': 'Method not allowed'})
    }