from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from bs4 import BeautifulSoup as b
import aiohttp


main_router = Router()

@main_router.message(CommandStart())
async def start_command(message: Message):
    await message.reply('Привет! Я бот спортивных новостей.')

# Пример команды /sport
@main_router.message(Command("sport"))
async def sport_command(message: Message):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Последние новости Футбола', callback_data='q_1')],
        [InlineKeyboardButton(text='Последние новости Хоккея', callback_data='q_2')],
        [InlineKeyboardButton(text='Последние новости Баскетбола', callback_data='q_3')]
    ])
    await message.reply('Вы можете выбрать:', reply_markup=button)

async def get_inf(url):
    # url = 'https://www.championat.com/football/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = b(text, 'html.parser')
                    news_items = soup.find_all('div', class_='article-preview')
                    
                    news_list = []
                    for item in news_items:
                        title = item.find('a', class_='article-preview__title').text.strip()
                        link = item.find('a')['href']
                        date = item.find('div', class_='article-preview__date').text.strip()
                        
                        news_list.append({
                            'title': title,
                            'link': link,
                            'date': date
                        })
                    
                    return news_list[:3]  # Возвращаем только первые три новости
                else:
                    return None
    except Exception as e:
        print(f"Ошибка при получении новостей: {e}")
        return None

# Обработка нажатий на кнопки
@main_router.callback_query(F.data.startswith("q_"))
async def process_callback(callback_query: CallbackQuery):
    if callback_query.data == 'q_1':
        url1 = 'https://www.championat.com/football/'
        inf = await get_inf(url1)  # Используем обновленную функцию
        if inf:
            await callback_query.message.answer(f"{inf[0]['date']} - {inf[0]['title']}\n{inf[0]['link']}\n")

    elif callback_query.data == 'q_2':
        url2 = 'https://www.championat.com/hockey/'
        inf = await get_inf(url2)  # Используем обновленную функцию
        if inf:
            await callback_query.message.answer(f"{inf[0]['date']} - {inf[0]['title']}\n{inf[0]['link']}\n")

    elif callback_query.data == 'q_3':
        url3 = 'https://www.championat.com/basketball/'
        inf = await get_inf(url3)  # Используем обновленную функцию
        if inf:
            await callback_query.message.answer(f"{inf[0]['date']} - {inf[0]['title']}\n{inf[0]['link']}\n")