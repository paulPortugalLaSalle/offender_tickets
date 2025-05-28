# Sistema de control de infracciones de transito

Este es un pequeño sistema de control de infracciones



## Instalacion

Para instalar y compilar este sistema, debes seguir los siguientes pasos.

1. Clonar este proyecto.
2. crear tu archivo .env
Usa la siguiente conf con la finalidad de no cambiar la configuracion en el compose de Docker.

```
DEBUG=True
SECRET_KEY=django-insecure-ab=h3)%%v=p**e%xovr*lz4_itobvmfha^qaf4fy%^x2fq0=y6
DB_NAME=traffic_ticket_DB
DB_USER=postgres
DB_PASSWORD=plop123PLOP
```
3. Crea un file llamado logs al mismo nivel del settings.py

4. Ejecutar el la imagen Docker con el siguiente comando con 
```
docker-compose up --build
```
5. Ejecuta las migraciones con
```
docker-compose exec web python manage.py migrate
```
5. Crear un superusuario con el email de login
```
docker-compose exec web python manage.py createsuperuser
```
6. Diviertete: Crea un par de usuarios policia(setea nombres y apellidos) y empieza con el uso del sistema




## API´S

#### Autenticacion

```http
  POST api/accounts/token/
```

| Body Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. user email|
| `password` | `string` | **Required**. password of email|

#### Registrar infraccion

```http
  POST api/tickets/create/
```

| Body Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vehicle`      | `string` | **Required**. placa del vehiculo |
| `offender_names`      | `string` | **Required**. id del infractor |
| `offender_ident`      | `string` | **Required**. nombres del infractor |
| `amount`      | `float` | **Required**. multa |
| `description`      | `string` | **Not Required**.  |
| `fecha`      | `date` | **Not Required**. fecha de registro |
| **Header** | **Type**     | **Description**                       |
| `Authentication`      | `string` | **Required**. Bearer token |

#### Actualizar infraccion

```http
  PUT api/tickets/ticket/<int:pk>/
```

| Body Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vehicle`      | `string` | **Required**. placa del vehiculo |
| `offender_names`      | `string` | **Required**. id del infractor |
| `offender_ident`      | `string` | **Required**. nombres del infractor |
| `amount`      | `float` | **Required**. multa |
| `description`      | `string` | **Not Required**.  |
| `fecha`      | `date` | **Not Required**. fecha de registro |
| **Parameter** | **Type**     | **Description**                       |
| `pk`      | `int` | **Required**. id del objeto |
| **Header** | **Type**     | **Description**                       |
| `Authentication`      | `string` | **Required**. Bearer token |

#### Eliminar infraccion

```http
  DELETE api/tickets/ticket/<int:pk>/
```

| URl Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. id del objeto |
| **Header** | **Type**     | **Description**                       |
| `Authentication`      | `string` | **Required**. Bearer token |

#### Filtro por vehiculo
```http
  GET api/tickets/filter/?vehicle_id=vehiculo1
```
|  Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vehicle_id`      | `str` | **Required**. id del vehiculo |

#### Filtro por infractor
```http
  GET api/tickets/filter/?offender_id=placa1
```
|  Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `offender_id`      | `str` | **Required**. id del infractor |
## Tests

Para ejecutar los test es necesario que la imagen docker este corriendo
1. Test de autenticacion
```bash
  docker-compose exec web python manage.py test tests.accounts.test_account
```
2. Test de Consulta de Infracciones
```bash
  docker-compose exec web python manage.py test tests.tickets.test_get_tickets
```
3. Test CRUD de Infracciones
```bash
  docker-compose exec web python manage.py test tests.tickets.test_tickets_crud
```
