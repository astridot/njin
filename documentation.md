```
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
```

**njin** is a micro language designed to organize the flow of files in your project.

### Statements and Syntax:

#### `package <PATH> {}` - Load an external package (extendant) from any import

**Example:**
```njin
import buckshot.nlib
import j-njin.nlib

package python {}
```
This initializes the `python` package from the `buckshot` module because `j-njin` has no package named `python`. If two imports are imported and they both have a package with the same name, an overlap error is raised.

#### `public <NAME>` - Load an implementation from a package. Accessed as `<implementation>`

**Example:**
```njin
import buckshot.nlib
import j-njin.nlib

package python {
    public Python
}
```
This initializes the `Python` implementation from the `python` extendant. Implementations hold 2 main attributes:
- **extension**: the file extension for the file (e.g., 'py' for Python files, 'c' for C files)
- **static**: how the file type is usually run in cmd (e.g., 'py' for Python files, 'gcc' for C files, 'start' for HTML files)

#### `protected <NAME>` - Similar to public, but the implementation can be accessed as `<extendant>.<implementation>` rather than just `<implementation>`

- Referring to public implementation: `Python`
- Referring to protected implementation: `python.Python`

#### `private <NAME>` - Create a representative implementation for the extendant. Accessed as `<extendant>`. ONLY ONE PER PACKAGE!

- Referring to public implementation: `Python`
- Referring to protected implementation: `python.Python`
- Referring to private implementation: `python`

#### `class <NAME> extends <EXTENDANT> implements <IMPLEMENTATION> {}` - Create a directory with files of a certain type

**Example:**
```njin
import buckshot.nlib
import j-njin.nlib

package python {
    public Python
}

class MyProject extends python implements Python {

}
```
Defining a class adds a layer to the execution path. While in a class, the pointer navigates to `./MyProject/`. If you need to reach `./MyProject/build/A/` do this:

```njin
class MyProject extends python implements Python {
    class build extends python implements Python {
        class A extends python implements Python {
            // here
        }
    }
}
```

#### `class <NAME> {}` - This is actually a different statement from the last one

The difference is `extends` and `implements`. This class does not extend nor implement anything, so files cannot be run here. This makes it easier to navigate through directories if you don't need to create files there.

**Example:**
```njin
class MyProject {
    class build {
        class A extends python implements Python {
            // you can create files here
        }
        // but not here
    }
    // or here
}
```

#### `abstract class <TYPE> extends <EXTENDANT> implements <IMPLEMENTATION> {}`

We'll talk about both the non-extending and extending version in this one chapter. Abstract classes don't take a name; they take a type. A type can be either `0` or `1`. If the type is `0`, the name becomes `build`. If `1`, the name becomes `dist`. When you have either of these directories in your project, it's a common convention to opt for `abstract class 0` or `abstract class 1` instead of `class build` or `class dist`.

**Example:**
```njin
class MyProject {
    abstract class 0 {
        class A extends python implements Python {
            // here is still ./MyProject/build/A/
        }
    }
}
```

#### `new <NAME>` - The statement to create variables

Variables in njin don't behave as you'd expect though. When you create a variable, a file name is assigned. Variables can only be created in extending layers.

**Example:**
```njin
import buckshot.nlib

package python {
    public Python
}

package javascript {
    private JavaScript
}

package c {
    protected GCC // gcc is the compiler for C
}

class MyProject extends c implements c.GCC {
    new main // this variable points to ./MyProject/main.c

    abstract class 0 extends javascript implements javascript {
        new start // this variable points to ./MyProject/build/start.js
    }

    abstract class 1 extends python implements Python {
        new start // this variable points to ./MyProject/dist/start.py
    }

    class HelloWorld {
        new main /* this line raises an error, because there is no file
                  * extension that can be assigned since ./MyProject/HelloWorld
                  * does not extend nor implement anything.
                  */
    }
}
```

#### `try <VARIABLENAME> <METHOD> [ARGS]` - `try` actually runs the files

First, add your variable, then a method, and then optional arguments. Command structure: `<method> <name>.<extension> <args>`. The method is always in square brackets and args are surrounded by parentheses. If you set the method to be `[static]`, the default for that file will be used.

