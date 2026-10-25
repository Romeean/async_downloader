from async_download_manager import download
import asyncio

if __name__ == "__main__":
    asyncio.run(download (
        "https://dev.to/outdated-dev/generate-random-strings-with-python-a-quick-guide-1nfm",
        "https://www.reddit.com/r/learnpython/comments/11tapnb/async_programming_in_python_looking_for_the_best/"
    ))
