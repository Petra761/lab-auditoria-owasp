# 🛡️ Auditoría de Seguridad Web (DAST/SAST) & Remediación OWASP Top 10

<p align="center">
  <img src="https://img.shields.io/badge/Asignatura-Seguridad%20Inform%C3%A1tica%20I-blue?style=for-the-badge&logo=security" alt="Seguridad Informática I">
  <img src="https://img.shields.io/badge/Flask-3.0.0-black?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/OWASP-Top10-F80000?style=for-the-badge&logo=owasp" alt="OWASP Top 10">
</p>

Repositorio oficial del laboratorio práctico de auditoría de seguridad web, análisis estático/dinámico (SAST/DAST) y refactorización segura de una API transaccional en Python/Flask y PostgreSQL.

---

## 🏛️ Contexto Académico

- **Institución:** Universidad Privada Domingo Savio (UPDS Sede Tarija)
- **Carrera / Semestre:** Ingeniería de Sistemas — 8vo Semestre
- **Asignatura:** Seguridad Informática I (SIS-0360)
- **Estudiante:** Herberth Marco Mamani Sanchez

---

## 📂 Estructura del Proyecto

```text
lab-auditoria-owasp/
├── app.py                # API Backend (Versión remediada y segura)
├── Dockerfile            # Configuración de contenedor Python
├── docker-compose.yml    # Orquestación de servicios (Web + Base de Datos)
├── init.sql              # Script SQL inicial con registros semilla
├── requirements.txt      # Dependencias del proyecto
└── sast_report.json      # Reporte de análisis estático (Semgrep)
```

---

## ⚠️ Vulnerabilidades Identificadas y Mitigadas (OWASP Top 10)

| ID OWASP     | Vulnerabilidad                    | Endpoint Afectado         | Estado                                              |
| ------------ | --------------------------------- | ------------------------- | --------------------------------------------------- |
| **A03:2021** | Inyección SQL (SQLi)              | `/api/socios/buscar`      | ✅ Mitigado (Consultas Parametrizadas)              |
| **A03:2021** | XSS Reflejado                     | `/api/socios/buscar`      | ✅ Mitigado (Sanitización con `markupsafe`)         |
| **A01:2021** | BOLA / IDOR                       | `/api/socios/<id>/perfil` | ✅ Mitigado (Control de autorización por cabeceras) |
| **A03:2021** | XSS Almacenado                    | `/api/comentarios`        | ✅ Mitigado (Escape de entradas POST)               |
| **A05:2021** | Fuga de Info y Falta de Cabeceras | Global (`after_request`)  | ✅ Mitigado (Cabeceras CSP, HSTS, no-sniff)         |

---

## 🚀 Guía de Despliegue Rápido

### Prerrequisitos

- Tener instalado **Docker** y **Docker Compose** en tu sistema (Linux/Ubuntu recomendado).

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu-usuario/lab-auditoria-owasp.git](https://github.com/tu-usuario/lab-auditoria-owasp.git)
cd lab-auditoria-owasp

```

### 2. Desplegar los contenedores

Levanta el entorno completo (Base de datos PostgreSQL + Servidor Web Flask) ejecutando:

```bash
docker compose up --build -d

```

### 3. Verificar el estado de los servicios

Comprueba que los contenedores estén activos y corriendo correctamente:

```bash
docker compose ps

```

---

## 🔍 Pruebas y Verificación

### Probar perfil de socio con cabeceras de autorización válidas (Acceso Permitido):

```bash
curl -i -H "X-User-Id: 1" -H "X-User-Rol: cliente" http://localhost:5000/api/socios/1/perfil

```

### Probar intento de acceso no autorizado (Prevención BOLA/IDOR):

```bash
curl -i -H "X-User-Id: 1" -H "X-User-Rol: cliente" http://localhost:5000/api/socios/2/perfil

```

_Debe retornar el código de estado `403 Forbidden`._

---

## 🛠️ Herramientas Empleadas

- **Contenedores:** Docker & Docker Compose.
- **Backend:** Python 3.11, Flask 3.0.0, Psycopg2.
- **Base de Datos:** PostgreSQL 15.
- **Análisis Estático (SAST):** Semgrep (`p/owasp-top-ten`).
- **Análisis Dinámico (DAST):** OWASP ZAP.

```

```
