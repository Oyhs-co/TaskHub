# TaskHub

TaskHub es una aplicación para la gestión de proyectos y el trabajo colaborativo, diseñada para ayudar a los equipos a organizar sus tareas y aumentar su productividad.

## Arquitectura

El backend de TaskHub sigue una arquitectura de microservicios, lo que facilita la escalabilidad y el mantenimiento de cada componente de forma independiente.

- **API Gateway:** Es el punto de entrada único para todas las peticiones de los clientes. Se encarga de redirigir el tráfico al microservicio correspondiente, además de gestionar la autenticación y la seguridad.
- **Servicio de Autenticación:** Gestiona el registro, inicio de sesión y la validación de usuarios, utilizando Supabase como proveedor de servicios de backend.

## Cómo empezar

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### Requisitos previos

- **Python:** Asegúrate de tener instalada una versión de Python 3.11 o superior.
- **Poetry:** Necesitarás [Poetry](https://python-poetry.org/docs/#installation) para gestionar las dependencias del proyecto.

### Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/taskhub.git
   cd taskhub
   ```

2. Instala las dependencias con Poetry:

   ```bash
   poetry install
   ```

### Configuración

El proyecto utiliza variables de entorno para gestionar la configuración. Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

```env
# Configuración del servicio de autenticación
PORT_AUTH=8001
SUPABASE_URL="TU_SUPABASE_URL"
SUPABASE_ANON_KEY="TU_SUPABASE_ANON_KEY"
SUPABASE_SERVICE_ROLE="TU_SUPABASE_SERVICE_ROLE_KEY"
SUPABASE_JWT_SECRET="TU_SUPABASE_JWT_SECRET"

# Configuración del API Gateway
PORT_GATEWAY=8000
AUTH_SERVICE_URL="http://localhost:8001"
```

**Nota:** Reemplaza los valores `"TU_..."` con tus propias credenciales de Supabase.

### Ejecución

Para iniciar los servicios, abre dos terminales separadas en la raíz del proyecto.

1. **En la primera terminal, inicia el servicio de autenticación:**

   ```bash
   poetry run uvicorn backend.auth.main:app --host 0.0.0.0 --port $PORT_AUTH --reload
   ```

2. **En la segunda terminal, inicia el API Gateway:**

   ```bash
   poetry run uvicorn backend.gateway.main:app --host 0.0.0.0 --port $PORT_GATEWAY --reload
   ```

Una vez completados estos pasos, el API Gateway estará disponible en `http://localhost:8000`.

## Uso

Una vez que los servicios están en funcionamiento, puedes interactuar con la API a través del Gateway.

### Endpoints

El API Gateway expone varios endpoints para interactuar con los microservicios. A continuación, se describen los principales:

- **Autenticación (`/auth`):**
  - `GET /auth/verify`: Verifica el token JWT del usuario y devuelve sus datos.

### Documentación Interactiva

Cada microservicio, incluido el API Gateway, cuenta con documentación interactiva gracias a FastAPI. Para explorarla, visita las siguientes URLs en tu navegador:

- **API Gateway:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Servicio de Autenticación:** [http://localhost:8001/docs](http://localhost:8001/docs)

En estas páginas, podrás ver todos los endpoints disponibles, sus parámetros y probarlos directamente desde el navegador.

## Sugerencias de mejora

A continuación, se presentan algunas sugerencias para mejorar el proyecto a corto, medio y largo plazo.

### Corto plazo

- **Calidad del código:**
  - **Linting y formateo:** Integrar herramientas como `flake8` y `black` para mantener un estilo de código consistente y detectar errores comunes.
  - **Pruebas unitarias:** Añadir pruebas unitarias para los componentes críticos, especialmente en el servicio de autenticación, para garantizar su fiabilidad.

- **Configuración:**
  - **Centralizar la configuración:** Utilizar un único archivo `.env` en la raíz del proyecto para ambos servicios, simplificando la gestión de las variables de entorno.

### Medio plazo

- **CI/CD:**
  - **Integración continua:** Configurar un pipeline de CI (con herramientas como GitHub Actions) para ejecutar las pruebas y el linter automáticamente en cada commit.
  - **Despliegue continuo:** Automatizar el despliegue de los servicios a un entorno de staging o producción.

- **Expansión de la API:**
  - **Nuevos microservicios:** Desarrollar microservicios adicionales para gestionar otras áreas de la aplicación, como proyectos, tareas o usuarios.

### Largo plazo

- **Observabilidad:**
  - **Stack de observabilidad:** Implementar herramientas como Prometheus para las métricas, Loki para los logs y Grafana para la visualización, obteniendo una visión completa del estado de los servicios.

- **Comunicación asíncrona:**
  - **Broker de mensajes:** Introducir un broker como RabbitMQ o Kafka para la comunicación asíncrona entre microservicios, mejorando la resiliencia y el desacoplamiento del sistema.
