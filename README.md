## Njin Language Documentation

### Overview
Njin is a micro-language designed to run files in a specific sequence. It allows you to structure projects by managing packages, implementations, classes, and variables, ensuring smooth execution of tasks across various file types and directories. The language is particularly useful for developers who need to automate or sequence the execution of files within a project.

### Statements and Syntax

#### 1. **`import <PATH>`**
   - **Purpose:** Imports an Njin library (nlib), which contains packages and implementations.
   - **Syntax:**
     ```njin
     import <library_path>
     ```
   - **Example:**
     ```njin
     import buckshot.nlib
     import j-njin.nlib
     import C:/Path/To/Some/Other/library.nlib
     ```

#### 2. **`package <PATH> {}`**
   - **Purpose:** Loads an external package from the imported libraries.
   - **Syntax:**
     ```njin
     package <package_name> {}
     ```
   - **Example:**
     ```njin
     import buckshot
     import j-njin

     package python {}
     ```
   - **Details:** 
     - If multiple imports contain a package with the same name, an overlap error is raised.

#### 3. **`public <NAME>`**
   - **Purpose:** Loads a public implementation from a package.
   - **Syntax:**
     ```njin
     public <implementation_name>
     ```
   - **Example:**
     ```njin
     package python {
         public Python
     }
     ```
   - **Details:**
     - Implementations have two attributes: 
       - `extension`: The file extension associated with the implementation (e.g., `.py`, `.c`).
       - `static`: The default command used to run files of this type (e.g., `py`, `gcc`, `start`).

#### 4. **`private <NAME>`**
   - **Purpose:** Loads a private implementation from a package, making it accessible via `<package>.<implementation>`.
   - **Syntax:**
     ```njin
     private <implementation_name>
     ```
   - **Example:**
     ```njin
     package python {
         private Python
     }
     ```

#### 5. **`class <NAME> extends <EXTENDANT> implements <IMPLEMENTATION> {}`**
   - **Purpose:** Creates a directory where files of a specified type can be generated and managed.
   - **Syntax:**
     ```njin
     class <class_name> extends <package_name> implements <implementation_name> {}
     ```
   - **Example:**
     ```njin
     class MyProject extends python implements Python {
     }
     ```
   - **Details:**
     - Defines a new directory layer. Nested classes further define subdirectories.

#### 6. **`class <NAME> {}`**
   - **Purpose:** Creates a directory without extending or implementing anything, useful for navigation without file creation.
   - **Syntax:**
     ```njin
     class <class_name> {}
     ```
   - **Example:**
     ```njin
     class MyProject {
         class build {
         }
     }
     ```

#### 7. **`abstract class <TYPE> extends <EXTENDANT> implements <IMPLEMENTATION> {}`**
   - **Purpose:** Creates a directory with a specific name based on the type (0 for `build`, 1 for `dist`).
   - **Syntax:**
     ```njin
     abstract class <type> extends <package_name> implements <implementation_name> {}
     ```
   - **Example:**
     ```njin
     abstract class 0 extends javascript implements JavaScript {
     }
     ```

#### 8. **`new <NAME>`**
   - **Purpose:** Creates a variable, which assigns a file name within the current directory.
   - **Syntax:**
     ```njin
     new <variable_name>
     ```
   - **Example:**
     ```njin
     new main // creates ./MyProject/main.c
     ```
   - **Details:**
     - Variables can only be created in extending layers.

#### 9. **`try <VARIABLENAME> <METHOD> [ARGS]`**
   - **Purpose:** Executes the file associated with the specified variable.
   - **Syntax:**
     ```njin
     try <variable_name> [method] (args)
     ```
   - **Example:**
     ```njin
     try start [static] ("arg1", "arg2")
     ```

#### 10. **`super <NAME> <METHOD> [ARGS]`**
   - **Purpose:** Runs a file directly without creating a variable.
   - **Syntax:**
     ```njin
     super <file_name> [method] (args)
     ```
   - **Example:**
     ```njin
     super main [static] ("arg123")
     ```

#### 11. **`interface <NAME> extends <EXTENDANT> implements <IMPLEMENTATION> {}`**
   - **Purpose:** Creates an interface, similar to a class but without adding directory layers.
   - **Syntax:**
     ```njin
     interface <interface_name> extends <package_name> implements <implementation_name> {}
     ```
   - **Example:**
     ```njin
     interface PyInterface extends python implements Python {
     }
     ```

#### 12. **`interface <NAME> {}`**
   - **Purpose:** Creates a non-extending interface. This is mostly used for the base `njin` interface.
   - **Syntax:**
     ```njin
     interface <interface_name> {}
     ```
   - **Example:**
     ```njin
     interface njin {
     }
     ```

#### 13. **`["<COMMAND>"]`**
   - **Purpose:** Executes a command in the command line directly.
   - **Syntax:**
     ```njin
     ["<command>"]
     ```
   - **Example:**
     ```njin
     ["echo Hello, world!"]
     ```

#### 14. **`return <true|false>`**
   - **Purpose:** Ends the execution of the current file and returns a boolean value.
   - **Syntax:**
     ```njin
     return <true|false>
     ```
   - **Details:** 
     - Files automatically return `false` at the end unless explicitly stated otherwise.

#### 15. **`assert <PATH>`**
   - **Purpose:** Runs another .n file and continues or terminates based on the returned value.
   - **Syntax:**
     ```njin
     assert <file_path>
     ```

### Example Project Structure

```njin
import buckshot
import j-njin

package python {
    public Python
}

package javascript {
    private NodeJS
}

    class MyProject extends python implements Python {
        new main // ./MyProject/main.py

        abstract class 0 extends javascript implements javascript.NodeJS {
            new start // ./MyProject/build/start.js
            try start [static]
        }

        try main [static]
    }
```

### Summary
Njin is a structured micro-language that enables precise file execution within a project, supporting a variety of file types and execution paths. By following this documentation, you can create, manage, and execute files in a methodical manner, streamlining your development process.
