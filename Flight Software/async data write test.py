import asyncio
import time
import aiofiles

data_log = []


async def async_write_data():
    while True:
        await asyncio.sleep(0.1)  # Adjust as needed
        if data_log:
            print(f"Writing {len(data_log)} lines to file")
            async with aiofiles.open('data_log.csv', 'a') as file:
                await file.write(','.join(map(str, data_log)) + '\n')
                print(f"Writing {data_log} lines to file")
            data_log.clear()
            print(f"Data log cleared. {len(data_log)} lines remaining")

async def main():
    # Start the asynchronous file writing task
    write_task = asyncio.create_task(async_write_data())

    # Your main loop
    for i in range(100):    
        data_log.append(i)
        print(i)
        await asyncio.sleep(0.03)  # 0.05 seems to be god to demonstrate writing as fast as possible while still having a delay

    # Wait for the write task to finish
    await write_task

if __name__ == "__main__":
    asyncio.run(main())
