import shutil
from pathlib import Path

import anyio


async def soft_delete_dir(path: Path):
    if path.exists():
        await anyio.to_thread.run_sync(shutil.rmtree, path)