**Example:**
```njin
import buckshot.nlib

package python {
    public Python
}

package javascript {
    private JavaScript // javascript.JavaScript has no static,
    protected NodeJS    // but javascript.NodeJS does have one
}

package htmlcss {
    protected HTML
}

class MyProject extends htmlcss implements htmlcss.HTML {
    new index // this variable points to ./MyProject/index.html
    try index ["start chrome"] // this runs `start chrome ./MyProject/index.html`

    abstract class 0 extends javascript implements javascript.NodeJS {
        new start // this variable points to ./MyProject/build/start.js
        try start [static] // this runs `node ./MyProject/build/start.js`
    }

    abstract class 1 extends python implements Python {
        new start // this variable points to ./MyProject/dist/start.py
        try start [static] ("these", "are", "passed", "as", "sys.argv")
        try start ["python3.12"] // if you need to use a specific version
    }
}
```

#### `interface <NAME> extends <EXTENDANT> implements <IMPLEMENTATION> {}` - Interfaces are like classes, but they don't add layers to the path

The name is just so it can be more readable.

**Example:**
```njin
class MyProject {
    // this class doesn't extend anything, so we can't create files here
    // here is ./MyProject

    interface PyInterface extends python implements Python {
        // we can create .py files here though
        // here is still ./MyProject
    }
}
```

#### `interface <NAME> {}` - Interfaces that don't extend are completely useless, apart from one exception

Your njin can't use `try` if the base isn't a non-extending, non-implementing interface `njin`.

**Example 1:**
```njin
class MyProject extends python implements Python {
    new main
    try main [static] // this won't work
}
```

**Example 2:**
```njin
interface njin {
    class MyProject extends python implements Python {
        new main
        try main [static] // this will :>
    }
}
```
We haven't shown you that you need this for the sake of simplicity.

#### `import <PATH>` - Importing nlibs

Nlibs hold all extendants and implementations. The base nlib is called `buckshot`, and it includes almost all file types you'd need. Buckshot is developed by the same studio as njin and is officially the default one. It usually comes bundled in with njin. Another one is `j-njin`. This is a third-party nlib, and it's designed to be an extension to buckshot, so no overlaps are included. The path can be anywhere on your computer, but remember to include the `.nlib` file extension.

**Example:**
```njin
import j-njin.nlib
import ../buckshot.nlib
import C:/Path/To/Some/Other/library.nlib
```

#### `super <NAME> <METHOD> [ARGS]` - `super` is the same as `try`, but you pass in the name of the file without having to create a variable

**Example:**
```njin
class MyProject extends python implements Python {
    super main [static] ("arg123")
} 
```

#### `["<COMMAND>"]` - This statement is called 'CMD LITERAL'

Add a command inside to run it in cmd.

**Example:**
```njin
["echo Hello, world!"] // output: Hello, world!
```

#### `return <true|false>` - Returning will end the current file on that line

Njins automatically return false at the end of the file.

#### `assert <PATH>` - Using assert will run another `.n` file

Once that file ends (runs into a return statement), depending on that return value,

 two things can happen:
- `true`: continue past the assert line
- `false`: end the file and return false

#### Changing the `void` environment variable

If you need to access a directory somewhere else on your system, and it would be impossible
or very tedious to get there using classes, you can change the `void` environment variable!

Changing it replaces the current path and removes all layers.

While you can't directly change it since `void` is a constant, you can create a `static copy`.
When you create a `static copy` of a constant, the original variable gets removed from all
running instances on that system, and the copy is inserted in it's former place. We can
create a `static copy` using the `[static]` descriptor
ex:
```njin
// this is file '.n' located in 'C:/Path/Towards/My/Project'

void[static] = "C:/Path/Towards/My/New"

class Project {
    // here is C:/Path/Towards/My/New/Project
    // you can build from here
}
```

### Extra Notes:

- Indentation is completely optional.
- Braces `{}` are optional, and opening braces can in most cases be completely removed, and closing braces can be substituted for the `break` statement.

  Though braces `{}` are preferred, in packages, a common convention is using `break` instead.

**Example:**
```njin
package python
    public Python
break

class MyProject
    abstract class 0
        super main [static]
    break
break
```

### Example of an njin (.n) File:

```njin
/*
Doc: this file is to run ./MyProject/build/index.html in chrome,
./MyProject/dist/script.js and compile and run ./MyProject/dist/main.c
*/

import buckshot.nlib
import j-njin.nlib

package javascript { // from buckshot
    public NodeJS
}

package chromeserver { // from j-njin
    public ChromeHTML
}

package c { // from buckshot
    private C
    protected GCC
}

interface njin {
    class MyProject {
        abstract class 0 extends chromeserver implements ChromeHTML {
            super index [static]
        }

        abstract class 1 extends javascript implements NodeJS {
            super script [static]

            interface CompilingC extends c implements c {
                super main [static]
            }

            interface RunningC extends c implements c.C {
                super main [static]
            }

        }
    }
}
return true
```

---
