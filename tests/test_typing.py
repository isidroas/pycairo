import os
import io
import types

import cairo


def test_typing():
    mod = types.ModuleType("cairo")
    stub = os.path.join(cairo.__path__[0], "__init__.pyi")
    with io.open(stub, "r", encoding="utf-8") as h:
        code = compile(h.read(), stub, "exec")
        exec(code, mod.__dict__)

    def collect_names(t):
        names = set()
        for key, value in vars(t).items():
            if key in ["XlibSurface", "XCBSurface", "Win32PrintingSurface",
                       "Win32Surface"]:
                continue
            if key.startswith("_"):
                continue
            if key.startswith("__") and key.endswith("__"):
                continue
            if getattr(value, "__module__", "") == "typing" or key == "Text":
                continue
            if isinstance(value, type):
                names.add(key)

                for k, v in vars(value).items():
                    name = key + "." + k
                    if k.startswith("_"):
                        continue
                    names.add(name)
            else:
                names.add(key)
        return names

    assert collect_names(cairo) <= collect_names(mod)
