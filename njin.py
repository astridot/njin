"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@          @@@@@@@             
     @@@@@@@@@@@@@@@           @@                 
       @@@@@@@@@@@@@                              
        @@@@@@@@@@@@                              
        @@@@@@@@@@@@              @@@@@@@@@       
        @@@@@@@@@@@@            @@@@@@@@@@@@      
        @@@@@@@@@@@@            @@@@@@@@@@@@      
        @@@@@@@@@@@@            @@@@@@@@@@@@      
        @@@@@@@@@@@@            @@@@@@@@@@@@      
        @@@@@@@@@@@@            @@@@@@@@@@@@      
        @@@@@@@@@@@@            @@@@@@@@@@@@      
        @@@@@@@@@@@@            @@@@@@@@@@@@       

-- welcome to your njin cli!

https://github.com/enjiprobably/njin/main/documentation.py for documentation

commands (cmd and powershell compatible):
~ py njin.py ~ run ./.n
~ py njin.py file.n ~ run ./file.n
~ py njin.py -help ~ get help for njin
~ py njin.py -cl ~ launch the njin command line interface
~ py njin.py -version ~ get the current version of njin on your system
~ py njin.py -ping ~ see how fast njin is running
~ py njin.py -upgrade ~ upgrade njin on your system

njin 2024 developed by enjiprobably from JΛVOLINN STUDIOS
[-] github.com/enjiprobably/njin
"""

try:
    import os
    import sys
    from typing import Any, Final
    from base64 import b64decode
    from importlib import import_module
    from time import perf_counter

    SYSVER: Final[str] = "njin4"

    class NjinError(Exception):
        ...

    class Lang:
        def __init__(self, name: str, ext: str, static: str | None) -> None:
            self.name: str = name
            self.ext: str = ext
            self.static: str | None = static

    class File:
        def __init__(self, name: str, root: Lang, path: str) -> None:
            self.name: str = name
            self.root: Lang = root
            self.path: str = path

    class Interface:
        def __init__(self, name: str, extends: list[str]) -> None:
            self.name: str = name
            self.extends: list[str] = extends

    class Commands:
        @staticmethod
        def help(_) -> None:
            print("""
get help for njin:

~ check out the documentation at
  [-] https://github.com/enjiprobably/njin/blob/main/documentation.md

~ get help on Garnet.com at
  [-] https://javolinn.wixsite.com/garnet/forum/questions-answers

~ see reported issues or post one yourself at
  [-] https://github.com/enjiprobably/njin/issues

~ troubleshoot your code by adding `-e` in your command
  to disable user-friendly errors and show advanced internal errors instead.
""")

        @staticmethod
        def cl(_) -> None:
            while True:
                cmd: str = input("py njin.py >> ")
                if cmd == "exit":
                    exit()
                os.system(f"py njin.py {cmd if cmd != "" else "-f"} -l")
                
        @staticmethod
        def version(_) -> None:
            print("your system is running " + SYSVER)

        @staticmethod
        def ping(start: float) -> None:
            print(f"Pong! {((perf_counter() - start) * 1000):.6f}ms ({(perf_counter() - start):.6f}s)")

        @staticmethod
        def upgrade(_) -> None:
            print(
"""
your system is currently running {}
                  
to upgrade your njin, follow any of these steps:
~ use `gh repo sync` if you loaded this from GitHub

~ re-download a zip from our GitHub repository at
  [-] https://github.com/enjiprobably/njin

~ check for updates at
  [-] https://javolinn.wixsite.com/garnet/forum/production

~ if you're an njineer, you can request a new release on
  the JΛVOLINN*njin Discord server.


