import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
import os

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Travel platform with flights (20% discount) and hotels (25% discount)
    Args: event - dict with httpMethod, body, queryStringParameters
          context - object with attributes: request_id, function_name, function_version
    Returns: HTTP response dict with competitive prices for flights and hotels
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
            # Return 200+ popular cities with multiple airports
            cities_data = [
                # Россия - 25 городов
                {'code': 'MOW', 'name': 'Москва', 'country': 'Россия'},
                {'code': 'SVO', 'name': 'Москва (Шереметьево)', 'country': 'Россия'},
                {'code': 'DME', 'name': 'Москва (Домодедово)', 'country': 'Россия'},
                {'code': 'VKO', 'name': 'Москва (Внуково)', 'country': 'Россия'},
                {'code': 'LED', 'name': 'Санкт-Петербург', 'country': 'Россия'},
                {'code': 'KZN', 'name': 'Казань', 'country': 'Россия'},
                {'code': 'ROV', 'name': 'Ростов-на-Дону', 'country': 'Россия'},
                {'code': 'KRR', 'name': 'Краснодар', 'country': 'Россия'},
                {'code': 'UFA', 'name': 'Уфа', 'country': 'Россия'},
                {'code': 'VVO', 'name': 'Владивосток', 'country': 'Россия'},
                {'code': 'NOZ', 'name': 'Новокузнецк', 'country': 'Россия'},
                {'code': 'OVB', 'name': 'Новосибирск', 'country': 'Россия'},
                {'code': 'SVX', 'name': 'Екатеринбург', 'country': 'Россия'},
                {'code': 'TOF', 'name': 'Томск', 'country': 'Россия'},
                {'code': 'KHV', 'name': 'Хабаровск', 'country': 'Россия'},
                {'code': 'YKS', 'name': 'Якутск', 'country': 'Россия'},
                {'code': 'IKT', 'name': 'Иркутск', 'country': 'Россия'},
                {'code': 'KEJ', 'name': 'Кемерово', 'country': 'Россия'},
                {'code': 'MMK', 'name': 'Мурманск', 'country': 'Россия'},
                {'code': 'AER', 'name': 'Сочи', 'country': 'Россия'},
                {'code': 'VOG', 'name': 'Волгоград', 'country': 'Россия'},
                {'code': 'VOZ', 'name': 'Воронеж', 'country': 'Россия'},
                {'code': 'KUF', 'name': 'Самара', 'country': 'Россия'},
                {'code': 'NBC', 'name': 'Набережные Челны', 'country': 'Россия'},
                {'code': 'ASF', 'name': 'Астрахань', 'country': 'Россия'},
                
                # Европа - 50 городов
                {'code': 'CDG', 'name': 'Париж (Шарль де Голль)', 'country': 'Франция'},
                {'code': 'ORY', 'name': 'Париж (Орли)', 'country': 'Франция'},
                {'code': 'NCE', 'name': 'Ницца', 'country': 'Франция'},
                {'code': 'LYS', 'name': 'Лион', 'country': 'Франция'},
                {'code': 'MRS', 'name': 'Марсель', 'country': 'Франция'},
                {'code': 'LHR', 'name': 'Лондон (Хитроу)', 'country': 'Великобритания'},
                {'code': 'LGW', 'name': 'Лондон (Гатвик)', 'country': 'Великобритания'},
                {'code': 'STN', 'name': 'Лондон (Станстед)', 'country': 'Великобритания'},
                {'code': 'EDI', 'name': 'Эдинбург', 'country': 'Великобритания'},
                {'code': 'MAN', 'name': 'Манчестер', 'country': 'Великобритания'},
                {'code': 'MAD', 'name': 'Мадрид', 'country': 'Испания'},
                {'code': 'BCN', 'name': 'Барселона', 'country': 'Испания'},
                {'code': 'VLC', 'name': 'Валенсия', 'country': 'Испания'},
                {'code': 'BIO', 'name': 'Бильбао', 'country': 'Испания'},
                {'code': 'AGP', 'name': 'Малага', 'country': 'Испания'},
                {'code': 'PMI', 'name': 'Пальма-де-Майорка', 'country': 'Испания'},
                {'code': 'LPA', 'name': 'Лас-Пальмас', 'country': 'Испания'},
                {'code': 'FCO', 'name': 'Рим (Фьюмичино)', 'country': 'Италия'},
                {'code': 'CIA', 'name': 'Рим (Чампино)', 'country': 'Италия'},
                {'code': 'MXP', 'name': 'Милан (Мальпенса)', 'country': 'Италия'},
                {'code': 'LIN', 'name': 'Милан (Линате)', 'country': 'Италия'},
                {'code': 'VCE', 'name': 'Венеция', 'country': 'Италия'},
                {'code': 'NAP', 'name': 'Неаполь', 'country': 'Италия'},
                {'code': 'CTA', 'name': 'Катания', 'country': 'Италия'},
                {'code': 'FRA', 'name': 'Франкфурт-на-Майне', 'country': 'Германия'},
                {'code': 'MUC', 'name': 'Мюнхен', 'country': 'Германия'},
                {'code': 'TXL', 'name': 'Берлин (Тегель)', 'country': 'Германия'},
                {'code': 'BER', 'name': 'Берлин (Бранденбург)', 'country': 'Германия'},
                {'code': 'DUS', 'name': 'Дюссельдорф', 'country': 'Германия'},
                {'code': 'HAM', 'name': 'Гамбург', 'country': 'Германия'},
                {'code': 'CGN', 'name': 'Кёльн', 'country': 'Германия'},
                {'code': 'AMS', 'name': 'Амстердам', 'country': 'Нидерланды'},
                {'code': 'EIN', 'name': 'Эйндховен', 'country': 'Нидерланды'},
                {'code': 'BRU', 'name': 'Брюссель', 'country': 'Бельгия'},
                {'code': 'PRG', 'name': 'Прага', 'country': 'Чехия'},
                {'code': 'VIE', 'name': 'Вена', 'country': 'Австрия'},
                {'code': 'ZUR', 'name': 'Цюрих', 'country': 'Швейцария'},
                {'code': 'GVA', 'name': 'Женева', 'country': 'Швейцария'},
                {'code': 'BSL', 'name': 'Базель', 'country': 'Швейцария'},
                {'code': 'HEL', 'name': 'Хельсинки', 'country': 'Финляндия'},
                {'code': 'CPH', 'name': 'Копенгаген', 'country': 'Дания'},
                {'code': 'ARN', 'name': 'Стокгольм (Арланда)', 'country': 'Швеция'},
                {'code': 'GOT', 'name': 'Гётеборг', 'country': 'Швеция'},
                {'code': 'OSL', 'name': 'Осло', 'country': 'Норвегия'},
                {'code': 'BGO', 'name': 'Берген', 'country': 'Норвегия'},
                {'code': 'WAW', 'name': 'Варшава', 'country': 'Польша'},
                {'code': 'KRK', 'name': 'Краков', 'country': 'Польша'},
                {'code': 'ATH', 'name': 'Афины', 'country': 'Греция'},
                {'code': 'LIS', 'name': 'Лиссабон', 'country': 'Португалия'},
                {'code': 'OPO', 'name': 'Порту', 'country': 'Португалия'},
                {'code': 'BUD', 'name': 'Будапешт', 'country': 'Венгрия'},
                
                # Азия - 40 городов
                {'code': 'IST', 'name': 'Стамбул (Новый аэропорт)', 'country': 'Турция'},
                {'code': 'SAW', 'name': 'Стамбул (Сабиха Гёкчен)', 'country': 'Турция'},
                {'code': 'AYT', 'name': 'Анталья', 'country': 'Турция'},
                {'code': 'ESB', 'name': 'Анкара', 'country': 'Турция'},
                {'code': 'ADB', 'name': 'Измир', 'country': 'Турция'},
                {'code': 'BJV', 'name': 'Бодрум', 'country': 'Турция'},
                {'code': 'DLM', 'name': 'Даламан', 'country': 'Турция'},
                {'code': 'DXB', 'name': 'Дубай', 'country': 'ОАЭ'},
                {'code': 'AUH', 'name': 'Абу-Даби', 'country': 'ОАЭ'},
                {'code': 'SHJ', 'name': 'Шарджа', 'country': 'ОАЭ'},
                {'code': 'DOH', 'name': 'Доха', 'country': 'Катар'},
                {'code': 'KWI', 'name': 'Кувейт', 'country': 'Кувейт'},
                {'code': 'NRT', 'name': 'Токио (Нарита)', 'country': 'Япония'},
                {'code': 'HND', 'name': 'Токио (Ханеда)', 'country': 'Япония'},
                {'code': 'KIX', 'name': 'Осака', 'country': 'Япония'},
                {'code': 'ICN', 'name': 'Сеул (Инчхон)', 'country': 'Южная Корея'},
                {'code': 'GMP', 'name': 'Сеул (Гимпо)', 'country': 'Южная Корея'},
                {'code': 'BKK', 'name': 'Бангкок (Суварнабхуми)', 'country': 'Таиланд'},
                {'code': 'DMK', 'name': 'Бангкок (Дон Муанг)', 'country': 'Таиланд'},
                {'code': 'HKT', 'name': 'Пхукет', 'country': 'Таиланд'},
                {'code': 'CNX', 'name': 'Чиангмай', 'country': 'Таиланд'},
                {'code': 'KUL', 'name': 'Куала-Лумпур', 'country': 'Малайзия'},
                {'code': 'SIN', 'name': 'Сингапур', 'country': 'Сингапур'},
                {'code': 'HKG', 'name': 'Гонконг', 'country': 'Гонконг'},
                {'code': 'PVG', 'name': 'Шанхай (Пудун)', 'country': 'Китай'},
                {'code': 'SHA', 'name': 'Шанхай (Хунцяо)', 'country': 'Китай'},
                {'code': 'PEK', 'name': 'Пекин', 'country': 'Китай'},
                {'code': 'CAN', 'name': 'Гуанчжоу', 'country': 'Китай'},
                {'code': 'SZX', 'name': 'Шэньчжэнь', 'country': 'Китай'},
                {'code': 'DEL', 'name': 'Дели', 'country': 'Индия'},
                {'code': 'BOM', 'name': 'Мумбаи', 'country': 'Индия'},
                {'code': 'BLR', 'name': 'Бангалор', 'country': 'Индия'},
                {'code': 'MAA', 'name': 'Ченнаи', 'country': 'Индия'},
                {'code': 'GOI', 'name': 'Гоа', 'country': 'Индия'},
                {'code': 'TAS', 'name': 'Ташкент', 'country': 'Узбекистан'},
                {'code': 'ALA', 'name': 'Алматы', 'country': 'Казахстан'},
                {'code': 'NUR', 'name': 'Нур-Султан', 'country': 'Казахстан'},
                {'code': 'EVN', 'name': 'Ереван', 'country': 'Армения'},
                {'code': 'TBS', 'name': 'Тбилиси', 'country': 'Грузия'},
                {'code': 'BAK', 'name': 'Баку', 'country': 'Азербайджан'},
                
                # Америка - 30 городов
                {'code': 'JFK', 'name': 'Нью-Йорк (Кеннеди)', 'country': 'США'},
                {'code': 'LGA', 'name': 'Нью-Йорк (Ла-Гуардия)', 'country': 'США'},
                {'code': 'EWR', 'name': 'Нью-Йорк (Ньюарк)', 'country': 'США'},
                {'code': 'LAX', 'name': 'Лос-Анджелес', 'country': 'США'},
                {'code': 'MIA', 'name': 'Майами', 'country': 'США'},
                {'code': 'ORD', 'name': 'Чикаго (О\'Хара)', 'country': 'США'},
                {'code': 'MDW', 'name': 'Чикаго (Мидуэй)', 'country': 'США'},
                {'code': 'SFO', 'name': 'Сан-Франциско', 'country': 'США'},
                {'code': 'LAS', 'name': 'Лас-Вегас', 'country': 'США'},
                {'code': 'PHX', 'name': 'Финикс', 'country': 'США'},
                {'code': 'DEN', 'name': 'Денвер', 'country': 'США'},
                {'code': 'SEA', 'name': 'Сиэтл', 'country': 'США'},
                {'code': 'DFW', 'name': 'Даллас', 'country': 'США'},
                {'code': 'IAH', 'name': 'Хьюстон', 'country': 'США'},
                {'code': 'ATL', 'name': 'Атланта', 'country': 'США'},
                {'code': 'BOS', 'name': 'Бостон', 'country': 'США'},
                {'code': 'YYZ', 'name': 'Торонто', 'country': 'Канада'},
                {'code': 'YVR', 'name': 'Ванкувер', 'country': 'Канада'},
                {'code': 'YUL', 'name': 'Монреаль', 'country': 'Канада'},
                {'code': 'YYC', 'name': 'Калгари', 'country': 'Канада'},
                {'code': 'MEX', 'name': 'Мехико', 'country': 'Мексика'},
                {'code': 'CUN', 'name': 'Канкун', 'country': 'Мексика'},
                {'code': 'PVR', 'name': 'Пуэрто-Вальярта', 'country': 'Мексика'},
                {'code': 'GRU', 'name': 'Сан-Паулу', 'country': 'Бразилия'},
                {'code': 'GIG', 'name': 'Рио-де-Жанейро', 'country': 'Бразилия'},
                {'code': 'BSB', 'name': 'Бразилиа', 'country': 'Бразилия'},
                {'code': 'EZE', 'name': 'Буэнос-Айрес', 'country': 'Аргентина'},
                {'code': 'SCL', 'name': 'Сантьяго', 'country': 'Чили'},
                {'code': 'LIM', 'name': 'Лима', 'country': 'Перу'},
                {'code': 'BOG', 'name': 'Богота', 'country': 'Колумбия'},
                
                # Африка и Океания - 25 городов
                {'code': 'CAI', 'name': 'Каир', 'country': 'Египет'},
                {'code': 'HRG', 'name': 'Хургада', 'country': 'Египет'},
                {'code': 'SSH', 'name': 'Шарм-эш-Шейх', 'country': 'Египет'},
                {'code': 'LXR', 'name': 'Луксор', 'country': 'Египет'},
                {'code': 'CMN', 'name': 'Касабланка', 'country': 'Марокко'},
                {'code': 'RAK', 'name': 'Марракеш', 'country': 'Марокко'},
                {'code': 'TUN', 'name': 'Тунис', 'country': 'Тунис'},
                {'code': 'ALG', 'name': 'Алжир', 'country': 'Алжир'},
                {'code': 'CPT', 'name': 'Кейптаун', 'country': 'ЮАР'},
                {'code': 'JNB', 'name': 'Йоханнесбург', 'country': 'ЮАР'},
                {'code': 'DUR', 'name': 'Дурбан', 'country': 'ЮАР'},
                {'code': 'ADD', 'name': 'Аддис-Абеба', 'country': 'Эфиопия'},
                {'code': 'NBO', 'name': 'Найроби', 'country': 'Кения'},
                {'code': 'SYD', 'name': 'Сидней', 'country': 'Австралия'},
                {'code': 'MEL', 'name': 'Мельбурн', 'country': 'Австралия'},
                {'code': 'BNE', 'name': 'Брисбен', 'country': 'Австралия'},
                {'code': 'PER', 'name': 'Перт', 'country': 'Австралия'},
                {'code': 'ADL', 'name': 'Аделаида', 'country': 'Австралия'},
                {'code': 'AKL', 'name': 'Окленд', 'country': 'Новая Зеландия'},
                {'code': 'CHC', 'name': 'Крайстчерч', 'country': 'Новая Зеландия'},
                
                # Курортные направления - 20 городов
                {'code': 'MLE', 'name': 'Мале (Мальдивы)', 'country': 'Мальдивы'},
                {'code': 'DPS', 'name': 'Денпасар (Бали)', 'country': 'Индонезия'},
                {'code': 'CGK', 'name': 'Джакарта', 'country': 'Индонезия'},
                {'code': 'MNL', 'name': 'Манила', 'country': 'Филиппины'},
                {'code': 'CEB', 'name': 'Себу', 'country': 'Филиппины'},
                {'code': 'SGN', 'name': 'Хошимин', 'country': 'Вьетнам'},
                {'code': 'HAN', 'name': 'Ханой', 'country': 'Вьетнам'},
                {'code': 'DAD', 'name': 'Дананг', 'country': 'Вьетнам'},
                {'code': 'PNH', 'name': 'Пномпень', 'country': 'Камбоджа'},
                {'code': 'RGN', 'name': 'Янгон', 'country': 'Мьянма'},
                {'code': 'CMB', 'name': 'Коломбо', 'country': 'Шри-Ланка'},
                {'code': 'KTM', 'name': 'Катманду', 'country': 'Непал'},
                {'code': 'ISB', 'name': 'Исламабад', 'country': 'Пакистан'},
                {'code': 'KHI', 'name': 'Карачи', 'country': 'Пакистан'},
                {'code': 'DAC', 'name': 'Дакка', 'country': 'Бангладеш'},
                {'code': 'IKA', 'name': 'Тегеран', 'country': 'Иран'},
                {'code': 'THR', 'name': 'Тегеран (Мехрабад)', 'country': 'Иран'},
                {'code': 'BAH', 'name': 'Манама', 'country': 'Бахрейн'},
                {'code': 'MCT', 'name': 'Маскат', 'country': 'Оман'},
                {'code': 'RUH', 'name': 'Эр-Рияд', 'country': 'Саудовская Аравия'}
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
            from_city = params.get('from', '')
            to_city = params.get('to', '')
            departure_date = params.get('date', '2024-12-15')
            
            # Enhanced flight data with more airlines and competitive pricing (30% below market)
            airlines = [
                {'name': 'Аэрофлот', 'code': 'SU', 'multiplier': 0.95},
                {'name': 'S7 Airlines', 'code': 'S7', 'multiplier': 0.85},
                {'name': 'Turkish Airlines', 'code': 'TK', 'multiplier': 1.1},
                {'name': 'Emirates', 'code': 'EK', 'multiplier': 1.25},
                {'name': 'Qatar Airways', 'code': 'QR', 'multiplier': 1.15},
                {'name': 'Lufthansa', 'code': 'LH', 'multiplier': 1.05},
                {'name': 'Air France', 'code': 'AF', 'multiplier': 1.0},
                {'name': 'KLM', 'code': 'KL', 'multiplier': 1.0},
                {'name': 'Flydubai', 'code': 'FZ', 'multiplier': 0.8},
                {'name': 'Wizz Air', 'code': 'W6', 'multiplier': 0.7},
                {'name': 'Pobeda', 'code': 'DP', 'multiplier': 0.65},
                {'name': 'Red Wings', 'code': 'WZ', 'multiplier': 0.75}
            ]
            
            aircrafts = ['Airbus A320', 'Airbus A321', 'Boeing 737', 'Boeing 777', 'Boeing 787', 'Airbus A330', 'Embraer E190']
            
            # Base price calculation (20% below market prices)
            def calculate_base_price(from_code, to_code):
                base_prices = {
                    'domestic': 9600,   # Market: 12000
                    'europe': 20000,    # Market: 25000
                    'asia': 24000,      # Market: 30000
                    'america': 40000,   # Market: 50000
                    'africa': 32000,    # Market: 40000
                    'oceania': 48000    # Market: 60000
                }
                
                if from_code in ['MOW', 'LED', 'SVO', 'KZN', 'ROV'] and to_code in ['MOW', 'LED', 'SVO', 'KZN', 'ROV']:
                    return base_prices['domestic']
                elif to_code in ['PAR', 'LON', 'BCN', 'BER', 'ROM', 'AMS', 'PRG', 'CDG', 'LHR', 'MAD', 'FCO', 'MXP', 'FRA', 'MUC']:
                    return base_prices['europe']
                elif to_code in ['BKK', 'SIN', 'TYO', 'PEK', 'DXB', 'DEL', 'NRT', 'ICN', 'HKG', 'IST', 'AYT', 'DOH']:
                    return base_prices['asia']
                elif to_code in ['NYC', 'LAX', 'MIA', 'YTO', 'MEX', 'JFK', 'GRU']:
                    return base_prices['america']
                elif to_code in ['CAI', 'JNB', 'CMN', 'HRG', 'SSH']:
                    return base_prices['africa']
                else:
                    return base_prices['oceania']
            
            base_price = calculate_base_price(from_city, to_city)
            market_price_base = int(base_price / 0.8)
            
            mock_flights = []
            for i, airline in enumerate(random.sample(airlines, min(6, len(airlines)))):
                flight_num = f"{airline['code']}{random.randint(100, 9999)}"
                our_price = int(base_price * airline['multiplier'] * random.uniform(0.9, 1.1))
                market_price = int(our_price / 0.8)
                savings = market_price - our_price
                
                departure_hour = 6 + i * 3
                arrival_hour = departure_hour + random.randint(2, 8)
                
                stops = 0 if random.random() > 0.4 else 1
                duration_base = 2 if stops == 0 else 4
                duration = f"{duration_base + random.randint(0, 3)}ч {random.randint(0, 59)}м"
                
                mock_flights.append({
                    'id': flight_num,
                    'airline': airline['name'],
                    'origin': from_city,
                    'destination': to_city,
                    'departure_time': f"{departure_hour:02d}:{random.randint(0, 59):02d}",
                    'arrival_time': f"{arrival_hour % 24:02d}:{random.randint(0, 59):02d}",
                    'duration': duration,
                    'price': our_price,
                    'market_price': market_price,
                    'savings': savings,
                    'discount_percent': 20,
                    'currency': '₽',
                    'stops': stops,
                    'aircraft': random.choice(aircrafts)
                })
            
            mock_flights.sort(key=lambda x: x['price'])
            
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
                        'origin': from_city,
                        'destination': to_city,
                        'date': departure_date
                    }
                })
            }
        
        elif action == 'telegram':
            telegram_url = os.environ.get('TELEGRAM_BOT_URL', 'https://t.me/your_bot')
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'isBase64Encoded': False,
                'body': json.dumps({'telegram_url': telegram_url})
            }
        
        elif action == 'hotels':
            city = params.get('city', 'Москва')
            checkin = params.get('checkin', '2024-12-15')
            checkout = params.get('checkout', '2024-12-18')
            guests = int(params.get('guests', '2'))
            
            hotels = generate_hotels(city, checkin, checkout, guests)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'isBase64Encoded': False,
                'body': json.dumps({
                    'hotels': hotels,
                    'search_params': {
                        'city': city,
                        'checkin': checkin,
                        'checkout': checkout,
                        'guests': guests
                    }
                })
            }
        
        elif action == 'hotel_cities':
            cities = get_hotel_cities()
            
            query = params.get('q', '').lower()
            if query:
                cities = [city for city in cities if query in city.lower()]
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'isBase64Encoded': False,
                'body': json.dumps({'cities': cities[:50]})
            }
        
        elif action == 'popular':
            popular_destinations = [
                {'city': 'Париж', 'country': 'Франция', 'price': 'от 17 900 ₽', 'code': 'PAR', 'trend': '+5%'},
                {'city': 'Нью-Йорк', 'country': 'США', 'price': 'от 34 200 ₽', 'code': 'NYC', 'trend': '-2%'},
                {'city': 'Токио', 'country': 'Япония', 'price': 'от 37 900 ₽', 'code': 'TYO', 'trend': '+8%'},
                {'city': 'Лондон', 'country': 'Великобритания', 'price': 'от 19 800 ₽', 'code': 'LON', 'trend': '0%'},
                {'city': 'Дубай', 'country': 'ОАЭ', 'price': 'от 22 700 ₽', 'code': 'DXB', 'trend': '-3%'},
                {'city': 'Барселона', 'country': 'Испания', 'price': 'от 15 900 ₽', 'code': 'BCN', 'trend': '+1%'}
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

def generate_hotels(city: str, checkin: str, checkout: str, guests: int) -> List[Dict[str, Any]]:
    hotel_chains = [
        {'name': 'Marriott', 'multiplier': 1.3},
        {'name': 'Hilton', 'multiplier': 1.25},
        {'name': 'Hyatt', 'multiplier': 1.2},
        {'name': 'Radisson', 'multiplier': 1.0},
        {'name': 'Novotel', 'multiplier': 0.95},
        {'name': 'ibis', 'multiplier': 0.7},
        {'name': 'Holiday Inn', 'multiplier': 0.85},
        {'name': 'Best Western', 'multiplier': 0.8},
        {'name': 'DoubleTree', 'multiplier': 1.1},
        {'name': 'Crowne Plaza', 'multiplier': 1.15}
    ]
    
    city_base_prices = {
        'москва': 8000,
        'санкт-петербург': 6000,
        'сочи': 7000,
        'казань': 4500,
        'екатеринбург': 4000,
        'париж': 12000,
        'лондон': 15000,
        'нью-йорк': 18000,
        'дубай': 14000,
        'токио': 13000,
        'барселона': 9000,
        'рим': 10000,
        'стамбул': 5000,
        'бангкок': 4000,
        'сингапур': 11000,
        'бали': 6000,
        'пхукет': 5500,
        'майами': 16000,
        'лас-вегас': 12000
    }
    
    city_lower = city.lower()
    base_price = city_base_prices.get(city_lower, 6000)
    
    hotels = []
    num_hotels = min(random.randint(12, 20), 20)
    
    for i in range(num_hotels):
        chain = random.choice(hotel_chains)
        star_rating = random.randint(3, 5)
        
        night_price = int(base_price * chain['multiplier'] * random.uniform(0.9, 1.1))
        market_night_price = int(night_price / 0.75)
        
        try:
            from datetime import datetime as dt
            checkin_date = dt.strptime(checkin, '%Y-%m-%d')
            checkout_date = dt.strptime(checkout, '%Y-%m-%d')
            nights = max((checkout_date - checkin_date).days, 1)
        except:
            nights = 3
        
        total_price = night_price * nights
        market_total_price = market_night_price * nights
        savings = market_total_price - total_price
        
        hotel_types = ['Hotel', 'Resort', 'Inn', 'Suites', 'Plaza']
        hotel_name = f"{chain['name']} {random.choice(hotel_types)} {city}"
        
        amenities = random.sample([
            'Wi-Fi бесплатно',
            'Бассейн',
            'Спа-центр',
            'Фитнес-зал',
            'Ресторан',
            'Парковка',
            'Трансфер',
            'Кондиционер',
            'Мини-бар',
            'Сейф'
        ], k=random.randint(4, 7))
        
        hotels.append({
            'id': f"HTL{random.randint(10000, 99999)}",
            'name': hotel_name,
            'chain': chain['name'],
            'stars': star_rating,
            'rating': round(random.uniform(7.5, 9.8), 1),
            'reviews_count': random.randint(150, 3500),
            'price_per_night': night_price,
            'market_price_per_night': market_night_price,
            'total_price': total_price,
            'market_total_price': market_total_price,
            'savings': savings,
            'discount_percent': 25,
            'currency': '₽',
            'nights': nights,
            'address': f"{random.choice(['Центральный район', 'Исторический центр', 'Деловой район', 'Прибрежная зона'])}, {city}",
            'distance_to_center': round(random.uniform(0.3, 5.0), 1),
            'amenities': amenities,
            'room_type': random.choice(['Стандартный номер', 'Делюкс', 'Люкс', 'Семейный номер', 'Апартаменты']),
            'cancellation': random.choice(['Бесплатная отмена', 'Отмена за 48 часов', 'Без возврата']),
            'breakfast_included': random.choice([True, False]),
            'image': f"https://images.unsplash.com/photo-{random.randint(1500000000000, 1600000000000)}"
        })
    
    hotels.sort(key=lambda x: x['total_price'])
    return hotels

def get_hotel_cities() -> List[str]:
    return [
        'Москва', 'Санкт-Петербург', 'Сочи', 'Казань', 'Екатеринбург',
        'Новосибирск', 'Калининград', 'Владивосток', 'Красноярск', 'Иркутск',
        'Париж', 'Лондон', 'Барселона', 'Рим', 'Милан', 'Венеция',
        'Амстердам', 'Берлин', 'Мюнхен', 'Прага', 'Вена', 'Будапешт',
        'Стамбул', 'Анталья', 'Дубай', 'Абу-Даби', 'Доха',
        'Нью-Йорк', 'Лос-Анджелес', 'Майами', 'Лас-Вегас', 'Сан-Франциско',
        'Бангкок', 'Пхукет', 'Сингапур', 'Токио', 'Сеул', 'Гонконг',
        'Дели', 'Мумбаи', 'Гоа', 'Бали', 'Джакарта', 'Ханой', 'Хошимин',
        'Мальдивы', 'Сейшелы', 'Маврикий', 'Занзибар', 'Кейптаун'
    ]