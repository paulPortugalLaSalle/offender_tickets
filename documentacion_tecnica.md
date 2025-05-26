
# Documentación Técnica del Proyecto

---

## 1. Diseño de la base de datos

### Descripción general

La base de datos está diseñada para un sistema de control de infracciones de tránsito. El sistema permite que **usuarios policiales (PoliceUser)** emitan **boletas de infracción (Ticket)** a **ciudadanos infractores (OffenderUser)** relacionados con **vehículos (Vehicle)**.

###  Modelos principales

- **PoliceUser**  
  Usuario con permisos policiales. Hereda de `AbstractUser` de Django y usa el `email` como identificador único.

- **OffenderUser**  
  Representa a un ciudadano infractor. Contiene un identificador único (por ejemplo, DNI) y nombres.

- **Vehicle**  
  Vehículo asociado a una boleta. 

- **Ticket**  
  Representa una infracción. Contiene el monto, descripción, fecha, y relaciones con vehículo, infractor (opcional) y el usuario policial que la registró.

- **BaseModel (abstracto)**  
  Proporciona trazabilidad agregando campos `created_by`, `created_date`, `modified_date`.

### 📊 Diagrama ER Simplificado

```
[PoliceUser] ─────┐
                  │
[OffenderUser] ─┐ │
                ├─┴── [Ticket]
[Vehicle] ──────┘
```

- `Ticket.created_by` → PoliceUser (FK)
- `Ticket.offender` → OffenderUser (FK, opcional)
- `Ticket.vehicle` → Vehicle (FK)

---

## 🔌 2. Estructura de la API

### 📌 Framework Utilizado

- Se utilizó **Django REST Framework** para la construcción de los endpoints.
- Autenticación implementada mediante **JWT (JSON Web Tokens)**.
- Se implementó un **logger interno personalizado** en las vistas (`views.py`) para registrar eventos clave (creación, modificación, errores).
- El proyecto se ha **contenedorizado mediante Docker**, facilitando su despliegue en diferentes entornos.

### 🔁 Endpoints REST (ejemplo)

| Método | Endpoint                           | Descripción                                    |
|--------|------------------------------------|------------------------------------------------|
| GET    | `/api/tickets/list/`               | Lista todas las boletas creadas por el policia |
| POST   | `/api/tickets/create/`             | Crea una nueva boleta                          |
| GET    | `/api/tickets/ticket/{id}/`        | Recupera una boleta específica                 |
| PUT    | `/api/tickets/ticket/{id}/`        | Actualiza una boleta                           |
| DELETE | `/api/tickets/ticket/{id}/`        | Elimina una boleta (si aplica)                 |
| GET/POST | `/api/tickets/filter/?vehicle_id`  | Lista infractores por vehiculo                 |
| GET/PUT  | `/api/tickets/filter/?offender_id` | Lista infracciones por infractor               |

###  Autenticación

La API requiere autenticación vía JWT:

- Iniciar sesión: `/api/token/`  
  (envía email y contraseña para obtener `access` y `refresh`)
- Refrescar token: `/api/token/refresh/`

## 🐳 3. Dockerización del Proyecto

Se ha creado un entorno Docker para facilitar la configuración y despliegue del proyecto:

- Dockerfile y `docker-compose.yml` incluidos.
- Servicios: `web` (Django), `db` (PostgreSQL o SQLite).
- Comandos típicos:

```bash
docker-compose build
docker-compose up
```

Esto permite desplegar el sistema completo en minutos, sin depender del entorno local.

---

## 📝 Observaciones Finales

- La estructura está preparada para escalar con nuevos modelos (por ejemplo, historial de pagos, tipos de infracción).
- Todos los cambios críticos en vistas son registrados por el logger personalizado para facilitar la trazabilidad.
- Algunos Modelos estan enteramente con los datos necesarios para uso practico del ejercicio, estos se pueden mejorar u optimizar.