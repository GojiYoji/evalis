import importlib.util
from pathlib import Path
import sys
from typing import Any, Tuple
import hashlib

# Cache: {(path): (mtime, module_name, module)}
_type_cache: dict[str, Tuple[float, str, Any]] = {}


def hash_path(path: Path) -> str:
    return hashlib.md5(str(path.resolve()).encode()).hexdigest()[:8]


def load_module_from_path(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"Expected path to exist ({path}). Found not exists.")
    if not path.is_file():
        raise ValueError(f"Expected path to be file ({path}). Found not a file.")

    mtime = path.stat().st_mtime
    key = str(path.resolve())

    # Check cache
    if key in _type_cache:
        cached_mtime, cached_module_name, cached_module = _type_cache[key]
        if cached_mtime == mtime:
            return cached_module
        else:
            # mtime changed — evict old entry
            del _type_cache[key]
            sys.modules.pop(cached_module_name, None)

    # Load module dynamically
    module_name = f"_dynamic_{path.stem}_{hash_path(path)}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if not spec or not spec.loader:
        raise ImportError(f"Could not load module from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # Optional: for introspection/imports
    spec.loader.exec_module(module)

    _type_cache[key] = (mtime, module_name, module)
    return module


def load_type_from_path(path: Path, type_name: str) -> Any:
    module = load_module_from_path(path)

    try:
        return getattr(module, type_name)
    except AttributeError:
        raise ImportError(f"Module at '{str(path)}' has no attribute '{type_name}'")


def clear_cache() -> None:
    _type_cache.clear()
