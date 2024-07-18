import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class PhoneNumberApp(App):
    # Ваш ключ API от OpenCage Geocoding
    API_KEY = 'ad67351c1639443aaa31dee57be0b3c8'

    # Список кодов мест для Польши
    polish_city_codes = ['12', '22', '42', '52', '61', '71', '81', '91']

    # Список кодов мест для России
    russian_city_codes = ['495', '499', '812', '863', '862', '861', '831', '843', '844', '846', '343', '351', '347', '342', '381', '383', '3952', '391', '421', '423', '3462']

    def generate_phone_number(self):
        # Случайный выбор кода места
        city_code = random.choice(self.polish_city_codes + self.russian_city_codes)
        
        if city_code in self.polish_city_codes:
            country_code = "+48"
        elif city_code in self.russian_city_codes:
            country_code = "+7"
        
        # Генерация номера телефона с выбранным кодом места
        first_seven_numbers = str(random.randint(1000000, 9999999))
        return f"{country_code}{city_code}{first_seven_numbers}"

    def generate_valid_number(self):
        # Генерируем случайный номер телефона
        phone = self.generate_phone_number()

        # Проверяем, является ли номер действительным
        try:
            check_phone = phonenumbers.parse(phone)
            return phone
        except phonenumbers.phonenumberutil.NumberParseException:
            # Если номер недействителен, генерируем новый
            return self.generate_valid_number()

    def on_generate_number(self, instance):
        # Генерируем новый действительный номер телефона
        valid_number = self.generate_valid_number()
        self.phone_input.text = valid_number

    def on_check_number(self, instance):
        phone = self.phone_input.text

        try:
            check_phone = phonenumbers.parse(phone)
            number_location = geocoder.description_for_number(check_phone, "en")
            service_provider = carrier.name_for_number(check_phone, "en")
        
            geocoder_instance = OpenCageGeocode(self.API_KEY)
            query = str(number_location)
            result = geocoder_instance.geocode(query)
        
            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']
        
            self.output_label.text = f"Phone Number: {phone}\nLocation: {number_location}\nService Provider: {service_provider}\nLatitude: {lat}, Longitude: {lng}"
        except phonenumbers.phonenumberutil.NumberParseException:
            self.output_label.text = "Phone number does not exist."
        except Exception as e:
            self.output_label.text = f"An error occurred: {e}"

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.phone_input = TextInput(hint_text='Enter phone number')
        layout.add_widget(self.phone_input)
        
        generate_button = Button(text='Generate Random Number')
        generate_button.bind(on_press=self.on_generate_number)
        layout.add_widget(generate_button)
        
        check_button = Button(text='Check Number')
        check_button.bind(on_press=self.on_check_number)
        layout.add_widget(check_button)
        
        self.output_label = Label(text='')
        layout.add_widget(self.output_label)
        
        return layout

if __name__ == '__main__':
    PhoneNumberApp().run()