(i) need help? run `py njin.py -help` to see how you can get support.
""".format(SYSVER))
                
    def fetch(path: str) -> str:
        with open(path, encoding="utf8") as file:
            c: str = file.read()

        return c
    
    troubleshooting: bool = False

    class Main:
        def __init__(self) -> None:
            ...

        def main(
                self,
                path: str,
                njin_loaded: bool = True,
                tbs: bool = False,
                start: float = 0.0,
                create: bool = False
            ) -> list[str]:
            if path == "-f":
                path = ".n"

            elif path.startswith("-"):
                eval(f"Commands.{path[1:]}(start)", {"Commands": Commands, "start": start})

                return []

            if njin_loaded:
                print("\033[1m~njin loaded\033[0m\n\n\n")

            self.pkgs: dict[str, dict[str, Lang]] = {}
            self.layers: dict[str|None, Any] = {}
            self.public: dict[str, list[str]] = {}
            self.files: dict[str, File] = {}

            global troubleshooting
            
            troubleshooting = tbs

            try:
                c: str = fetch(path).replace("\\\n", "")
            except FileNotFoundError as exc:
                if not create:
                    raise exc
                with open(path, "w") as _: ...
                c: str = fetch(path).replace("\\\n", "")

            lns: list[str] = c.split("\n") + ["return false"]

            self.comment: bool = False

            return lns

        def loop(self, ln: str) -> bool|None:
            if self.comment:
                if ln.endswith("*/"):
                    self.comment = False

            elif ln.startswith("//"):
                ...

            elif ln.startswith("/*"):
                self.comment = True

            elif ln.startswith("assert "):
                if fn := self.parseAssert(ln) is not None:
                    return fn

            elif ln.startswith("package "):
                self.parsePackage(ln)

            elif ln.startswith("return "):
                return self.parseReturn(ln)

            elif ln.startswith("public "):
                self.parsePublic(ln)

            elif ln.startswith("private "):
                self.parsePrivate(ln)

            elif ln.startswith("protected "):
                self.parseProtected(ln)

            elif ln.startswith("class "):
                self.parseClass(ln)

            elif ln.startswith("abstract class "):
                self.parseAbstractClass(ln)
        
            elif ln.startswith("new "):
                self.parseNew(ln)

            elif ln.startswith("try "):
                self.parseTry(ln)

            elif ln.startswith("interface "):
                self.parseInterface(ln)

            elif ln.startswith("import "):
                self.parseImport(ln)

            elif ln.startswith("super "):
                self.parseSuper(ln)

            elif ln.startswith("[\"") and ln.endswith("\"]"):
                os.system(ln.strip("[\"]"))
                
            elif ln in ("}", "break"):
                self.layers.popitem()
        
        def parseAssert(self, ln: str) -> bool | None:
            parts: list[str] = ln.strip().removeprefix("assert ").split(" ")

            id: str = parts[0]

            if not main_func(id, perf_counter()):
                return False

        def parsePackage(self, ln: str) -> None:
            parts: list[str] = ln.strip().removeprefix("package ").split(" ")

            self.layers.update({None: parts[0]})
            self.public.update({parts[0]: []})

        def parseReturn(self, ln: str) -> bool | None:
            parts: list[str] = ln.strip().removeprefix("return ").split(" ")

            match parts[0]:
                case "true":
                    return True
                
                case "false":
                    return False
                
        def parseModule(self, ln: str, struct: str, name: str) -> None:
            parts: list[str] = ln.strip().removeprefix(name).split(" ")

            mod: str = list(self.layers.values())[-1]

            if parts[0] in [i for i in list(self.pkgs[mod].keys())]:
                self.public[list(self.layers.values())[-1]].append(struct.format(
                    name=parts[0],
                    module=mod
                ))

            else:
                raise NameError(f"njin: no implementation '{parts[0]}' in extendant '{list(self.layers.values())[-1]}'")
                
        def parsePublic(self, ln: str) -> None:
            self.parseModule(ln, "{name}", "public ")
            
        def parsePrivate(self, ln: str) -> None:
            self.parseModule(ln, "{module}", "private ")

        def parseProtected(self, ln: str) -> None:
            self.parseModule(ln, "{module}.{name}", "protected ")
            
        def parseClass(self, ln: str) -> None:
            parts: list[str] = ln.removeprefix("class ").split(" ")

            if "extends" not in " ".join(parts):
                self.layers.update({parts[0]: None})

            elif parts[1] != "extends" or parts[3] != "implements":
                raise SyntaxError("njin: expected extendant and implementation")

            elif parts[4] not in self.public[parts[2]]:
                raise TypeError("njin: invalid implementation")
            
            else:
                self.layers.update({parts[0]: self.pkgs[parts[2]][parts[4].split(".")[-1][0].upper() + parts[4].split(".")[-1][1:]]})
        
        def parseAbstractClass(self, ln: str) -> None:
            parts: list[str] = ln.removeprefix("abstract class ").split(" ")

            id = {
                0: "build",
                1: "dist"
            }[int(parts[0])]

            if "extends" not in " ".join(parts):
                self.layers.update({parts[0]: None})

            elif parts[1] != "extends" or parts[3] != "implements":
                raise SyntaxError("njin: expected extendant and implementation")

            elif parts[4] not in self.public[parts[2]]:
                raise TypeError("njin: invalid implementation")
            
            else:
                self.layers.update({id: self.pkgs[parts[2]][parts[4].split(".")[-1][0].upper() + parts[4].split(".")[-1][1:]]})

        def parseNew(self, ln: str) -> None:
            parts: list[str] = ln.removeprefix("new ").split(" ")

            name: str = parts[0]
            o: Lang | None = list(self.layers.values())[-1]

            if o is None:
                raise TypeError("njin: cannot create variables in non-extending class/interface")

            fn: str = f"{name}.{o.ext}"

            path: str = "/".join([layer for layer in self.layers if layer is not None])

            if not path.startswith("njin/"):
                raise NameError("njin: cannot create variables without global main-level interface 'njin'")

            path = path.removeprefix("njin/")

            self.files.update({name: File(
                name,
                o,
                path
            )})

        def parseTry(self, ln: str) -> None:
            parts: list[str] = ln.removeprefix("try ").split(" ")

            file: File = self.files[parts[0]]
            root: Lang = file.root

            fn: str = f"{file.name}.{root.ext}"

            if not parts[1].startswith("[") or not parts[1].endswith("]"):
                raise SyntaxError(f"njin: argument 2 should be a sq. bracket structure")

            else:
                cmd: str = parts[1].strip("[\"]")
                cmd = cmd.format(fn, fn=file.name)

            if cmd == "static" and root.static is not None:
                cmd = root.static
            else:
                try:
                    cmd = eval(repr(cmd))

                    if not isinstance(cmd, str) or 1 == 0:
                        raise TypeError("type is not 'str'")
                    
                except Exception as err:
                    raise SyntaxError(f"njin: python 'eval' error in 'str': '{repr(err)}'")
                
            after: str = " ".join(parts[2:]).strip()

            if after != "":
                args: tuple[str, ...] = eval((after.strip(")") + ",)") if after != "()" else "tuple()")

                if not isinstance(args, tuple) or 1 == 0:
                    raise SyntaxError("njin: args is not 'tuple'")
            else:
                args: tuple[str, ...] = tuple()

            os.system(f"{cmd} {file.path}/{fn} {' '.join(args)}")

        def parseInterface(self, ln: str) -> None:
            parts: list[str] = ln.removeprefix("interface ").split(" ")

            if "extends" not in " ".join(parts):
                self.layers.update({parts[0]: None})

            elif parts[1] != "extends" or parts[3] != "implements":
                raise SyntaxError("njin: expected extendant and implementation")

            elif parts[4] not in self.public[parts[2]]:
                raise TypeError("njin: invalid implementation")
            
            else:
                self.layers.update({None: self.pkgs[parts[2]][parts[4].split(".")[-1][0].upper() + parts[4].split(".")[-1][1:]]})

        def parseImport(self, ln: str) -> None:
            path: str = ln.removeprefix("import ")

            c_: dict[str, dict[str, Lang]] | None = eval(b64decode(fetch(path).replace("\n", "")), None, {"Lang": Lang})

            if isinstance(c_, dict):
                self.pkgs |= c_

            else:
                raise TypeError("njin: there was an error while loading an import")
            
        def parseSuper(self, ln: str) -> None:
            parts: list[str] = ln.removeprefix("super ").split(" ")

            self.parseNew(f"new {parts[0]}")
            self.parseTry(f"try {' '.join(parts)}")

    def main_func(path: str, start: float) -> bool:
        main: Main = Main()
        for ln in main.main(path, "-c" not in sys.argv, "-e" in sys.argv, start, "-F" in sys.argv):
            if (fn := main.loop(ln.strip())) is not None:
                return fn
        return False

    if __name__ == "__main__":
        start: float = perf_counter()
        r: bool = main_func((sys.argv[1] if len(sys.argv) >= 2 else ".n"), start)
        if "-l" in sys.argv:
            print(f"{sys.argv[1]}.n >> {str(r).lower()}")

except Exception as exc:
    if not troubleshooting:
        raise NjinError("a fatal error occured while parsing njin and the system couldn't recover :(\n\nplease review your code and try again")
    else:
        raise exc