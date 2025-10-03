import { useState, useEffect, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Autocomplete } from "@/components/ui/autocomplete";
import Icon from '@/components/ui/icon';

interface City {
  code: string;
  name: string;
  country: string;
}

interface Flight {
  id: string;
  airline: string;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  duration: string;
  price: number;
  market_price?: number;
  savings?: number;
  discount_percent?: number;
  currency: string;
  stops: number;
  aircraft: string;
}

interface Hotel {
  id: string;
  name: string;
  chain: string;
  stars: number;
  rating: number;
  reviews_count: number;
  price_per_night: number;
  market_price_per_night: number;
  total_price: number;
  market_total_price: number;
  savings: number;
  discount_percent: number;
  currency: string;
  nights: number;
  address: string;
  distance_to_center: number;
  amenities: string[];
  room_type: string;
  cancellation: string;
  breakfast_included: boolean;
}

const Index = () => {
  const [activeTab, setActiveTab] = useState<'flights' | 'hotels'>('flights');
  const [fromCity, setFromCity] = useState('');
  const [toCity, setToCity] = useState('');
  const [departDate, setDepartDate] = useState('');
  const [returnDate, setReturnDate] = useState('');
  const [cities, setCities] = useState<City[]>([]);
  const [filteredFromCities, setFilteredFromCities] = useState<City[]>([]);
  const [filteredToCities, setFilteredToCities] = useState<City[]>([]);
  const [flights, setFlights] = useState<Flight[]>([]);
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [hotelCity, setHotelCity] = useState('');
  const [hotelCheckin, setHotelCheckin] = useState('');
  const [hotelCheckout, setHotelCheckout] = useState('');
  const [hotelGuests, setHotelGuests] = useState('2');
  const [hotelCities, setHotelCities] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [selectedFromCity, setSelectedFromCity] = useState<City | null>(null);
  const [selectedToCity, setSelectedToCity] = useState<City | null>(null);
  const [telegramUrl, setTelegramUrl] = useState('');

  // Fetch cities and telegram URL on component mount
  useEffect(() => {
    fetchCities();
    fetchTelegramUrl();
  }, []);

  const fetchCities = async () => {
    try {
      setLoading(true);
      const response = await fetch('https://functions.poehali.dev/6cdc378e-a07f-445d-bf2d-624439860b60?action=cities');
      const data = await response.json();
      setCities(data.cities || []);
      setFilteredFromCities(data.cities || []);
      setFilteredToCities(data.cities || []);
    } catch (error) {
      console.error('Error fetching cities:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterCities = useCallback((query: string, exclude?: string) => {
    if (!query) return cities;
    const filtered = cities.filter(city => 
      (city.name.toLowerCase().includes(query.toLowerCase()) || 
       city.country.toLowerCase().includes(query.toLowerCase())) &&
      city.code !== exclude
    );
    return filtered.slice(0, 8); // Limit results
  }, [cities]);

  const handleFromCityChange = (value: string) => {
    setFromCity(value);
    setFilteredFromCities(filterCities(value, selectedToCity?.code));
  };

  const handleToCityChange = (value: string) => {
    setToCity(value);
    setFilteredToCities(filterCities(value, selectedFromCity?.code));
  };

  const handleFromCitySelect = (city: City) => {
    setSelectedFromCity(city);
    setFromCity(city.name);
  };

  const handleToCitySelect = (city: City) => {
    setSelectedToCity(city);
    setToCity(city.name);
  };

  const fetchTelegramUrl = async () => {
    try {
      const response = await fetch('https://functions.poehali.dev/6cdc378e-a07f-445d-bf2d-624439860b60?action=telegram');
      const data = await response.json();
      setTelegramUrl(data.telegram_url || 'https://t.me/your_bot');
    } catch (error) {
      console.error('Error fetching telegram URL:', error);
    }
  };

  const searchFlights = async () => {
    if (!selectedFromCity || !selectedToCity || !departDate) {
      alert('Пожалуйста, заполните все поля поиска');
      return;
    }

    try {
      setSearchLoading(true);
      const params = new URLSearchParams({
        action: 'search',
        from: selectedFromCity.code,
        to: selectedToCity.code,
        date: departDate
      });
      
      const response = await fetch(`https://functions.poehali.dev/6cdc378e-a07f-445d-bf2d-624439860b60?${params}`);
      const data = await response.json();
      setFlights(data.flights || []);
    } catch (error) {
      console.error('Error searching flights:', error);
    } finally {
      setSearchLoading(false);
    }
  };

  const buyTicket = (flight: Flight) => {
    const message = `Рейс ${flight.airline} ${flight.id}\n${flight.origin} → ${flight.destination}\n${flight.departure_time} - ${flight.arrival_time}\nЦена: ${flight.price.toLocaleString()} ${flight.currency}`;
    const url = `${telegramUrl}?start=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
  };

  const popularDestinations = [
    { city: 'Париж', country: 'Франция', price: 'от 20 000 ₽', oldPrice: '25 000 ₽', image: '🇫🇷' },
    { city: 'Нью-Йорк', country: 'США', price: 'от 36 000 ₽', oldPrice: '45 000 ₽', image: '🇺🇸' },
    { city: 'Токио', country: 'Япония', price: 'от 44 000 ₽', oldPrice: '55 000 ₽', image: '🇯🇵' },
    { city: 'Лондон', country: 'Великобритания', price: 'от 22 400 ₽', oldPrice: '28 000 ₽', image: '🇬🇧' },
    { city: 'Дубай', country: 'ОАЭ', price: 'от 25 600 ₽', oldPrice: '32 000 ₽', image: '🇦🇪' },
    { city: 'Барселона', country: 'Испания', price: 'от 17 600 ₽', oldPrice: '22 000 ₽', image: '🇪🇸' }
  ];

  const specialOffers = [
    { title: 'Раннее бронирование', discount: '-30%', description: 'Скидка на билеты за 60 дней до вылета', color: 'bg-green-100 text-green-800' },
    { title: 'Горящие туры', discount: '-50%', description: 'Билеты на завтра и послезавтра', color: 'bg-red-100 text-red-800' },
    { title: 'Семейные билеты', discount: '-25%', description: 'При покупке от 3 билетов', color: 'bg-blue-100 text-blue-800' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-sky-50 to-white">
      {/* Header */}
      <header className="bg-white/90 backdrop-blur-md border-b border-sky-100 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Icon name="Plane" size={28} className="text-sky-500" />
            <span className="text-2xl font-bold text-gray-900">AviaSky</span>
          </div>
          <nav className="flex items-center space-x-6">
            <a href="#" className="text-gray-600 hover:text-sky-600 transition-colors">Билеты</a>
            <a href="#" className="text-gray-600 hover:text-sky-600 transition-colors">Отели</a>
            <a href="#" className="text-gray-600 hover:text-sky-600 transition-colors">Поддержка</a>
            <Button variant="outline" size="sm">Войти</Button>
          </nav>
        </div>
      </header>

      {/* Hero Section with Search */}
      <section className="relative py-20 px-4 bg-sky-gradient">
        <div 
          className="absolute inset-0 opacity-30"
          style={{
            backgroundImage: 'url(/img/60a00755-7517-43b7-b64c-b53d1b321e25.jpg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}
        />
        <div className="relative container mx-auto text-center">
          <h1 className="text-5xl font-bold text-white mb-4 animate-fade-in">
            Авиабилеты на 20% дешевле рынка
          </h1>
          <p className="text-xl text-white/90 mb-12 animate-fade-in">
            200+ городов • Реальный парсинг цен • Гарантия лучшей цены
          </p>
          <Badge className="mb-8 bg-green-500 text-white text-lg px-6 py-2">
            <Icon name="TrendingDown" size={20} className="mr-2" />
            Скидка 20% на все рейсы
          </Badge>

          {/* Search Form */}
          <Card className="max-w-4xl mx-auto bg-white/95 backdrop-blur-md shadow-2xl animate-scale-in">
            <CardContent className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <Autocomplete
                  placeholder="Откуда"
                  value={fromCity}
                  onChange={handleFromCityChange}
                  onSelect={handleFromCitySelect}
                  options={filteredFromCities}
                  loading={loading}
                  icon="MapPin"
                />
                <Autocomplete
                  placeholder="Куда"
                  value={toCity}
                  onChange={handleToCityChange}
                  onSelect={handleToCitySelect}
                  options={filteredToCities}
                  loading={loading}
                  icon="Navigation"
                />
                <div className="relative">
                  <Icon name="Calendar" size={20} className="absolute left-3 top-3 text-gray-400" />
                  <Input
                    type="date"
                    value={departDate}
                    onChange={(e) => setDepartDate(e.target.value)}
                    className="pl-10 h-12"
                  />
                </div>
                <div className="relative">
                  <Icon name="Calendar" size={20} className="absolute left-3 top-3 text-gray-400" />
                  <Input
                    type="date"
                    value={returnDate}
                    onChange={(e) => setReturnDate(e.target.value)}
                    placeholder="Обратно"
                    className="pl-10 h-12"
                  />
                </div>
              </div>
              <Button 
                size="lg" 
                className="w-full h-12 bg-sky-500 hover:bg-sky-600 text-white font-semibold"
                onClick={searchFlights}
                disabled={searchLoading}
              >
                <Icon name={searchLoading ? "Loader2" : "Search"} size={20} className={`mr-2 ${searchLoading ? 'animate-spin' : ''}`} />
                {searchLoading ? 'Поиск...' : 'Найти билеты'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Flight Results */}
      {flights.length > 0 && (
        <section className="py-16 px-4 bg-white">
          <div className="container mx-auto">
            <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
              Результаты поиска
            </h2>
            <div className="max-w-4xl mx-auto space-y-4">
              {flights.map((flight, index) => (
                <Card key={flight.id} className="hover:shadow-lg transition-all duration-300 animate-fade-in">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-4">
                          <div className="text-center">
                            <div className="text-2xl font-bold text-gray-900">{flight.departure_time}</div>
                            <div className="text-sm text-gray-500">{flight.origin}</div>
                          </div>
                          <div className="flex-1 text-center">
                            <div className="flex items-center justify-center space-x-2">
                              <div className="h-px bg-gray-300 flex-1"></div>
                              <Icon name="Plane" size={20} className="text-sky-500" />
                              <div className="h-px bg-gray-300 flex-1"></div>
                            </div>
                            <div className="text-sm text-gray-500 mt-1">{flight.duration}</div>
                            {flight.stops > 0 && (
                              <div className="text-xs text-orange-600">{flight.stops} пересадка</div>
                            )}
                          </div>
                          <div className="text-center">
                            <div className="text-2xl font-bold text-gray-900">{flight.arrival_time}</div>
                            <div className="text-sm text-gray-500">{flight.destination}</div>
                          </div>
                        </div>
                        <div className="mt-4 flex items-center justify-between">
                          <div>
                            <div className="font-medium text-gray-900">{flight.airline}</div>
                            <div className="text-sm text-gray-500">{flight.aircraft}</div>
                          </div>
                          <div className="text-right">
                            {flight.market_price && (
                              <div className="text-sm text-gray-400 line-through">
                                {flight.market_price.toLocaleString()} {flight.currency}
                              </div>
                            )}
                            <div className="text-3xl font-bold text-green-600">
                              {flight.price.toLocaleString()} {flight.currency}
                            </div>
                            {flight.savings && (
                              <Badge className="mt-1 bg-green-500 text-white">
                                -20% • Экономия {flight.savings.toLocaleString()} ₽
                              </Badge>
                            )}
                            <Button 
                              className="mt-2 bg-green-500 hover:bg-green-600 w-full"
                              onClick={() => buyTicket(flight)}
                            >
                              <Icon name="ShoppingCart" size={18} className="mr-2" />
                              Купить
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Popular Destinations */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Популярные направления
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {popularDestinations.map((destination, index) => (
              <Card key={index} className="group hover:shadow-lg transition-all duration-300 cursor-pointer animate-fade-in">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="text-4xl">{destination.image}</div>
                    <div className="text-right">
                      <div className="text-xs text-gray-400 line-through">{destination.oldPrice}</div>
                      <Badge variant="secondary" className="bg-green-100 text-green-800">
                        {destination.price}
                      </Badge>
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-1">
                    {destination.city}
                  </h3>
                  <p className="text-gray-600 text-sm">{destination.country}</p>
                  <Badge className="mt-2 bg-green-500 text-white text-xs">
                    -20% скидка
                  </Badge>
                  <div className="mt-4 flex items-center text-sky-600 group-hover:text-sky-700 transition-colors">
                    <span className="text-sm font-medium">Подробнее</span>
                    <Icon name="ArrowRight" size={16} className="ml-1" />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Special Offers */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Спецпредложения и скидки
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {specialOffers.map((offer, index) => (
              <Card key={index} className="hover:shadow-lg transition-all duration-300 animate-fade-in">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{offer.title}</CardTitle>
                    <Badge className={offer.color}>
                      {offer.discount}
                    </Badge>
                  </div>
                  <CardDescription className="text-gray-600">
                    {offer.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button variant="outline" className="w-full">
                    Узнать больше
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Почему выбирают нас
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center animate-fade-in">
              <div className="w-16 h-16 bg-sky-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-float">
                <Icon name="Shield" size={32} className="text-sky-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Безопасность</h3>
              <p className="text-gray-600">Все платежи защищены. Работаем только с проверенными авиакомпаниями</p>
            </div>
            <div className="text-center animate-fade-in">
              <div className="w-16 h-16 bg-sky-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-float">
                <Icon name="Clock" size={32} className="text-sky-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">24/7 поддержка</h3>
              <p className="text-gray-600">Круглосуточная техническая поддержка поможет в любой ситуации</p>
            </div>
            <div className="text-center animate-fade-in">
              <div className="w-16 h-16 bg-sky-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-float">
                <Icon name="Percent" size={32} className="text-sky-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Скидка 20%</h3>
              <p className="text-gray-600">Парсим цены конкурентов и делаем на 20% дешевле. Гарантия лучшей цены</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Icon name="Plane" size={24} className="text-sky-400" />
                <span className="text-xl font-bold">AviaSky</span>
              </div>
              <p className="text-gray-400">
                Ваш надежный помощник в поиске авиабилетов по всему миру
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Услуги</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Авиабилеты</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Отели</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Трансфер</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Поддержка</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Помощь</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Контакты</a></li>
                <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Контакты</h4>
              <div className="space-y-2 text-gray-400">
                <p>+7 (800) 123-45-67</p>
                <p>info@aviasky.ru</p>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 AviaSky. Все права защищены.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;