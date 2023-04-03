## Nombre: 
### Escuela el Trebol.

## Descripción: 
### El sistema prove de las operaciones básicas CRUD para recibir registros de aspirantes y que puedan pasar por un proceso de selección. 

#### El aspirante podrá:
    - crear un nuevo registro
    - ver su registro mediante su id que se le ha proporcionado
    - editar parámetros de su registro
    - borrar su registro

El proceso lo lleva a cabo un profesor quien decide si un aspirante es seleccionado o no.

El profesor debe de estar autenticado en la plataforma para lo cual se le ha provisto de un login con usuario y contraseña

#### Una vez logueado el profesor podrá:
    - Acceder a todos los registros
    - Aceptar o rechazar a un aspirante
    - Acceder a los estudiantes
    - Editar suspender, dar de baja o de alta a un estudiante


## Instalación:
    - Tener python 3.10 o superior instalado y el gestor de paquetes PIP añadido al path
    - Abrir una consola de comandos y teclear pip install virtualenv
    - Una vez instalado virtualenv ejecutar virtualenv <nombre de la carpeta que guardará el proyecto>
    - Creada la carpeta con el entorno virtual, navegar hasta La carpeta Scripts y ejecutar el comando activate
    - Una vez activado el entorno virtual regresaremos de nuevo en la carpeta que creamos al inicio
    - Guardaremos el proyecto en una carpeta con la siguiente estructura de archivos
    - En este ejemplo guardamos el proyecto en la carpeta llamada "back"

    ./carpeta_de_entorno_virtual
        |-    pyvenv.cfg
        |-    /gitignore
        |-    /include
        |-    /Lib
        |-    /Scripts
        |-    /back
            |-  .env
            |-  /auth
            |-  /schemas
            |-  /classmodels
            |-  /config
            |-  main.py
            |-  readme.md
            |-  requirements.txt

    - Navegamos a la carpeta donde guardamos el proyecto y ejecutamos pip install -r requirements.txt 
#### Así las dependencias estarán instaladas

### Configuracion de la base de datos    
    - Necesitaremos el cliente MySQL

    - Usando consola o Mysql Workbench cremamos un esquema en nuestro servidor llamado treboldb
    - Abrimos el archivo de configuración .env con un editor de texto editamos el USER, PASSWD, PORT y HOST acorde a la configuracion de nuestra base de datos

    - en una consola de comandos ejecutamos el comando  python main.py
#### El servidor debe correr en el puerto localhost:8000

## Cómo usar:
### Profesor:
    - En la ruta /signin pondremos nuestro nombre, un usuario y un password
    - Haremos login en la ruta /login que nos pedira user y password nos devolvera nuestro id de profesor profesor_id que habremos de usar para identificarnos en las demás rutas que estén hechas para los profesores
    
    - En la ruta /registros (GET) podremos ver todos los registros que se han hecho de aspirantes aceptados, rechazados y en espera de ser aceptados o no
    
    - En la ruta /registros/aspirantes (GET) podremos ver todos los registros que se han hecho de aspirantes en espera de ser aceptados o no

    - En la ruta /registros/aspirantes (POST) podremos aceptar o rechazar a un aspirante
    
    - En la ruta /estudiantes (GET) podremos ver a los estudiantes que fueron aceptados y a que grimorio fueron enviados
    
    - En la ruta /estudiantes (PUT) podremos dar de baja, dar de alta o suspender a un estudiante

### Aspirante:
    - En la ruta /solicitudes (POST) se podrá insertar un nuevo registro
    - En caso que el aspirante haya sido rechazado previamente se reiniciará su registro
    - En la ruta /solicitudes/<id_registro> (GET) se podrá obtener la info del registro indicado
    - En la ruta /solicitudes/<id_registro> (PUT) se podrá editar el registro indicado
    - En la ruta /solicitudes/<id_registro> (DELETE) se podrá eliminar el registro indicado