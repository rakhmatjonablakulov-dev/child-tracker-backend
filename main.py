
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# Сюда импортируйте функцию запуска вашего бота
# from my_bot import start_bot_loop

class BotControlApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.status_label = Label(text="Статус: Остановлен", font_size='20sp')
        
        btn_start = Button(text="Запустить бота", size_hint=(1, 0.3))
        btn_start.bind(on_press=self.run_bot)
        
        layout.add_widget(self.status_label)
        layout.add_widget(btn_start)
        return layout

    def run_bot(self, instance):
        self.status_label.text = "Статус: Запущен в фоне..."
        # Запускаем бота в отдельном потоке, чтобы не завис экран
        threading.Thread(target=self.bot_worker, daemon=True).start()

    def bot_worker(self):
        # Здесь вызывается цикл вашего бота (например, asyncio.run(main()))
        pass

if __name__ == '__main__':
    BotControlApp().run()
