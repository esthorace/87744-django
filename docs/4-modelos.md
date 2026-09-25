# Campos y Tipos de Datos en Django

## Cadenas

- **`CharField`**:  
  Un campo de texto corto con una longitud máxima fija, especificada mediante el parámetro `max_length`. No tiene un valor predeterminado, por lo que `max_length` debe establecerse explícitamente.  
  - En **MySQL**, el tamaño máximo permitido para un `CharField` depende del límite de bytes por fila (65.535 bytes para InnoDB, incluido el overhead).  
  - En **PostgreSQL**, el tamaño máximo permitido está definido por `max_length` y no puede superarse.  

- **`TextField`**:  
  Un campo de texto largo sin longitud máxima definida en Django. Su límite depende de la capacidad de almacenamiento de la base de datos subyacente.  

## Números

- **`IntegerField`**:  
  Un campo que almacena números enteros, con un rango de -2.147.483.648 a 2.147.483.647. Aunque este rango es válido en todas las bases de datos compatibles. SQLite permite valores mayores internamente debido al tipo INTEGER no limitado.

- **`BigIntegerField`**:  
  Un campo para números enteros grandes, con un rango de -9.223.372.036.854.775.808 a 9.223.372.036.854.775.807. SQLite no es compatible con este campo.

- **`DecimalField`**:  
  Un campo para almacenar números decimales precisos, configurado con dos parámetros obligatorios:  
  - `max_digits`: Número total de dígitos permitidos (incluidos los decimales).  
  - `decimal_places`: Número de dígitos a la derecha del punto decimal.  
  Es ideal para aplicaciones que requieren cálculos financieros o alta precisión decimal. El rango depende de la configuración de estos parámetros y las capacidades de la base de datos.

- **`FloatField`**:  
  Un campo que almacena números en coma flotante. Aunque tiene un rango muy amplio (aproximadamente 2.23 x 10^-308 a 1.80 x 10^308), no es adecuado para cálculos financieros debido a las imprecisiones inherentes de los números de punto flotante.

- **`PositiveIntegerField`**:  
  Un campo para números enteros positivos, con un rango de 0 a 2.147.483.647. Este rango es validado por Django, no por la base de datos.

- **`PositiveSmallIntegerField`**:  
  Un campo para números enteros pequeños y positivos, con un rango de 0 a 32.767.

- **`SmallIntegerField`**:  
  Un campo para números enteros pequeños, con un rango de -32.768 a 32.767.

## Fechas y horas

- **`DateField`**: Almacena una fecha.  
- **`DateTimeField`**: Almacena una fecha y hora.  
- **`TimeField`**: Almacena una hora.  
- **`DurationField`**: Almacena un período de tiempo.

## Propias de las relaciones entre modelos

- **`AutoField`**:  
  Un identificador único generado automáticamente, utilizado normalmente como clave primaria. Para valores más grandes, usar **`BigAutoField`**.  

- **`ForeignKey`**:  
  Establece una relación uno a muchos entre dos modelos. Se requiere el argumento `on_delete` para definir el comportamiento al eliminar el objeto relacionado. Es posible usar `related_name` para definir relaciones inversas personalizadas.  

- **`ManyToManyField`**:  
  Define relaciones muchos a muchos. Django maneja automáticamente la creación de una tabla intermedia para almacenar las relaciones.

- **`UUIDField`**:  
  Almacena un identificador único universal (UUID), que es globalmente único y útil para garantizar escalabilidad, privacidad y universalidad en aplicaciones distribuidas.

## `on_delete` en `ForeignKey`

El parámetro `on_delete` define el comportamiento al eliminar un objeto relacionado:  

- `CASCADE`: Borra los objetos relacionados.
- `PROTECT`: Evita la eliminación generando una excepción.  
- `SET_NULL`: Establece los campos relacionados en `NULL` (requiere `null=True`).  
- `SET_DEFAULT`: Establece los campos en su valor predeterminado.  
- `SET()`: Establece los campos en un valor específico.  
- `DO_NOTHING`: No hace nada (puede causar referencias rotas).

## Archivos

- **`FileField`**:  
  Almacena archivos en el sistema de archivos del servidor y guarda su ruta en la base de datos. Puede almacenar cualquier tipo de archivo.

- **`ImageField`**:  
  Subclase de `FileField`, diseñada específicamente para imágenes. Requiere la instalación de **Pillow**. Realiza validaciones adicionales para garantizar que los archivos cargados sean imágenes válidas.

- **`BinaryField`**:  
  Almacena datos binarios directamente en la base de datos. Puede impactar negativamente el rendimiento si se usa para almacenar archivos grandes.

## Otros tipos de campo

- **`BooleanField`**: Almacena valores `True` o `False`.  
- **`EmailField`**: Verifica que el valor tenga un formato válido de correo electrónico.  
- **`URLField`**: Valida que el valor tenga un formato válido de URL.  
- **`SlugField`**: Almacena cadenas amigables para URL.  
- **`JSONField`**: Almacena datos JSON.
- **`ArrayField`**: Exclusivo de **PostgreSQL**, permite almacenar listas de valores en una sola columna.  
- **`IPAddressField`**: Almacena direcciones IPv4 válidas.  
- **`GenericIPAddressField`**: Almacena direcciones IPv4 o IPv6.
