import asyncio
from create_bot import bot, dp, database
from handlers.start import start_router, money_router

async def main():
    await database.init()
    dp.include_router(start_router)
    dp.include_router(money_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())