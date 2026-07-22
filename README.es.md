# ReviewLens MCP

> Un servidor MCP seguro y explicable para asistir en la revisión técnica de pull requests de GitHub.

ReviewLens publica siete herramientas tipadas y estrictamente de lectura. Separa la recopilación determinista de evidencias de la interpretación del modelo, considera no fiable todo contenido del repositorio e incluye un proveedor simulado y una demo web sin credenciales.

![Recorrido visual de ReviewLens MCP](docs/images/reviewlens-demo.gif)

## Recorrido por el producto

La demo determinista completa una revisión realista sin necesitar un token de GitHub. Muestra las evidencias recopiladas, los tests relacionados, el nivel de riesgo y cualquier texto con apariencia de instrucción encontrado en contenido no fiable del repositorio.

![Revisión simulada con evidencias estructuradas](docs/images/simulated-review-evidence.png)

La superficie de herramientas es deliberadamente pequeña: siete operaciones con entradas explícitas y una única responsabilidad. La arquitectura mantiene MCP en la capa de adaptación y separa la lógica de revisión del acceso a GitHub.

![Herramientas y arquitectura de ReviewLens](docs/images/tools-and-architecture.png)

El modelo de seguridad se muestra de forma explícita: mínimo privilegio, evidencias acotadas, tratamiento del contenido no fiable y fallos visibles. La firma discreta en pixel art conecta el proyecto con su autora sin competir con el contenido técnico.

![Modelo de seguridad y firma de la autora](docs/images/security-and-creator.png)

## Inicio rápido

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -e ".[dev]"
    pytest
    reviewlens-demo

Abre http://127.0.0.1:8000.

## Servidor MCP

    reviewlens-mcp

El transporte predeterminado es stdio. El MVP no contiene herramientas para aprobar, fusionar, comentar ni modificar repositorios.

## Modo live

Copia .env.example como .env, selecciona REVIEWLENS_MODE=live y, si lo necesitas, configura un token con permisos de solo lectura para Contents y Pull requests. La credencial nunca llega al navegador.

## Diseño técnico

La separación proveedor → servicio → adaptadores permite probar la lógica sin depender de GitHub ni de un LLM. Consulta docs/architecture.md, docs/security.md y docs/limitations.md.

## Autora

Creado por **Paula García Fernández**.

- [GitHub](https://github.com/pgf3712)
- [LinkedIn](https://www.linkedin.com/in/paula-garcia-fernandez-pgf3712)

## Copyright

Copyright © 2026 Paula García Fernández. Todos los derechos reservados. El repositorio puede consultarse como portfolio personal y demostración técnica; cualquier reutilización requiere autorización previa por escrito. Consulta COPYRIGHT.md. La primera versión no incluye audio.
