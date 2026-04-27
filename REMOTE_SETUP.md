# Remote Setup

Esta configuración te permite mover las pruebas pesadas fuera de tu Mac y seguir usando la app desde el navegador.

## GitHub Actions

El repositorio ahora incluye el workflow [ci.yml](/Users/jorgekeles/Documents/news-assitance/.github/workflows/ci.yml) que:

- instala Python 3.11
- instala `ffmpeg` y `portaudio`
- instala dependencias
- compila los archivos Python
- ejecuta `test_components.py`

### Cómo usarlo

1. Sube el repo a GitHub.
2. En GitHub, abre `Settings > Secrets and variables > Actions`.
3. Crea el secreto `GEMINI_API_KEY` si querés que la validación también pruebe Gemini.
4. Cada `push` o `pull request` va a correr el workflow automáticamente.

## GitHub Codespaces

El proyecto ahora incluye un devcontainer en [.devcontainer/devcontainer.json](/Users/jorgekeles/Documents/news-assitance/.devcontainer/devcontainer.json).

### Qué prepara

- Python 3.11
- `ffmpeg`
- `portaudio19-dev`
- instalación automática de `requirements.txt`
- puerto `8501` reenviado para Streamlit

### Cómo abrirlo

1. Publica el repo en GitHub.
2. En GitHub, elegí `Code > Codespaces > Create codespace on main`.
3. Cuando abra, si hace falta copiá `.env.example` a `.env`.
4. Configurá `GEMINI_API_KEY` en `.env` o como Codespaces secret.
5. Ejecutá:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

6. Abrí el puerto `8501` cuando Codespaces lo ofrezca.

## Recomendación práctica

- Usá tu Mac para editar.
- Usá `GitHub Actions` para validar cambios.
- Usá `Codespaces` cuando quieras correr la app sin congelar la máquina.
